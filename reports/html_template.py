#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - HTML Report Template
Beautiful, responsive HTML template with full CSS and JavaScript
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GhostIntel Report - {{ target }}</title>
    <style>
        /* ===== RESET & VARIABLES ===== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            /* Dark theme (default) */
            --bg-primary: #0a0c0f;
            --bg-secondary: #14181c;
            --bg-tertiary: #1e2329;
            --bg-hover: #252d36;
            --text-primary: #e6e9ef;
            --text-secondary: #9aa3b4;
            --text-muted: #6b7485;
            --accent-cyan: #2dd4bf;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
            --accent-purple: #a78bfa;
            --accent-blue: #3b82f6;
            --border-color: #2a3038;
            --border-light: #333b44;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }

        /* Light theme */
        .light-theme {
            --bg-primary: #f3f4f6;
            --bg-secondary: #ffffff;
            --bg-tertiary: #f9fafb;
            --bg-hover: #e5e7eb;
            --text-primary: #111827;
            --text-secondary: #4b5563;
            --text-muted: #6b7280;
            --border-color: #e5e7eb;
            --border-light: #d1d5db;
            --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        /* ===== BASE STYLES ===== */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* ===== TYPOGRAPHY ===== */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            line-height: 1.3;
            color: var(--text-primary);
        }

        h1 { font-size: 2.5rem; }
        h2 { font-size: 2rem; }
        h3 { font-size: 1.5rem; }
        h4 { font-size: 1.25rem; }

        a {
            color: var(--accent-cyan);
            text-decoration: none;
            transition: color 0.2s;
        }

        a:hover {
            color: var(--accent-green);
            text-decoration: underline;
        }

        /* ===== HEADER SECTION ===== */
        .header {
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
            border-radius: 1.5rem;
            padding: 2.5rem;
            margin-bottom: 2rem;
            border: 1px solid var(--border-color);
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow);
        }

        .header::before {
            content: '👻';
            position: absolute;
            right: 2rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 10rem;
            opacity: 0.05;
            pointer-events: none;
            z-index: 0;
        }

        .header-content {
            position: relative;
            z-index: 1;
        }

        .header-title {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }

        .header-title h1 {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            font-size: 3rem;
        }

        .header-badge {
            background: var(--accent-green);
            color: white;
            padding: 0.25rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: var(--shadow-sm);
        }

        .header-meta {
            color: var(--text-secondary);
            font-size: 1rem;
            margin-top: 1rem;
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .meta-item strong {
            color: var(--accent-cyan);
            font-weight: 600;
        }

        /* ===== THEME TOGGLE ===== */
        .theme-toggle {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 2rem;
            padding: 0.25rem;
            display: flex;
            gap: 0.25rem;
            z-index: 10;
        }

        .theme-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            cursor: pointer;
            font-size: 0.875rem;
            transition: all 0.2s;
        }

        .theme-btn.active {
            background: var(--accent-cyan);
            color: white;
        }

        /* ===== STATS GRID ===== */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .stat-card {
            background: var(--bg-tertiary);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            transition: transform 0.2s, border-color 0.2s;
            box-shadow: var(--shadow-sm);
        }

        .stat-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-cyan);
        }

        .stat-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 0.25rem;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* ===== MODULE CARDS ===== */
        .module-card {
            background: var(--bg-secondary);
            border-radius: 1rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: all 0.3s;
        }

        .module-card:hover {
            border-color: var(--accent-cyan);
            box-shadow: 0 15px 30px -10px rgba(45, 212, 191, 0.2);
        }

        .module-header {
            padding: 1.25rem 1.5rem;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            transition: background 0.2s;
        }

        .module-header:hover {
            background: var(--bg-hover);
        }

        .module-title {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .module-title h3 {
            margin: 0;
            font-size: 1.25rem;
            color: var(--accent-cyan);
        }

        .module-icon {
            font-size: 1.5rem;
        }

        .module-badge {
            background: var(--accent-purple);
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 1rem;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .module-content {
            padding: 1.5rem;
            display: none;
        }

        .module-content.active {
            display: block;
        }

        .toggle-btn {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 1.2rem;
            transition: transform 0.3s;
            width: 2rem;
            height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }

        .toggle-btn:hover {
            background: var(--bg-hover);
            color: var(--accent-cyan);
        }

        /* ===== DATA GRID ===== */
        .data-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }

        .data-item {
            background: var(--bg-tertiary);
            border-radius: 0.75rem;
            padding: 1rem;
            border: 1px solid var(--border-color);
            transition: border-color 0.2s;
        }

        .data-item:hover {
            border-color: var(--accent-cyan);
        }

        .data-label {
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .data-value {
            color: var(--text-primary);
            font-size: 1rem;
            font-weight: 500;
            word-break: break-word;
        }

        .data-value.success { color: var(--success); }
        .data-value.warning { color: var(--warning); }
        .data-value.danger { color: var(--danger); }
        .data-value.info { color: var(--info); }

        /* ===== LISTS ===== */
        .list {
            list-style: none;
            margin-top: 0.5rem;
        }

        .list li {
            padding: 0.5rem 0.75rem;
            background: var(--bg-secondary);
            border-radius: 0.5rem;
            margin-bottom: 0.25rem;
            border-left: 3px solid var(--accent-cyan);
            word-break: break-word;
            font-size: 0.875rem;
            transition: transform 0.2s;
        }

        .list li:hover {
            transform: translateX(5px);
            background: var(--bg-hover);
        }

        .list li a {
            color: var(--accent-cyan);
            text-decoration: none;
            display: block;
        }

        .list li a:hover {
            text-decoration: underline;
        }

        /* ===== TABLES ===== */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
            background: var(--bg-tertiary);
            border-radius: 0.5rem;
            overflow: hidden;
        }

        .data-table th {
            text-align: left;
            padding: 0.75rem;
            background: var(--bg-hover);
            color: var(--text-secondary);
            font-weight: 600;
            border-bottom: 2px solid var(--border-color);
        }

        .data-table td {
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }

        .data-table tr:hover {
            background: var(--bg-hover);
        }

        /* ===== CORRELATION TREE ===== */
        .correlation-tree {
            background: var(--bg-tertiary);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-top: 1rem;
            border: 1px solid var(--border-color);
        }

        .tree-node {
            margin-left: 1.5rem;
            position: relative;
        }

        .tree-root {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--accent-cyan);
            margin-bottom: 1rem;
            padding-left: 1.5rem;
            position: relative;
        }

        .tree-root::before {
            content: '🔗';
            position: absolute;
            left: -0.5rem;
            top: 0;
        }

        .tree-branch {
            margin: 0.75rem 0;
            padding-left: 1.5rem;
            border-left: 2px solid var(--border-color);
        }

        .tree-leaf {
            padding: 0.25rem 0;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .tree-leaf::before {
            content: '↳';
            color: var(--accent-cyan);
            font-weight: bold;
        }

        .tree-leaf strong {
            color: var(--accent-green);
            min-width: 80px;
        }

        /* ===== TAGS/CHIPS ===== */
        .tag {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 2rem;
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin: 0.25rem;
        }

        .tag.success {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            border-color: var(--success);
        }

        .tag.warning {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
            border-color: var(--warning);
        }

        .tag.danger {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border-color: var(--danger);
        }

        /* ===== PROGRESS BARS ===== */
        .progress {
            background: var(--bg-hover);
            border-radius: 1rem;
            height: 0.5rem;
            overflow: hidden;
            margin: 0.5rem 0;
        }

        .progress-bar {
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green));
            height: 100%;
            border-radius: 1rem;
            transition: width 0.3s;
        }

        /* ===== SEARCH BOX ===== */
        .search-box {
            margin-bottom: 1.5rem;
            position: relative;
        }

        .search-input {
            width: 100%;
            padding: 1rem 1rem 1rem 3rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 2rem;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(45, 212, 191, 0.2);
        }

        .search-icon {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
        }

        /* ===== EXPORT BUTTONS ===== */
        .export-buttons {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .export-btn {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            cursor: pointer;
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
        }

        .export-btn:hover {
            background: var(--accent-cyan);
            color: white;
            border-color: var(--accent-cyan);
        }

        /* ===== SOURCES SECTION ===== */
        .sources {
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .sources span {
            color: var(--accent-cyan);
            font-weight: 600;
        }

        .source-badge {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            padding: 0.2rem 0.5rem;
            border-radius: 1rem;
            font-size: 0.7rem;
        }

        /* ===== TIMESTAMP ===== */
        .timestamp {
            font-family: monospace;
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }

        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 2rem;
            color: var(--text-secondary);
            font-size: 0.8rem;
            border-top: 1px solid var(--border-color);
            background: var(--bg-secondary);
            border-radius: 1rem;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
        }

        .footer-links a {
            color: var(--text-muted);
            font-size: 0.8rem;
        }

        /* ===== LOADING ANIMATION ===== */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .loading {
            animation: pulse 1.5s ease-in-out infinite;
            text-align: center;
            padding: 2rem;
        }

        /* ===== TOOLTIPS ===== */
        [data-tooltip] {
            position: relative;
            cursor: help;
        }

        [data-tooltip]:before {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            padding: 0.5rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            font-size: 0.75rem;
            white-space: nowrap;
            display: none;
            z-index: 1000;
            color: var(--text-primary);
            box-shadow: var(--shadow);
        }

        [data-tooltip]:hover:before {
            display: block;
        }

        /* ===== RESPONSIVE DESIGN ===== */
        @media (max-width: 1024px) {
            .container { padding: 1.5rem; }
            h1 { font-size: 2rem; }
        }

        @media (max-width: 768px) {
            .container { padding: 1rem; }
            .header { padding: 1.5rem; }
            .header::before { font-size: 6rem; }
            .stats-grid { grid-template-columns: 1fr; }
            .data-grid { grid-template-columns: 1fr; }
            .header-meta { flex-direction: column; gap: 0.5rem; }
            .theme-toggle { position: static; margin-bottom: 1rem; }
        }

        @media (max-width: 480px) {
            h1 { font-size: 1.5rem; }
            .header-title { flex-direction: column; align-items: flex-start; }
            .export-buttons { flex-direction: column; }
            .export-btn { width: 100%; justify-content: center; }
        }

        /* ===== PRINT STYLES ===== */
        @media print {
            body {
                background: white;
                color: black;
            }
            
            .theme-toggle,
            .export-buttons,
            .toggle-btn {
                display: none;
            }
            
            .module-card {
                break-inside: avoid;
                border: 1px solid #ddd;
            }
            
            .header::before {
                opacity: 0.1;
            }
        }

        /* ===== CUSTOM SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-cyan);
        }
    </style>
</head>
<body>
    <!-- Theme Toggle -->
    <div class="theme-toggle">
        <button class="theme-btn active" onclick="setTheme('dark')">🌙 Dark</button>
        <button class="theme-btn" onclick="setTheme('light')">☀️ Light</button>
    </div>

    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-content">
                <div class="header-title">
                    <h1>👻 GhostIntel Report</h1>
                    <span class="header-badge">v2.0</span>
                </div>
                
                <div class="header-meta">
                    <div class="meta-item">
                        <span>🎯 Target:</span>
                        <strong>{{ target }}</strong>
                    </div>
                    <div class="meta-item">
                        <span>📅 Generated:</span>
                        <strong>{{ timestamp }}</strong>
                    </div>
                    <div class="meta-item">
                        <span>📊 Modules:</span>
                        <strong>{{ total_modules }}</strong>
                    </div>
                </div>
            </div>
        </div>

        <!-- Export Buttons -->
        <div class="export-buttons">
            <button class="export-btn" onclick="exportJSON()">
                <span>📋</span> Export JSON
            </button>
            <button class="export-btn" onclick="exportMarkdown()">
                <span>📝</span> Export Markdown
            </button>
            <button class="export-btn" onclick="window.print()">
                <span>🖨️</span> Print / PDF
            </button>
        </div>

        <!-- Search Box -->
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" class="search-input" placeholder="Search in report..." onkeyup="searchReport(this.value)">
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📦</div>
                <div class="stat-value">{{ total_modules }}</div>
                <div class="stat-label">Modules Run</div>
            </div>
            {% if correlation and correlation.summary %}
                {% for etype, count in correlation.summary.items() %}
                <div class="stat-card">
                    <div class="stat-icon">
                        {% if etype == 'username' %}👤
                        {% elif etype == 'email' %}📧
                        {% elif etype == 'phone' %}📱
                        {% elif etype == 'domain' %}🌐
                        {% elif etype == 'ip' %}🌍
                        {% else %}🔍
                        {% endif %}
                    </div>
                    <div class="stat-value">{{ count }}</div>
                    <div class="stat-label">{{ etype|title }} Found</div>
                </div>
                {% endfor %}
            {% endif %}
        </div>

        <!-- Modules -->
        {% for name, module in modules.items() %}
        <div class="module-card" data-module="{{ name }}">
            <div class="module-header" onclick="toggleModule(this)">
                <div class="module-title">
                    <span class="module-icon">
                        {% if name == 'username' %}👤
                        {% elif name == 'email' %}📧
                        {% elif name == 'phone' %}📱
                        {% elif name == 'domain' %}🌐
                        {% elif name == 'ip' %}🌍
                        {% else %}📦
                        {% endif %}
                    </span>
                    <h3>{{ name.upper() }}</h3>
                    {% if module.data %}
                        {% if module.data.valid is defined %}
                            <span class="module-badge {{ 'success' if module.data.valid else 'danger' }}">
                                {{ '✓ Valid' if module.data.valid else '✗ Invalid' }}
                            </span>
                        {% endif %}
                    {% endif %}
                </div>
                <span class="toggle-btn">▼</span>
            </div>
            <div class="module-content">
                <div class="data-grid">
                    {% for key, value in module.data.items() if not key.startswith('_') and key not in ['timestamp'] %}
                    <div class="data-item" data-label="{{ key }}">
                        <div class="data-label" data-tooltip="{{ key|replace('_', ' ')|title }}">
                            {{ key|replace('_', ' ')|title }}
                        </div>
                        <div class="data-value 
                            {%- if key in ['valid', 'has_website', 'is_mobile'] %} 
                                {%- if value %} success{% else %} danger{% endif %}
                            {%- elif key in ['spam_score', 'risk_score'] %}
                                {%- if value > 70 %} danger
                                {%- elif value > 40 %} warning
                                {%- else %} success
                                {%- endif %}
                            {%- endif %}">
                            
                            {% if value is string %}
                                {% if value.startswith('http') %}
                                    <a href="{{ value }}" target="_blank">{{ value|truncate(60) }}</a>
                                {% else %}
                                    {{ value }}
                                {% endif %}
                                
                            {% elif value is number %}
                                {{ value }}
                                
                            {% elif value is boolean %}
                                <span class="tag {{ 'success' if value else 'danger' }}">
                                    {{ '✓ Yes' if value else '✗ No' }}
                                </span>
                                
                            {% elif value is iterable and value is not string %}
                                {% if value|length > 0 %}
                                    <ul class="list">
                                    {% for item in value %}
                                        <li>
                                        {% if item is mapping %}
                                            {% if item.platform %}
                                                <strong>{{ item.platform }}:</strong>
                                                <a href="{{ item.url }}" target="_blank">{{ item.url|truncate(50) }}</a>
                                                {% if item.profile_name %}
                                                    <br><small>📝 {{ item.profile_name }}</small>
                                                {% endif %}
                                                
                                            {% elif item.exchange %}
                                                <strong>{{ item.exchange }}</strong>
                                                <small>(priority: {{ item.priority }})</small>
                                                
                                            {% elif item.ip_addresses %}
                                                <strong>{{ item.subdomain }}</strong>
                                                <br><small>IPs: {{ item.ip_addresses|join(', ') }}</small>
                                                
                                            {% else %}
                                                {{ item }}
                                            {% endif %}
                                            
                                        {% elif item is string and item.startswith('http') %}
                                            <a href="{{ item }}" target="_blank">{{ item|truncate(50) }}</a>
                                            
                                        {% else %}
                                            {{ item }}
                                        {% endif %}
                                        </li>
                                    {% endfor %}
                                    </ul>
                                {% else %}
                                    <span class="tag">None</span>
                                {% endif %}
                                
                            {% else %}
                                {{ value }}
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                {% if module.sources %}
                <div class="sources">
                    <span>🔍 Sources:</span>
                    {% for source in module.sources %}
                    <span class="source-badge">{{ source }}</span>
                    {% endfor %}
                </div>
                {% endif %}
                
                {% if module.data.timestamp %}
                <div class="timestamp">
                    ⏱️ Last updated: {{ module.data.timestamp }}
                </div>
                {% endif %}
            </div>
        </div>
        {% endfor %}

        <!-- Correlation -->
{% if correlation and correlation.entities %}
<div class="module-card">
    <div class="module-header" onclick="toggleModule(this)">
        <div class="module-title">
            <span class="module-icon">🔗</span>
            <h3>INTELLIGENCE CORRELATION</h3>
        </div>
        <span class="toggle-btn">▼</span>
    </div>
    <div class="module-content">
        <div class="correlation-tree">
            <div class="tree-root">{{ correlation.primary }}</div>
            
            {% for etype, entities in correlation.entities.items() %}
                {% if entities %}
                <div class="tree-branch">
                    <div class="tree-leaf">
                        <strong>{{ etype|upper }}</strong>
                    </div>
                    {% for entity in entities %}
                    <div class="tree-leaf">
                        <span>{{ entity }}</span>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}
                    {% endfor %}
                </div>

                {% if correlation.connections %}
                <div style="margin-top: 2rem;">
                    <h4 style="color: var(--accent-yellow);">🔗 Connections</h4>
                    <div class="data-grid">
                        {% for conn in correlation.connections %}
                        <div class="data-item">
                            <div class="data-label">Connection</div>
                            <div class="data-value">{{ conn }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
            </div>
        </div>
        {% endif %}

        <!-- Footer -->
        <div class="footer">
            <div>👻 GhostIntel v2.0 - OSINT Mashup Engine</div>
            <div class="footer-links">
                <a href="https://github.com/ruyynn/GhostIntel" target="_blank">GitHub</a>
                <a href="#" onclick="window.print()">Print Report</a>
                <a href="#" onclick="scrollToTop()">Back to Top</a>
            </div>
            <div style="margin-top: 1rem; font-size: 0.7rem;">
                ⚠️ For Educational Purposes Only • No API Keys Required
            </div>
        </div>
    </div>

    <script>
        // ===== MODULE TOGGLE =====
        function toggleModule(header) {
            const content = header.nextElementSibling;
            const btn = header.querySelector('.toggle-btn');
            
            if (content.style.display === 'none' || !content.style.display) {
                content.style.display = 'block';
                btn.textContent = '▲';
                btn.style.transform = 'rotate(0deg)';
            } else {
                content.style.display = 'none';
                btn.textContent = '▼';
                btn.style.transform = 'rotate(0deg)';
            }
        }

        // ===== THEME TOGGLE =====
        function setTheme(theme) {
            const body = document.body;
            const darkBtn = document.querySelector('.theme-btn:first-child');
            const lightBtn = document.querySelector('.theme-btn:last-child');
            
            if (theme === 'dark') {
                body.classList.remove('light-theme');
                darkBtn.classList.add('active');
                lightBtn.classList.remove('active');
                localStorage.setItem('ghostintel-theme', 'dark');
            } else {
                body.classList.add('light-theme');
                lightBtn.classList.add('active');
                darkBtn.classList.remove('active');
                localStorage.setItem('ghostintel-theme', 'light');
            }
        }

        // Load saved theme
        const savedTheme = localStorage.getItem('ghostintel-theme');
        if (savedTheme === 'light') {
            setTheme('light');
        }

        // ===== SEARCH FUNCTION =====
        function searchReport(query) {
            query = query.toLowerCase();
            const modules = document.querySelectorAll('.module-card');
            
            modules.forEach(module => {
                const content = module.querySelector('.module-content');
                const text = content.textContent.toLowerCase();
                
                if (text.includes(query) || query === '') {
                    module.style.display = 'block';
                    
                    // Highlight matching text
                    if (query !== '') {
                        highlightText(content, query);
                    }
                } else {
                    module.style.display = 'none';
                }
            });
        }

        function highlightText(element, query) {
            // Simple highlight - in production, use a proper highlighting library
            const html = element.innerHTML;
            const regex = new RegExp(`(${query})`, 'gi');
            element.innerHTML = html.replace(regex, '<mark style="background: var(--accent-yellow); color: black;">$1</mark>');
        }

        // ===== EXPORT FUNCTIONS =====
        function exportJSON() {
            const data = {
                target: {{ target|tojson }},
                generated: {{ timestamp|tojson }},
                modules: {{ modules|tojson }}
            };
            
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ghostintel-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function exportMarkdown() {
            let markdown = `# GhostIntel Report - {{ target }}\n\n`;
            markdown += `Generated: {{ timestamp }}\n\n`;
            
            {% for name, module in modules.items() %}
            markdown += `## {{ name|upper }}\n\n`;
            {% for key, value in module.data.items() if not key.startswith('_') %}
            markdown += `- **{{ key|replace('_', ' ')|title }}**: ${JSON.stringify({{ value|tojson }})}\n`;
            {% endfor %}
            markdown += `\n`;
            {% endfor %}
            
            const blob = new Blob([markdown], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ghostintel-${Date.now()}.md`;
            a.click();
            URL.revokeObjectURL(url);
        }

        // ===== SCROLL TO TOP =====
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // ===== INITIALIZATION =====
        document.addEventListener('DOMContentLoaded', function() {
            // Auto-expand first module
            const firstModule = document.querySelector('.module-content');
            if (firstModule) {
                firstModule.style.display = 'block';
                const firstBtn = firstModule.previousElementSibling.querySelector('.toggle-btn');
                if (firstBtn) firstBtn.textContent = '▲';
            }
            
            // Add tooltips to all data items
            const dataItems = document.querySelectorAll('[data-tooltip]');
            dataItems.forEach(item => {
                item.addEventListener('mouseenter', function(e) {
                    // Tooltip handled by CSS
                });
            });
            
            // Add copy buttons to code blocks
            const codeBlocks = document.querySelectorAll('.data-value');
            codeBlocks.forEach(block => {
                if (block.textContent.length > 100) {
                    const copyBtn = document.createElement('button');
                    copyBtn.innerHTML = '📋 Copy';
                    copyBtn.className = 'export-btn';
                    copyBtn.style.marginTop = '0.5rem';
                    copyBtn.onclick = function() {
                        navigator.clipboard.writeText(block.textContent);
                        copyBtn.innerHTML = '✅ Copied!';
                        setTimeout(() => {
                            copyBtn.innerHTML = '📋 Copy';
                        }, 2000);
                    };
                    block.appendChild(copyBtn);
                }
            });
        });

        // ===== KEYBOARD SHORTCUTS =====
        document.addEventListener('keydown', function(e) {
            // Ctrl+F for search
            if (e.ctrlKey && e.key === 'f') {
                e.preventDefault();
                document.querySelector('.search-input').focus();
            }
            
            // Esc to clear search
            if (e.key === 'Escape') {
                document.querySelector('.search-input').value = '';
                searchReport('');
            }
            
            // Ctrl+P to print
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                window.print();
            }
        });

        // ===== LAZY LOADING =====
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        });

        document.querySelectorAll('.module-card').forEach(card => {
            observer.observe(card);
        });

        // ===== ERROR HANDLING =====
        window.onerror = function(msg, url, lineNo, columnNo, error) {
            console.error('Report Error:', msg);
            // Don't show to user, just log
            return true;
        };
    </script>
</body>
</html>
"""