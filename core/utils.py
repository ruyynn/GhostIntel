#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Utils
Enhanced with new features, batch processing help, and better formatting
"""

from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.columns import Columns
from rich.text import Text
from core.banner import console, show_banner

VERSION = "2.5.0"
AUTHOR = "Ruyynn"
GITHUB = "https://github.com/ruyynn"


def print_help():
    """Print comprehensive help menu"""
    show_banner()
    
    console.print(Panel.fit(
        "[bold cyan]GHOSTINTEL v2.5  —  ADVANCED OSINT FRAMEWORK[/bold cyan]\n"
        "[dim]No API Keys • Public Sources Only • Ethical Use[/dim]",
        border_style="cyan"
    ))

    # ==================== BASIC USAGE ====================
    console.print("\n[bold yellow]📌 BASIC USAGE:[/bold yellow]")
    basic_commands = [
        ("python ghostintel.py -u USERNAME",    "Username investigation (120+ platforms)"),
        ("python ghostintel.py -e EMAIL",       "Email + DNS + breach analysis"),
        ("python ghostintel.py -p PHONE",       "Phone number OSINT (ID/US/UK/MY/IN/AU/SG/PH)"),
        ("python ghostintel.py -d DOMAIN",      "Domain recon (DNS/HTTP/TLS/tech detection)"),
        ("python ghostintel.py -i IP",          "IP geolocation + RDAP + ASN + risk score"),
        ("python ghostintel.py -web",           "Launch web UI on localhost:7331"),
        ("python ghostintel.py -web --port 8080","Custom web UI port"),
    ]
    for cmd, desc in basic_commands:
        console.print(f"  [green]{cmd:<45}[/green] [dim]{desc}[/dim]")

    # ==================== ADVANCED OPTIONS ====================
    console.print("\n[bold yellow]⚡ ADVANCED OPTIONS:[/bold yellow]")
    advanced_commands = [
        ("--deep",                              "Deep investigation (run all relevant modules)"),
        ("--batch targets.txt",                 "Batch scan multiple targets from file"),
        ("--batch-delay 2",                     "Delay between batch scans (seconds)"),
        ("--output-dir ./reports",              "Custom output directory"),
        ("--quiet",                             "Suppress output (only save report)"),
        ("--debug",                             "Enable debug output"),
        ("--timeout 30",                        "Custom request timeout"),
        ("--threads 50",                        "Concurrent threads"),
    ]
    for cmd, desc in advanced_commands:
        console.print(f"  [cyan]{cmd:<45}[/cyan] [dim]{desc}[/dim]")

    # ==================== REPORT FORMATS ====================
    console.print("\n[bold yellow]📊 REPORT FORMATS:[/bold yellow]")
    report_commands = [
        ("... --report",                        "Generate report (JSON default)"),
        ("... --format json",                   "JSON format (machine readable)"),
        ("... --format html",                   "HTML report (interactive)"),
        ("... --format txt",                    "Plain text report"),
        ("... --format md",                     "Markdown report"),
        ("... --format all",                    "Generate all formats at once"),
        ("... --compress",                      "Compress JSON output (gzip)"),
        ("... -o report.html",                  "Specify output filename"),
    ]
    for cmd, desc in report_commands:
        console.print(f"  [green]{cmd:<45}[/green] [dim]{desc}[/dim]")

    # ==================== BATCH PROCESSING ====================
    console.print("\n[bold yellow]📦 BATCH PROCESSING:[/bold yellow]")
    console.print("  [cyan]Create a file with one target per line:[/cyan]")
    console.print("  [dim]  targets.txt:[/dim]")
    console.print("  [dim]    user1[/dim]")
    console.print("  [dim]    user2@gmail.com[/dim]")
    console.print("  [dim]    08123456789[/dim]")
    console.print("  [dim]    example.com[/dim]")
    console.print("")
    console.print("  [green]python ghostintel.py --batch targets.txt --format all --output-dir ./reports[/green]")

    # ==================== PHONE EXAMPLES (8 COUNTRIES) ====================
    console.print("\n[bold yellow]📱 PHONE OSINT — 8 COUNTRIES:[/bold yellow]")
    
    phone_table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    phone_table.add_column("Country", style="green")
    phone_table.add_column("Code", style="yellow")
    phone_table.add_column("Example", style="white")
    phone_table.add_column("Providers", style="dim")
    
    phone_data = [
        ("🇮🇩 Indonesia", "+62", "python ghostintel.py -p 08123456789", "Telkomsel, Indosat, XL, Three, Smartfren"),
        ("🇺🇸 USA", "+1", "python ghostintel.py -p +12125551234", "AT&T, Verizon, T-Mobile"),
        ("🇬🇧 UK", "+44", "python ghostintel.py -p +447700123456", "EE, O2, Vodafone, Three"),
        ("🇲🇾 Malaysia", "+60", "python ghostintel.py -p +60123456789", "Maxis, Celcom, DiGi, U Mobile"),
        ("🇮🇳 India", "+91", "python ghostintel.py -p +919876543210", "Airtel, Vi, Jio, BSNL"),
        ("🇦🇺 Australia", "+61", "python ghostintel.py -p +61412345678", "Telstra, Optus, Vodafone"),
        ("🇸🇬 Singapore", "+65", "python ghostintel.py -p +6581234567", "Singtel, StarHub, M1, SIMBA"),
        ("🇵🇭 Philippines", "+63", "python ghostintel.py -p +639171234567", "Globe, Smart, DITO"),
    ]
    
    for row in phone_data:
        phone_table.add_row(*row)
    
    console.print(phone_table)

    # ==================== EXAMPLES ====================
    console.print("\n[bold green]🚀 REAL-WORLD EXAMPLES:[/bold green]")
    
    examples = [
        ("[dim]# Username investigation[/dim]", "python ghostintel.py -u ruyynn"),
        ("[dim]# Email with breach detection[/dim]", "python ghostintel.py -e user@gmail.com --report --format html"),
        ("[dim]# Phone number (Indonesia)[/dim]", "python ghostintel.py -p 08123456789 --deep"),
        ("[dim]# Domain recon with tech detection[/dim]", "python ghostintel.py -d example.com --format all"),
        ("[dim]# IP with risk score[/dim]", "python ghostintel.py -i 8.8.8.8 --report"),
        ("[dim]# Batch scan 100 targets[/dim]", "python ghostintel.py --batch targets.txt --deep --format json"),
        ("[dim]# Generate all report formats[/dim]", "python ghostintel.py -u asep --format all -o asep_report"),
        ("[dim]# Quiet mode (no terminal output)[/dim]", "python ghostintel.py -d example.com --report --quiet"),
    ]
    
    for desc, cmd in examples:
        console.print(desc)
        console.print(f"  [cyan]{cmd}[/cyan]")

    # ==================== FEATURE HIGHLIGHTS ====================
    console.print("\n[bold magenta]✨ NEW IN v2.5:[/bold magenta]")
    features = Columns([
        "🌐 Web UI - Localhost dashboard",
        "📱 8 Countries - Phone OSINT expanded",
        "🔗 Breach Detection - Email risk scoring",
        "📦 Batch Processing - Scan multiple targets",
        "📄 Markdown Reports - New format",
        "🗜️ JSON Compression - Save space",
        "🛡️ DNSSEC Check - Domain security",
        "🔒 SSL/TLS Info - Certificate details",
    ], equal=False, expand=False)
    console.print(features)

    # ==================== LEGAL DISCLAIMER ====================
    console.print(Panel(
        "[yellow]⚠️  LEGAL DISCLAIMER[/yellow]\n\n"
        "GhostIntel is designed for educational purposes and authorized security testing only.\n"
        "• Only investigate targets you own or have explicit permission to test\n"
        "• All data collected is from public sources (DNS, RDAP, public websites)\n"
        "• Do not use for doxing, stalking, or any illegal activities\n\n"
        "[dim]By using this tool, you acknowledge that you are solely responsible for compliance with all applicable laws.[/dim]",
        border_style="red",
        box=box.HEAVY,
        padding=(1, 2)
    ))

    # ==================== FOOTER ====================
    console.print(f"\n[dim]💡 Need help? Visit [cyan]{GITHUB}[/cyan] • Report issues at GitHub Issues[/dim]")
    console.print(f"[dim]📧 Contact: [cyan]ruyynn25@gmail.com[/cyan] • ⭐ Star the repo if you find it useful![/dim]")


def print_version():
    """Print version information"""
    console.print(f"\n[bold cyan]👻 GhostIntel v{VERSION}[/bold cyan]")
    console.print(f"[dim]   Author: {AUTHOR}[/dim]")
    console.print(f"[dim]   GitHub: {GITHUB}[/dim]")
    console.print(f"[dim]   License: MIT[/dim]")
    console.print(f"[dim]   Python: {__import__('sys').version.split()[0]}[/dim]")
    console.print()
    console.print("[green]✨ Features:[/green]")
    console.print("  • 120+ Username Platforms")
    console.print("  • 8 Country Phone OSINT")
    console.print("  • Email Breach Detection")
    console.print("  • Domain Tech Stack Detection")
    console.print("  • IP Risk Scoring")
    console.print("  • Web UI Dashboard")
    console.print("  • Batch Processing")
    console.print("  • Multi-format Reports (JSON/HTML/TXT/MD)")


def sanitize_filename(text: str) -> str:
    """Sanitize string for use as filename"""
    import re
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)
    # Replace spaces with underscore
    sanitized = sanitized.replace(' ', '_')
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    return sanitized.strip('_')


def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def parse_timeout(timeout_str: str) -> int:
    """Parse timeout string to seconds"""
    try:
        return int(timeout_str)
    except ValueError:
        return 12


def print_banner_small():
    """Print a small banner (for web UI or quick display)"""
    console.print("[bold magenta]GHOST[cyan]INTEL[/cyan][/bold magenta] [dim]v2.5[/dim]")


def get_version_info() -> dict:
    """Get version information as dict"""
    return {
        'version': VERSION,
        'author': AUTHOR,
        'github': GITHUB,
        'python': __import__('sys').version.split()[0],
        'features': [
            'Username OSINT (120+ platforms)',
            'Email OSINT with breach detection',
            'Phone OSINT (8 countries)',
            'Domain OSINT with tech detection',
            'IP OSINT with risk scoring',
            'Web UI',
            'Batch processing',
            'Multi-format reports'
        ]
    }