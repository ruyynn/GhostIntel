#!/bin/bash
cd ~/Schreibtisch/Tollspon/tbot || { echo "Ordner nicht gefunden"; read -p "Enter..."; exit 1; }
export TELEGRAM_BOT_TOKEN="$(grep -oP '(?<=^BOT_TOKEN=).*' ~/Tbotv2.py)"
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then echo "Token nicht in ~/Tbotv2.py gefunden"; read -p "Enter..."; exit 1; fi
echo "=================================================="
echo "  Im Browser oeffnen:  http://127.0.0.1:5055"
echo "  Beenden:             Strg + C"
echo "=================================================="
python3 web_ui.py
