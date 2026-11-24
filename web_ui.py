#!/usr/bin/env python3
"""TBot Web UI – read / chat-info / send / HTML-Bericht senden.

Spricht direkt mit der Telegram Bot API (kein Umweg ueber das CLI-Skript).

Token-Quelle (erste gefundene gewinnt):
  1. Umgebungsvariable TELEGRAM_BOT_TOKEN (oder TBOT_TOKEN)
  2. Datei .env im selben Ordner mit Zeile  TELEGRAM_BOT_TOKEN=123:ABC...

Start:  python3 web_ui.py   ->  http://127.0.0.1:5055
"""
import html
import json
import os
from pathlib import Path

import requests
from flask import Flask, request, render_template_string

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CHAT_ID = os.environ.get("TBOT_DEFAULT_CHAT_ID", "9150544387")
REPORT_DIR = Path(
    os.environ.get("GHOSTINTEL_OUTPUT", BASE_DIR.parent / "GhostIntel" / "output")
).expanduser().resolve()


def load_token():
    for key in ("TELEGRAM_BOT_TOKEN", "TBOT_TOKEN"):
        if os.environ.get(key):
            return os.environ[key].strip()
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() in ("TELEGRAM_BOT_TOKEN", "TBOT_TOKEN"):
                    return v.strip().strip('"').strip("'")
    return None


TOKEN = load_token()
API = f"https://api.telegram.org/bot{TOKEN}/" if TOKEN else None

app = Flask(__name__)


def tg(method, data=None, files=None):
    """Telegram-API-Aufruf; gibt (ok, text) zurueck."""
    if not API:
        return False, "Kein Bot-Token gefunden. Setze TELEGRAM_BOT_TOKEN oder lege .env an."
    try:
        r = requests.post(API + method, data=data, files=files, timeout=30)
        payload = r.json()
    except Exception as exc:  # Netzwerk / JSON
        return False, f"Fehler bei {method}: {exc}"
    if not payload.get("ok"):
        return False, f"Telegram-Fehler ({method}): {payload.get('description')}"
    return True, json.dumps(payload["result"], indent=2, ensure_ascii=False)


def clean_chat_id(raw):
    raw = (raw or "").strip()
    if not raw:
        return None
    if raw.startswith("@"):
        return raw
    if raw.lstrip("-").isdigit():
        return raw
    return None


def list_reports():
    if not REPORT_DIR.is_dir():
        return []
    files = [p for p in REPORT_DIR.rglob("*") if p.suffix.lower() in (".html", ".htm")]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p.relative_to(REPORT_DIR)) for p in files]


def resolve_report(rel):
    if not rel:
        return None
    path = (REPORT_DIR / rel).resolve()
    if REPORT_DIR not in path.parents or not path.is_file():
        return None
    return path


PAGE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>TBot Web UI</title>
<style>
 body{background:#17181c;color:#e6e6e6;font-family:sans-serif;max-width:820px;margin:40px auto;padding:0 16px}
 label{display:inline-block;min-width:110px}
 input,select{background:#202228;color:#eee;border:1px solid #444;border-radius:4px;padding:8px;margin:4px 0}
 input[name=chat_id]{width:220px} input[name=text]{width:420px} select{width:420px}
 button{background:#2f6db5;color:#fff;border:0;border-radius:4px;padding:9px 14px;margin:4px 2px;cursor:pointer}
 pre{background:#0f1014;padding:14px;border-radius:6px;white-space:pre-wrap;word-break:break-word}
 .err{color:#ff7b7b} .ok{color:#7bdc8f} hr{border-color:#444}
 small{color:#999}
</style></head><body>
<h2>TBot Web UI</h2>
<form method="post">
  <button name="action" value="read">Updates lesen (read)</button>
  <hr>
  <div><label>Chat-ID:</label>
    <input name="chat_id" value="{{ chat_id }}" placeholder="9150544387 oder -100...">
    <button name="action" value="chat_info">Chat-Info</button></div>
  <div><label>Nachricht:</label>
    <input name="text" value="" placeholder="Text ...">
    <button name="action" value="send">Nachricht senden</button></div>
  <div><label>HTML-Bericht:</label>
    <select name="report">
      {% for r in reports %}<option value="{{ r }}">{{ r }}</option>{% endfor %}
      {% if not reports %}<option value="">(keine .html in {{ report_dir }})</option>{% endif %}
    </select>
    <button name="action" value="send_report">Bericht senden</button></div>
  <small>Bericht-Ordner: {{ report_dir }}</small>
</form>
<h3>Ausgabe</h3>
<pre class="{{ cls }}">{{ output }}</pre>
</body></html>"""


@app.route("/", methods=["GET", "POST"])
def index():
    output, cls = "Bereit.", ""
    chat_id_raw = request.form.get("chat_id", DEFAULT_CHAT_ID)
    if request.method == "POST":
        action = request.form.get("action")
        chat_id = clean_chat_id(chat_id_raw)
        text = request.form.get("text", "").strip()

        if action == "read":
            ok, output = tg("getUpdates", {"timeout": 0})
        elif not chat_id:
            ok, output = False, "Chat-ID fehlt oder ist ungueltig (nur Zahl, -Zahl oder @name)."
        elif action == "chat_info":
            ok, output = tg("getChat", {"chat_id": chat_id})
        elif action == "send":
            if not text:
                ok, output = False, "Nachrichtentext ist leer."
            else:
                ok, output = tg("sendMessage", {"chat_id": chat_id, "text": text[:4096]})
        elif action == "send_report":
            path = resolve_report(request.form.get("report"))
            if not path:
                ok, output = False, "Kein gueltiger Bericht ausgewaehlt."
            else:
                with path.open("rb") as fh:
                    ok, output = tg(
                        "sendDocument",
                        {"chat_id": chat_id, "caption": path.name[:1024]},
                        files={"document": (path.name, fh, "text/html")},
                    )
        else:
            ok, output = False, f"Unbekannte Aktion: {action}"
        cls = "ok" if ok else "err"

    return render_template_string(
        PAGE,
        output=output,
        cls=cls,
        chat_id=chat_id_raw,
        reports=list_reports(),
        report_dir=REPORT_DIR,
    )


if __name__ == "__main__":
    if not TOKEN:
        print("WARNUNG: Kein Bot-Token gefunden (TELEGRAM_BOT_TOKEN oder .env).")
    app.run(host="127.0.0.1", port=5055)
