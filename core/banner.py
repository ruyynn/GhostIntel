#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Banner"""

import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, TextColumn

custom_theme = Theme({
    "info":      "dim cyan",
    "warning":   "yellow",
    "danger":    "bold red",
    "success":   "bold green",
    "ghost":     "bold magenta",
    "highlight": "bold blue",
    "dim":       "dim white",
    "accent":    "bold cyan",
})

console = Console(theme=custom_theme)

# ASCII Art Banner - Clean and readable
BANNER = r"""
       ▄████  ██░ ██  ▒█████   ██████ ▄▄▄█████▓
      ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
     ▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
     ░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░
     ░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░
      ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░
       ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░
     ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░
           ░  ░  ░  ░    ░ ░        ░
"""

# Small banner for web UI or compact display
SMALL_BANNER = """
╔══════════════════════════════════════╗
║  GHOSTINTEL v2.5 - OSINT Framework   ║
║     No API Keys • Public Sources     ║
╚══════════════════════════════════════╝
"""

# One-line banner for logging
LINE_BANNER = "👻 GHOSTINTEL v2.5 - Advanced OSINT Framework"


def show_banner():
    """Display the full GhostIntel banner with premium styling"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print colored ASCII art
    for line in BANNER.split('\n'):
        if line.strip():
            # Detect if line contains ASCII art characters
            if any(c in line for c in ['█', '▄', '▒', '░', '▓', '▀']):
                console.print(f"[bold magenta]{line}[/bold magenta]")
            else:
                console.print(line)
    
    # Print main panel
    console.print(Panel.fit(
        "[bold cyan]G H O S T I N T E L[/bold cyan]  [dim]•[/dim]  "
        "[bold white]v2.5 Advanced OSINT Framework[/bold white]\n"
        "[dim]No API Keys  •  Public Sources Only  •  Ethical Use[/dim]\n"
        "[yellow]⚠  For education & authorized security research only[/yellow]",
        border_style="magenta",
        box=box.HEAVY,
    ))
    
    # Print commands
    console.print(
        "[bold cyan]⚡ Commands:[/bold cyan]  "
        "[green]-u USERNAME[/green]  [green]-e EMAIL[/green]  "
        "[green]-p PHONE[/green]  [green]-d DOMAIN[/green]  "
        "[green]-i IP[/green]  [bold yellow]-web[/bold yellow]  "
        "[green]--batch FILE[/green]\n"
        "[dim]GitHub: https://github.com/ruyynn  •  © 2026 Ruyynn[/dim]"
    )
    console.print()


def show_small_banner():
    """Display a smaller banner (for web UI or compact mode)"""
    console.print(SMALL_BANNER, style="bold cyan")


def show_loading_banner():
    """Display banner with loading animation"""
    console.clear()
    console.print("[bold magenta]GHOSTINTEL v2.5[/bold magenta] - [dim]Initializing...[/dim]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        progress.add_task(description="[cyan]Loading modules...[/cyan]", total=None)
        time.sleep(0.5)
    
    console.clear()
    show_banner()


def get_banner_text() -> str:
    """Return banner as plain text (for logs, reports, etc.)"""
    return f"""GhostIntel v2.5 - Advanced OSINT Framework
    No API Keys Required • Public Sources Only • Ethical Use Only
    GitHub: https://github.com/ruyynn
    """


def get_banner_rich() -> Text:
    """Return banner as rich Text object"""
    text = Text()
    text.append("GHOSTINTEL", style="bold magenta")
    text.append(" v2.5 ", style="bold white")
    text.append("• ", style="dim")
    text.append("OSINT Framework", style="cyan")
    return text


def print_header(title: str, subtitle: str = "", icon: str = "🔍"):
    """Print a formatted header with title and subtitle"""
    console.print()
    console.print(Panel(
        Text(f"{icon} {title}", style="bold cyan", justify="center"),
        subtitle=subtitle if subtitle else None,
        box=box.HEAVY,
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()


def print_divider(char: str = "─", length: int = 50):
    """Print a divider line"""
    console.print(f"[dim]{char * length}[/dim]")


def print_entity_summary(entity_type: str, count: int, icon: str = "📦"):
    """Print entity summary line"""
    if count > 0:
        console.print(f"  {icon} [cyan]{entity_type.title()}:[/cyan] [green]{count}[/green]")
    else:
        console.print(f"  {icon} [cyan]{entity_type.title()}:[/cyan] [dim]0[/dim]")


def animate_loading(message: str = "Loading", duration: float = 1.0):
    """Simple loading animation"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    start = time.time()
    i = 0
    
    while time.time() - start < duration:
        console.print(f"\r[cyan]{chars[i % len(chars)]}[/cyan] {message}...", end="")
        time.sleep(0.1)
        i += 1
    
    console.print("\r" + " " * 50, end="")
    console.print("\r", end="")


# ==================== CONVENIENCE FUNCTIONS ====================

def print_success(msg: str):
    """Print success message"""
    console.print(f"[success]✅ {msg}[/success]")


def print_error(msg: str):
    """Print error message"""
    console.print(f"[danger]❌ {msg}[/danger]")


def print_warning(msg: str):
    """Print warning message"""
    console.print(f"[warning]⚠  {msg}[/warning]")


def print_info(msg: str):
    """Print info message"""
    console.print(f"[info]ℹ  {msg}[/info]")


def print_debug(msg: str):
    """Print debug message (only shown with --debug flag)"""
    if "--debug" in sys.argv:
        console.print(f"[dim]🐛 DEBUG: {msg}[/dim]")


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


# ==================== PROGRESS BARS ====================

def create_progress():
    """Create a rich progress bar"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=False
    )


def create_spinner():
    """Create a simple spinner"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    )


# Export commonly used functions
__all__ = [
    'console',
    'show_banner',
    'show_small_banner',
    'show_loading_banner',
    'get_banner_text',
    'get_banner_rich',
    'print_header',
    'print_divider',
    'print_entity_summary',
    'animate_loading',
    'print_success',
    'print_error',
    'print_warning',
    'print_info',
    'print_debug',
    'clear_screen',
    'create_progress',
    'create_spinner'
]