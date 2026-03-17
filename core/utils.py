#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Utility Functions
Help menus, version info, and common utilities
"""

from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box
from rich.text import Text
from rich.syntax import Syntax

from core.banner import console, show_banner

VERSION = "2.0.0"
AUTHOR = "Ruyynn"
GITHUB = "https://github.com/ruyynn"


def print_help():
    """Print comprehensive help menu"""
    show_banner()
    
    # Main help panel
    console.print(Panel.fit(
        "[bold cyan]GHOSTINTEL v2.0 - HELP & COMMANDS[/bold cyan]\n"
        "[dim]API-Less OSINT Mashup Engine • No Keys Required[/dim]",
        border_style="cyan"
    ))
    
    # Basic usage
    console.print("\n[bold yellow]📌 BASIC USAGE:[/bold yellow]")
    console.print("  [green]ghostintel investigate TARGET[/green]    # Auto-detect and investigate")
    console.print("  [green]ghostintel -u USERNAME[/green]           # Username investigation")
    console.print("  [green]ghostintel -e EMAIL[/green]              # Email investigation")
    console.print("  [green]ghostintel -p PHONE[/green]              # Phone investigation")
    console.print("  [green]ghostintel -d DOMAIN[/green]             # Domain investigation")
    console.print("  [green]ghostintel -i IP[/green]                 # IP investigation")
    
    # Phone examples (multi-country)
    console.print("\n[bold yellow]📱 PHONE INVESTIGATION (Multi-Country):[/bold yellow]")
    
    phone_table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    phone_table.add_column("Country", style="green")
    phone_table.add_column("Example", style="white")
    phone_table.add_column("Description", style="dim")
    
    phone_table.add_row("🇮🇩 Indonesia", "ghostintel -p 08123456789", "Detect provider, location")
    phone_table.add_row("🇺🇸 USA", "ghostintel -p +12125551234", "US number with area code")
    phone_table.add_row("🇬🇧 UK", "ghostintel -p +447700123456", "UK mobile number")
    phone_table.add_row("🇲🇾 Malaysia", "ghostintel -p +60123456789", "Malaysian mobile")
    phone_table.add_row("🇮🇳 India", "ghostintel -p +919876543210", "Indian mobile")
    
    console.print(phone_table)
    
    # Report generation
    console.print("\n[bold yellow]📊 REPORT GENERATION:[/bold yellow]")
    
    report_table = Table(show_header=True, header_style="bold yellow", box=box.ROUNDED)
    report_table.add_column("Command", style="green")
    report_table.add_column("Output", style="white")
    
    report_table.add_row("ghostintel investigate target --report", "Generate all reports")
    report_table.add_row("ghostintel -u user --format html -o report.html", "HTML report")
    report_table.add_row("ghostintel -d domain --format json -o data.json", "JSON report")
    report_table.add_row("ghostintel -p phone --format txt -o output.txt", "Text report")
    
    console.print(report_table)
    
    # Options
    console.print("\n[bold yellow]⚙️ OPTIONS:[/bold yellow]")
    
    options = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    options.add_column("Option", style="green")
    options.add_column("Description", style="white")
    
    options.add_row("-h, --help", "Show this help message")
    options.add_row("-v, --version", "Show version information")
    options.add_row("--report", "Generate comprehensive report")
    options.add_row("-o, --output FILE", "Save output to file")
    options.add_row("--format [json|html|txt]", "Output format")
    options.add_row("--timeout SECONDS", "Request timeout (default: 10)")
    options.add_row("--threads NUM", "Concurrent threads (default: 20)")
    options.add_row("--no-color", "Disable colored output")
    
    console.print(options)
    
    # Examples
    console.print("\n[bold green]🚀 REAL EXAMPLES:[/bold green]")
    
    examples = [
        ("[dim]# Quick username check[/dim]", "ghostintel -u asep"),
        ("[dim]# Phone investigation with report[/dim]", "ghostintel -p +62812345678 --report --format html"),
        ("[dim]# Domain recon[/dim]", "ghostintel -d example.com"),
        ("[dim]# Email investigation[/dim]", "ghostintel -e user@example.com"),
        ("[dim]# IP geolocation[/dim]", "ghostintel -i 8.8.8.8"),
        ("[dim]# Save JSON output[/dim]", "ghostintel investigate target -o results.json"),
    ]
    
    for desc, cmd in examples:
        console.print(desc)
        console.print(f"  [cyan]{cmd}[/cyan]\n")
    
    # Legal notice
    console.print(Panel(
        "[yellow]⚠️ LEGAL DISCLAIMER[/yellow]\n\n"
        "GhostIntel is designed for educational purposes and authorized security testing only.\n"
        "Only investigate targets you own or have explicit permission to test.\n"
        "The user is solely responsible for compliance with all applicable laws.",
        border_style="red",
        box=box.HEAVY
    ))


def print_version():
    """Print version information"""
    console.print(f"[bold cyan]GhostIntel v{VERSION}[/bold cyan]")
    console.print(f"[dim]Author: {AUTHOR}[/dim]")
    console.print(f"[dim]GitHub: {GITHUB}[/dim]")
    console.print("[dim]OSINT Mashup Engine • No API Keys Required[/dim]")


def sanitize_filename(text: str) -> str:
    """Sanitize string for use as filename"""
    import re
    return re.sub(r'[^\w\-_\. ]', '_', text)


def parse_timeout(timeout_str: str) -> int:
    """Parse timeout string to seconds"""
    try:
        return int(timeout_str)
    except:
        return 10