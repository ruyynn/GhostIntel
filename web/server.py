#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GhostIntel v2.5 - Web Server (Enhanced with Breach Detection & Risk Score)
Flask localhost interface — python ghostintel.py -web
"""

import asyncio
import json
import threading
import webbrowser
import time
import sys
from pathlib import Path
from datetime import datetime

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.engine import GhostIntelEngine
from core.detector import detector
from core.banner import console

app = Flask(__name__)
CORS(app)


# ─────────────────────────────────────────────────────────────────────────────
#  FULL WEB UI  (single HTML page, zero CDN, works offline)
# ─────────────────────────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GhostIntel v2.5</title>
<style>
:root{
  --bg:#0a0c10;--bg2:#0d1117;--bg3:#161b22;--bg4:#1c2128;
  --border:#21262d;--border2:#30363d;
  --cyan:#22d3ee;--cyan2:#06b6d4;--cyan3:#0891b2;
  --green:#4ade80;--green2:#22c55e;
  --yellow:#fbbf24;--red:#f87171;--purple:#a78bfa;--orange:#fb923c;
  --text:#e6edf3;--text2:#8b949e;--text3:#6e7681;
  --magenta:#d946ef;
  --shadow:0 8px 32px rgba(0,0,0,.6);
}
*{box-sizing:border-box;margin:0;padding:0}
html{height:100%}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;height:100vh;display:flex;flex-direction:column;overflow:hidden}

/* ── TOP BAR ── */
header{
  background:var(--bg2);border-bottom:1px solid var(--border);
  display:flex;align-items:center;padding:0 20px;height:52px;
  flex-shrink:0;gap:12px;z-index:50;
}
.logo{
  font-family:'Courier New',monospace;font-size:1.05rem;font-weight:700;
  color:var(--magenta);letter-spacing:3px;white-space:nowrap;
}
.logo em{color:var(--cyan);font-style:normal}
.ver-badge{
  font-size:.65rem;background:rgba(34,211,238,.1);border:1px solid rgba(34,211,238,.25);
  color:var(--cyan);padding:2px 8px;border-radius:10px;letter-spacing:.5px;
}
.live-dot{
  margin-left:auto;display:flex;align-items:center;gap:6px;
  font-size:.72rem;color:var(--green);
}
.dot{width:7px;height:7px;border-radius:50%;background:var(--green);animation:blink 2s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}

/* ── LAYOUT ── */
.body{display:flex;flex:1;overflow:hidden}
aside{
  width:230px;min-width:230px;background:var(--bg2);
  border-right:1px solid var(--border);display:flex;flex-direction:column;
  overflow-y:auto;
}
main{flex:1;overflow-y:auto;padding:20px 24px}

/* ── SIDEBAR ── */
.sb-section{padding:14px 12px 6px}
.sb-label{font-size:.6rem;letter-spacing:1.8px;text-transform:uppercase;color:var(--text3);padding:0 4px 8px;font-weight:600}
.sb-btn{
  width:100%;text-align:left;background:none;border:none;
  color:var(--text2);padding:7px 10px;border-radius:6px;
  cursor:pointer;font-size:.82rem;display:flex;align-items:center;gap:9px;
  transition:all .15s;
}
.sb-btn:hover{background:var(--bg3);color:var(--text)}
.sb-btn.act{background:rgba(34,211,238,.1);color:var(--cyan);border-left:2px solid var(--cyan);border-radius:0 6px 6px 0}
.sb-btn .ic{font-size:.95rem;width:18px;text-align:center}
.sb-divider{height:1px;background:var(--border);margin:6px 12px}
.hist-item{
  padding:7px 14px;cursor:pointer;font-size:.76rem;
  color:var(--text3);display:flex;align-items:center;gap:7px;
  transition:all .15s;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;
}
.hist-item:hover{color:var(--text2);background:var(--bg3)}
.hist-type{
  font-size:.6rem;background:var(--bg3);border:1px solid var(--border2);
  border-radius:3px;padding:1px 5px;color:var(--cyan);flex-shrink:0;
}
.hist-target{overflow:hidden;text-overflow:ellipsis}

/* ── SEARCH CARD ── */
.search-card{
  background:var(--bg2);border:1px solid var(--border);
  border-radius:10px;padding:20px;margin-bottom:18px;
}
.sc-title{font-size:1.1rem;font-weight:700;color:var(--text);margin-bottom:3px}
.sc-sub{font-size:.78rem;color:var(--text2);margin-bottom:16px}
.type-tabs{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:14px}
.tab{
  background:var(--bg3);border:1px solid var(--border);color:var(--text2);
  padding:4px 13px;border-radius:14px;cursor:pointer;font-size:.77rem;
  transition:all .15s;
}
.tab:hover{border-color:var(--cyan);color:var(--cyan)}
.tab.act{background:rgba(34,211,238,.12);border-color:var(--cyan);color:var(--cyan)}
.input-row{display:flex;gap:8px}
.target-in{
  flex:1;background:var(--bg3);border:1px solid var(--border2);color:var(--text);
  padding:9px 14px;border-radius:7px;font-size:.92rem;outline:none;
  font-family:'Courier New',monospace;transition:border-color .2s;
}
.target-in:focus{border-color:var(--cyan)}
.target-in::placeholder{color:var(--text3)}
.scan-btn{
  background:var(--cyan2);color:#000;border:none;padding:9px 22px;
  border-radius:7px;cursor:pointer;font-weight:800;font-size:.88rem;
  letter-spacing:.5px;transition:all .15s;white-space:nowrap;
}
.scan-btn:hover:not(:disabled){background:var(--cyan);transform:translateY(-1px);box-shadow:0 4px 12px rgba(34,211,238,.3)}
.scan-btn:disabled{background:var(--bg3);color:var(--text3);cursor:not-allowed;transform:none}
.opts-row{margin-top:10px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.opt{display:flex;align-items:center;gap:5px;cursor:pointer;font-size:.78rem;color:var(--text2)}
.opt input{accent-color:var(--cyan)}
#detected{font-size:.72rem;color:var(--yellow);margin-left:auto}

/* ── STATUS ── */
#statusBar{
  background:var(--bg3);border:1px solid var(--border);border-radius:7px;
  padding:10px 14px;font-family:'Courier New',monospace;font-size:.8rem;
  color:var(--cyan);margin-bottom:16px;align-items:center;gap:9px;
  display:none;
}
#statusBar.show{display:flex}
.sdot{width:7px;height:7px;border-radius:50%;background:var(--cyan);animation:blink 1s infinite;flex-shrink:0}
.sdot.ok{background:var(--green);animation:none}
.sdot.err{background:var(--red);animation:none}

/* ── RESULTS ── */
.results-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.results-title{font-size:.95rem;font-weight:600}
.results-meta{font-size:.73rem;color:var(--text3)}
.mod-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}

/* ── MODULE CARD ── */
.mod{background:var(--bg3);border:1px solid var(--border);border-radius:9px;overflow:hidden;transition:border-color .2s}
.mod:hover{border-color:var(--border2)}
.mod.username{border-top:2px solid var(--cyan)}
.mod.email   {border-top:2px solid var(--purple)}
.mod.phone   {border-top:2px solid var(--green)}
.mod.domain  {border-top:2px solid var(--yellow)}
.mod.ip      {border-top:2px solid var(--orange)}
.mod-hdr{padding:12px 14px;display:flex;align-items:center;gap:9px;border-bottom:1px solid var(--border)}
.mod-ic{font-size:1.1rem}
.mod-name{font-weight:600;font-size:.86rem}
.mod-badge{margin-left:auto;font-size:.62rem;padding:2px 7px;border-radius:8px;font-weight:700}
.b-found{background:#122a12;color:var(--green)}
.b-none {background:#2a1212;color:var(--red)}
.mod-body{padding:12px 14px}
.row{display:flex;justify-content:space-between;align-items:flex-start;padding:4px 0;border-bottom:1px solid rgba(33,38,45,.6);font-size:.79rem;gap:10px}
.row:last-child{border-bottom:none}
.rk{color:var(--text2);flex-shrink:0}
.rv{color:var(--text);text-align:right;font-family:'Courier New',monospace;font-size:.76rem;word-break:break-all;max-width:190px}
.rv a{color:var(--cyan);text-decoration:none}
.rv a:hover{text-decoration:underline}
.rv.ok{color:var(--green)}
.rv.warn{color:var(--yellow)}
.rv.bad{color:var(--red)}

/* ── BREACH ALERT STYLES ── */
.breach-alert{background:linear-gradient(135deg,rgba(239,68,68,.1),rgba(245,158,11,.05));border-left:4px solid var(--red);margin-bottom:10px}
.breach-detail{background:var(--bg2);padding:8px;border-radius:6px;margin-bottom:6px;border-left:2px solid var(--yellow)}
.recommendation-box{background:rgba(59,130,246,.1);padding:8px;border-radius:6px;margin-top:8px;border-left:2px solid var(--blue)}

/* ── PLATFORM PILLS ── */
.plat-list{display:flex;flex-wrap:wrap;gap:4px;margin-top:8px}
.pill{
  background:rgba(34,211,238,.07);border:1px solid rgba(34,211,238,.18);
  color:var(--cyan);font-size:.67rem;padding:2px 7px;border-radius:10px;
  text-decoration:none;transition:background .15s;
}
.pill:hover{background:rgba(34,211,238,.18)}
.category-header{margin-top:8px;margin-bottom:4px;font-size:.7rem;color:var(--text2)}
.category-header:first-child{margin-top:0}

/* ── PROGRESS BAR ── */
.progress-bar-bg{background:var(--bg2);border-radius:10px;height:6px;overflow:hidden;margin:6px 0}
.progress-bar-fill{background:linear-gradient(90deg,var(--red),var(--yellow));height:100%;border-radius:10px;transition:width .3s}

/* ── TAGS ── */
.tag{display:inline-block;padding:2px 8px;border-radius:12px;font-size:.65rem;margin:2px}
.tag-danger{background:rgba(239,68,68,.2);color:var(--red);border:1px solid var(--red)}
.tag-warning{background:rgba(245,158,11,.2);color:var(--yellow);border:1px solid var(--yellow)}
.tag-success{background:rgba(74,222,128,.2);color:var(--green);border:1px solid var(--green)}
.tag-info{background:rgba(34,211,238,.2);color:var(--cyan);border:1px solid var(--cyan)}

/* ── EMPTY / ERROR ── */
.empty{text-align:center;padding:50px 20px;color:var(--text3)}
.empty-ic{font-size:2.8rem;margin-bottom:14px;opacity:.35}
.empty-t{font-size:.88rem}

/* ── SKELETON ── */
.skel{
  background:linear-gradient(90deg,var(--bg3) 25%,var(--bg4) 50%,var(--bg3) 75%);
  background-size:200% 100%;animation:shimmer 1.4s infinite;border-radius:4px;
}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}

/* ── TOAST ── */
#toast{
  position:fixed;bottom:20px;right:20px;background:var(--bg3);
  border:1px solid var(--border2);color:var(--text);padding:10px 16px;
  border-radius:7px;font-size:.82rem;opacity:0;transform:translateY(8px);
  transition:all .25s;pointer-events:none;z-index:999;
}
#toast.show{opacity:1;transform:translateY(0)}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px}

@media(max-width:700px){
  aside{display:none}
  .mod-grid{grid-template-columns:1fr}
  header{padding:0 12px}
  main{padding:14px}
}
</style>
</head>
<body>

<header>
  <span class="logo">GHOST<em>INTEL</em></span>
  <span class="ver-badge">v2.5</span>
  <div class="live-dot"><span class="dot"></span> LOCALHOST</div>
</header>

<div class="body">
<aside id="sidebar">
  <div class="sb-section">
    <div class="sb-label">Scan Mode</div>
    <button class="sb-btn act" onclick="setScanMode(this,'quick')" id="modeQuick">
      <span class="ic">⚡</span> Quick Scan
    </button>
    <button class="sb-btn" onclick="setScanMode(this,'deep')" id="modeDeep">
      <span class="ic">🔬</span> Deep Scan
    </button>
  </div>
  <div class="sb-divider"></div>
  <div class="sb-section">
    <div class="sb-label">History</div>
    <div id="histList"><div style="padding:6px 4px;font-size:.75rem;color:var(--text3)">No history yet</div></div>
  </div>
</aside>

<main>
  <div class="search-card">
    <div class="sc-title">🔍 OSINT Investigation</div>
    <div class="sc-sub">Analyze usernames · emails · phones · domains · IPs from public sources only. No API keys.</div>
    <div class="type-tabs">
      <div class="tab act" data-t="auto" onclick="selType(this)">🤖 Auto</div>
      <div class="tab" data-t="username" onclick="selType(this)">👤 Username</div>
      <div class="tab" data-t="email" onclick="selType(this)">📧 Email</div>
      <div class="tab" data-t="phone" onclick="selType(this)">📱 Phone</div>
      <div class="tab" data-t="domain" onclick="selType(this)">🌐 Domain</div>
      <div class="tab" data-t="ip" onclick="selType(this)">🌍 IP</div>
    </div>
    <div class="input-row">
      <input id="tin" class="target-in" type="text"
        placeholder="Target: username / email / +628xx / domain.com / 8.8.8.8"
        onkeydown="if(event.key==='Enter')doScan()"
        oninput="detectLive(this.value)"
        autofocus>
      <button class="scan-btn" id="scanBtn" onclick="doScan()">SCAN ▶</button>
    </div>
    <div class="opts-row">
      <label class="opt"><input type="checkbox" id="deepCk"> Deep (all modules)</label>
      <label class="opt"><input type="checkbox" id="reportCk"> Save report</label>
      <span id="detected"></span>
    </div>
  </div>

  <div id="statusBar">
    <span class="sdot" id="sdot"></span>
    <span id="stxt">Ready</span>
  </div>

  <div id="results">
    <div class="empty">
      <div class="empty-ic">👻</div>
      <div class="empty-t">Enter a target above to start investigating</div>
      <div style="margin-top:6px;font-size:.73rem;color:var(--text3)">GhostIntel uses public sources only — no illegal access</div>
    </div>
  </div>
</main>
</div>
<div id="toast"></div>

<script>
let curType = 'auto';
let scanMode = 'quick';
let history = JSON.parse(localStorage.getItem('gi25_hist') || '[]');
const PLACEHOLDER = {
  auto: 'Target: username / email / +628xx / domain.com / 8.8.8.8',
  username: 'Username (e.g. ruyynn)',
  email: 'Email (e.g. user@gmail.com)',
  phone: 'Phone (e.g. 08123456789 or +12125551234)',
  domain: 'Domain (e.g. example.com)',
  ip: 'IP Address (e.g. 8.8.8.8 or 2606:4700::)',
};

renderHistory();

function selType(el) {
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('act'));
  el.classList.add('act');
  curType = el.dataset.t;
  document.getElementById('tin').placeholder = PLACEHOLDER[curType];
  document.getElementById('detected').textContent = '';
}

function setScanMode(el, m) {
  document.querySelectorAll('.sb-btn').forEach(b=>b.classList.remove('act'));
  el.classList.add('act');
  scanMode = m;
  document.getElementById('deepCk').checked = m === 'deep';
}

function detectLive(val) {
  if (!val || curType !== 'auto') { document.getElementById('detected').textContent=''; return; }
  const d = document.getElementById('detected');
  if (/^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$/i.test(val)) d.textContent='📧 Detected: email';
  else if (/(\+?\d[\d\s\-]{7,14})/.test(val) && val.replace(/\D/g,'').length >= 8) d.textContent='📱 Detected: phone';
  else if (/^(\d{1,3}\.){3}\d{1,3}$/.test(val) || /^[0-9a-f:]+$/i.test(val)) d.textContent='🌍 Detected: IP';
  else if (/^[a-z0-9\-]+(\.[a-z]{2,})+$/i.test(val)) d.textContent='🌐 Detected: domain';
  else if (val.length >= 2) d.textContent='👤 Detected: username';
  else d.textContent='';
}

async function doScan() {
  const target = document.getElementById('tin').value.trim();
  if (!target) { showToast('⚠️ Enter a target first'); return; }
  const deep = document.getElementById('deepCk').checked;
  const report = document.getElementById('reportCk').checked;
  const btn = document.getElementById('scanBtn');
  const bar = document.getElementById('statusBar');
  const dot = document.getElementById('sdot');
  const stxt = document.getElementById('stxt');
  btn.disabled = true; btn.textContent = 'SCANNING...';
  bar.classList.add('show');
  dot.className = 'sdot';
  stxt.textContent = `Scanning "${target}" — please wait...`;
  showSkeleton();
  try {
    const res = await fetch('/api/scan', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({target, type: curType, deep, report})
    });
    const data = await res.json();
    if (data.error) {
      dot.className = 'sdot err';
      stxt.textContent = '❌ ' + data.error;
      showError(data.error);
    } else {
      const mods = Object.keys(data.results||{}).filter(k=>!k.startsWith('_'));
      dot.className = 'sdot ok';
      stxt.textContent = `✅ Done — ${mods.length} module(s) — "${target}" — ${new Date().toLocaleTimeString()}`;
      renderResults(data.results, target, data.detected_type);
      addHistory(target, data.detected_type || curType);
      if (data.report_file) showToast('📄 Report saved: ' + data.report_file);
    }
  } catch(e) {
    dot.className = 'sdot err';
    stxt.textContent = '❌ Connection error: ' + e.message;
    showError('Server unreachable — is GhostIntel running?');
  }
  btn.disabled = false; btn.textContent = 'SCAN ▶';
}

function showSkeleton() {
  document.getElementById('results').innerHTML = `<div class="results-hdr"><div class="results-title" style="color:var(--text3)">Scanning…</div></div>
    <div class="mod-grid">${[1,2,3].map(()=>`<div class="mod" style="padding:16px"><div class="skel" style="width:40%;height:11px;margin-bottom:10px"></div><div class="skel" style="width:90%;height:9px;margin-bottom:7px"></div><div class="skel" style="width:70%;height:9px"></div></div>`).join('')}</div>`;
}

function renderResults(results, target, dtype) {
  if (!results) { showError('No results'); return; }
  const mods = Object.entries(results).filter(([k])=>!k.startsWith('_'));
  if (!mods.length) { showError('No results found for: '+target); return; }
  let html = `<div class="results-hdr"><div class="results-title">Results for <span style="color:var(--cyan)">${esc(target)}</span>${dtype ? `<span style="color:var(--text3);font-size:.75rem;margin-left:8px">[${dtype}]</span>` : ''}</div><div class="results-meta">${mods.length} module(s) · ${new Date().toLocaleTimeString()}</div></div><div class="mod-grid">`;
  mods.forEach(([name,result]) => { html += buildModCard(name, result); });
  html += '</div>';
  document.getElementById('results').innerHTML = html;
}

function buildModCard(name, result) {
  const icons = {username:'👤',email:'📧',phone:'📱',domain:'🌐',ip:'🌍'};
  const icon = icons[name]||'🔍';
  const data = result?.data || {};
  const hasData = result && !result.error;
  const badge = hasData ? '<span class="mod-badge b-found">✓ FOUND</span>' : '<span class="mod-badge b-none">✗ NONE</span>';
  let body = '';
  if (!hasData) body = `<div style="color:var(--red);font-size:.8rem;padding:4px 0">${esc(result?.error||'No data')}</div>`;
  else if (name === 'username') body = buildUsername(data);
  else if (name === 'email') body = buildEmail(data);
  else if (name === 'phone') body = buildPhone(data);
  else if (name === 'domain') body = buildDomain(data);
  else if (name === 'ip') body = buildIP(data);
  else body = row('Data', JSON.stringify(data).slice(0,200));
  return `<div class="mod ${name}"><div class="mod-hdr"><span class="mod-ic">${icon}</span><span class="mod-name">${name.toUpperCase()} OSINT</span>${badge}</div><div class="mod-body">${body}</div></div>`;
}

function buildUsername(d) {
  const found = d.found || [];
  const total = d.total_found || 0;
  let html = row('Username', d.username) + row('Checked', `${d.total_checked||0} platforms`) + row('Found', `<span class="${total>0?'ok':'bad'}">${total} platforms</span>`);
  if (d.categories?.length) html += row('Categories', d.categories.join(', '));
  if (d.possible_emails?.length) html += row('Email hints', d.possible_emails.slice(0,3).join('<br>'));
  if (found.length) {
    html += `<div style="margin-top:8px;font-size:.72rem;color:var(--text3)">Found on:</div><div class="plat-list">`;
    found.slice(0,30).forEach(p => { html += `<a class="pill" href="${esc(p.url)}" target="_blank">${esc(p.platform)}</a>`; });
    if (found.length > 30) html += `<span class="pill" style="cursor:default">+${found.length-30} more</span>`;
    html += '</div>';
  }
  return html;
}

function buildEmail(d) {
  let html = row('Email', d.email) + row('Domain', d.domain) + row('MX Records', d.mx_records?.length ? d.mx_records.map(m=>m.exchange||m).join('<br>') : '<span class="bad">None</span>');
  html += row('SPF', d.spf ? '<span class="ok">✓ Present</span>' : '<span class="bad">✗ Missing</span>');
  html += row('DMARC', d.dmarc ? '<span class="ok">✓ Present</span>' : '<span class="warn">✗ Missing</span>');
  html += row('DKIM', d.dkim_hint ? '<span class="ok">✓ Detected</span>' : '<span class="warn">Not detected</span>');
  html += row('Disposable', d.disposable ? '<span class="bad">Yes ⚠</span>' : '<span class="ok">No</span>');
  html += row('Free provider', d.free_provider ? '<span class="warn">Yes</span>' : 'No');
  html += row('Gravatar', d.gravatar ? `<a href="${esc(d.gravatar_profile||d.gravatar)}" target="_blank">✓ Has profile</a>` : 'Not found');
  html += row('Website', d.has_website ? `<a href="${esc(d.website_url)}" target="_blank">✓ ${esc(d.website_url)}</a>` : '<span class="bad">No website</span>');
  
  // Breach detection
  if (d.breach_info && d.breach_info.has_breaches) {
    const bi = d.breach_info;
    html += `<div class="breach-alert" style="margin-top:10px;padding:8px;border-radius:6px">
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px">
        <span class="tag tag-danger">${bi.risk_level?.toUpperCase() || 'RISK'}</span>
        <span class="tag tag-warning">Risk Score: ${bi.risk_score || 0}/100</span>
        <span class="tag tag-info">${bi.total_breaches || 0} Breaches</span>
      </div>
      <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:${bi.risk_score || 0}%"></div></div>
      <p style="margin:6px 0;font-size:.75rem">${esc(bi.message || 'Known breaches detected')}</p>`;
    if (bi.username_may_be_affected) html += `<div class="tag tag-warning">⚠️ Username/Email may be affected</div>`;
    if (bi.breaches?.length) {
      html += `<details style="margin-top:6px"><summary style="cursor:pointer;color:var(--cyan);font-size:.7rem">📋 View ${bi.breaches.length} breach(es)</summary><div style="margin-top:6px">`;
      bi.breaches.forEach(b => {
        html += `<div class="breach-detail"><strong>${esc(b.name)}</strong> (${b.year}) <span class="tag tag-${b.risk === 'critical' ? 'danger' : (b.risk === 'high' ? 'warning' : 'info')}" style="float:right">${b.risk?.toUpperCase() || 'UNKNOWN'}</span><br>📊 ${(b.records||0).toLocaleString()} records<br>📁 ${b.data_types?.join(', ') || 'N/A'}<br><small>${esc(b.description?.slice(0,120) || '')}</small></div>`;
      });
      html += `</div></details>`;
    }
    if (bi.recommendation) html += `<div class="recommendation-box"><strong>🔒 Recommendation:</strong><br>${esc(bi.recommendation)}</div>`;
    html += `</div>`;
  }
  return html;
}

function buildPhone(d) {
  let html = row('Input', d.input) + row('E.164', d.e164) + row('International', d.international) + row('National', d.national);
  html += row('Country', `${d.country||'?'} (${d.country_iso||'?'})`);
  html += row('Provider', d.provider||'Unknown') + row('Type', d.line_type||'Unknown') + row('Location', d.location||'—');
  html += row('Timezone', (d.timezones||[]).slice(0,2).join(', ')||'—');
  html += row('Mobile', d.is_mobile ? '<span class="ok">Yes</span>' : 'No');
  if (d.whatsapp_link) html += row('WhatsApp', `<a href="${esc(d.whatsapp_link)}" target="_blank">Open chat</a>`);
  if (d.possible_handles?.length) html += row('Handles', d.possible_handles.join(', '));
  return html;
}

function buildDomain(d) {
  let html = row('Domain', d.domain) + row('IPv4', (d.ip_addresses||[]).join(', ')||'<span class="bad">None</span>');
  html += row('IPv6', (d.ipv6_addresses||[]).slice(0,2).join(', ')||'—') + row('Nameservers', (d.nameservers||[]).join('<br>')||'—');
  html += row('MX', (d.mx_records||[]).map(m=>m.exchange||m).join('<br>')||'<span class="bad">None</span>');
  html += row('HTTP', d.http_status ? `<span class="${d.http_status===200?'ok':'warn'}">${d.http_status}</span>` : '—');
  html += row('HTTPS', d.https_status ? `<span class="${d.https_status===200?'ok':'warn'}">${d.https_status}</span>` : '—');
  html += row('Server', esc(d.server_header||'—')) + row('Title', esc((d.title||'—').slice(0,60)));
  if (d.technologies?.length) html += row('Tech stack', d.technologies.join(', '));
  if (d.security_headers) {
    const sh = d.security_headers;
    const flags = [sh.hsts?'<span class="ok">HSTS</span>':'<span class="bad">No HSTS</span>', sh.csp?'<span class="ok">CSP</span>':'<span class="bad">No CSP</span>', sh.xframe?'<span class="ok">X-Frame</span>':''].filter(Boolean).join(' ');
    if (flags) html += row('Security', flags);
  }
  return html;
}

function buildIP(d) {
  let html = row('IP', d.ip) + row('Version', `IPv${d.version}`) + row('Country', d.country ? `${d.country} (${d.country_code})` : '—');
  html += row('Region', d.region||'—') + row('City', d.city||'—') + row('ZIP', d.zip||'—');
  html += row('Coords', d.lat ? `${d.lat}, ${d.lon}` : '—') + row('Timezone', d.timezone||'—');
  html += row('ISP', d.isp||'—') + row('Org', d.org||'—') + row('ASN', d.asn ? `${d.asn} ${d.asn_name||''}` : '—');
  html += row('Reverse DNS', d.reverse_dns||'—');
  html += row('Proxy/VPN', d.is_proxy ? '<span class="bad">⚠ Detected</span>' : '<span class="ok">No</span>');
  html += row('Hosting', d.is_hosting ? '<span class="warn">Yes (datacenter)</span>' : 'No');
  html += row('Mobile', d.is_mobile ? '<span class="ok">Yes</span>' : 'No');
  if (d.rdap?.organization) html += row('RIR Org', esc(d.rdap.organization));
  if (d.rdap?.registered) html += row('Registered', d.rdap.registered);
  if (d.abuse_contact) html += row('Abuse', `<a href="mailto:${esc(d.abuse_contact)}">${esc(d.abuse_contact)}</a>`);
  return html;
}

function row(k, v) { return `<div class="row"><span class="rk">${k}</span><span class="rv">${v}</span></div>`; }
function esc(s) { if (!s) return ''; return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function showError(msg) { document.getElementById('results').innerHTML = `<div class="empty"><div class="empty-ic">⚠️</div><div class="empty-t" style="color:var(--red)">${esc(msg)}</div></div>`; }
function showToast(msg, dur=3500) { const t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'), dur); }
function addHistory(target, type) { history = history.filter(h=>h.target !== target); history.unshift({target, type, ts: Date.now()}); if (history.length > 30) history.pop(); localStorage.setItem('gi25_hist', JSON.stringify(history)); renderHistory(); }
function renderHistory() { const el = document.getElementById('histList'); if (!history.length) { el.innerHTML='<div style="padding:6px 4px;font-size:.75rem;color:var(--text3)">No history yet</div>'; return; } el.innerHTML = history.slice(0,20).map(h=>`<div class="hist-item" onclick="loadHistory('${esc(h.target)}','${esc(h.type)}')"><span class="hist-type">${esc(h.type||'?')}</span><span class="hist-target">${esc(h.target)}</span></div>`).join(''); }
function loadHistory(target, type) { document.getElementById('tin').value = target; document.querySelectorAll('.tab').forEach(t=>{ t.classList.remove('act'); if(t.dataset.t===type||type==='auto'){} }); doScan(); }
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
#  FLASK ROUTES
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return HTML


@app.route('/api/scan', methods=['POST'])
def api_scan():
    try:
        body = request.get_json(force=True)
        target = (body.get('target') or '').strip()
        scan_type = body.get('type', 'auto')
        deep = bool(body.get('deep', False))
        save_report = bool(body.get('report', False))

        if not target:
            return jsonify({'error': 'No target provided'}), 400

        from core.detector import detector as det
        entity = det.detect(target)
        detected_type = entity.type
        norm_target = entity.normalized

        use_type = scan_type if scan_type != 'auto' else detected_type

        results = run_async_scan(norm_target, use_type, deep)

        report_file = None
        if save_report and results:
            from reports.generator import ReportGenerator
            rg = ReportGenerator(output_dir='output')
            loop = asyncio.new_event_loop()
            try:
                fp = loop.run_until_complete(rg.save_html(results))
                report_file = str(fp)
            finally:
                loop.close()

        return jsonify({
            'target': norm_target,
            'detected_type': detected_type,
            'used_type': use_type,
            'results': make_serializable(results),
            'report_file': report_file,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect', methods=['POST'])
def api_detect():
    body = request.get_json(force=True)
    target = (body.get('target') or '').strip()
    if not target:
        return jsonify({'error': 'No target'}), 400
    entity = detector.detect(target)
    return jsonify({'type': entity.type, 'normalized': entity.normalized, 'confidence': entity.confidence})


@app.route('/api/health')
def api_health():
    return jsonify({'status': 'ok', 'version': '2.5.0', 'timestamp': datetime.now().isoformat()})


# ─────────────────────────────────────────────────────────────────────────────
#  ASYNC RUNNER
# ─────────────────────────────────────────────────────────────────────────────
def run_async_scan(target: str, target_type: str, deep: bool) -> dict:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_do_scan(target, target_type, deep))
    finally:
        loop.close()


async def _do_scan(target: str, target_type: str, deep: bool) -> dict:
    engine = GhostIntelEngine(timeout=12, max_concurrent=25)
    async with engine:
        if deep:
            return await engine.investigate_all(target, target_type)
        else:
            result = await engine.investigate(target, target_type)
            if result and not result.get('error'):
                return {target_type: result}
            return {}


def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(i) for i in obj]
    elif isinstance(obj, set):
        return sorted(list(obj))
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


def start_web_server(port: int = 7331, open_browser: bool = True):
    console.print(f"\n[bold cyan]🌐 GhostIntel Web UI starting...[/bold cyan]")
    console.print(f"[green]  → URL  : [bold]http://localhost:{port}[/bold][/green]")
    console.print(f"[dim]  → Press Ctrl+C to stop[/dim]\n")

    if open_browser:
        def _open():
            time.sleep(1.2)
            webbrowser.open(f'http://localhost:{port}')
        threading.Thread(target=_open, daemon=True).start()

    try:
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)
    except OSError as e:
        console.print(f"[red]❌ Port {port} in use. Try: python ghostintel.py -web --port 8080[/red]")
        sys.exit(1)


if __name__ == '__main__':
    start_web_server()