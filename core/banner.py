#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Banner and Styling Module
Premium CLI interface with rich formatting
"""

import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.style import Style
from rich.theme import Theme

# Custom theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "danger": "bold red",
    "success": "bold green",
    "ghost": "bold magenta",
    "highlight": "bold blue",
    "dim": "dim white"
})

console = Console(theme=custom_theme)

# Original banner (preserved exactly)
BANNER = """
       ▄████  ██░ ██  ▒█████   ██████ ▄▄▄█████▓     
      ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒    
     ▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░    
     ░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░     
     ░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░     
      ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░       
       ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░        
     ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░          
           ░  ░  ░  ░    ░ ░        ░               
                                                    
                  [ G H O S T I N T E L ]           
                  • OSINT MASHUP ENGINE •     
  ⚠️ Untuk bahan pembelajaran, jangan doxing orang tanpa izin ⚠️
                         Ethical Use                
────────────────────────────────────────────────    
© 2026 Ruyynn.
GitHub : https://github.com/ruyynn
────────────────────────────────────────────────    
"""


def show_banner():
    """Display the GhostIntel banner with premium styling"""
    console.clear()
    
    # Split banner into lines
    lines = BANNER.split('\n')
    
    # Print with colors
    for line in lines:
        if "████" in line or "██" in line:
            console.print(f"[bold magenta]{line}[/bold magenta]")
        elif "OSINT MASHUP ENGINE" in line:
            console.print(f"[bold cyan]{line}[/bold cyan]")
        elif "NO API KEYS" in line:
            console.print(f"[bold green]{line}[/bold green]")
        elif "doxing" in line:
            console.print(f"[yellow]{line}[/yellow]")
        elif "GitHub" in line:
            console.print(f"[blue]{line}[/blue]")
        elif "──" in line:
            console.print(f"[dim]{line}[/dim]")
        elif "©" in line:
            console.print(f"[magenta]{line}[/magenta]")
        else:
            console.print(line)
    
    # Show version and quick tips
    console.print("\n[bold cyan]⚡ GhostIntel v2.0[/bold cyan] [dim]|[/dim] [green]No API Keys Required[/green] [dim]|[/dim] [yellow]Type 'ghostintel help' for commands[/yellow]")
    console.print()


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, subtitle: str = ""):
    """Print a formatted header"""
    console.print()
    console.print(Panel(
        Text(title, style="bold cyan", justify="center"),
        subtitle=subtitle,
        box=box.HEAVY,
        border_style="cyan"
    ))
    console.print()


def print_success(message: str):
    """Print success message"""
    console.print(f"[success]✅ {message}[/success]")


def print_error(message: str):
    """Print error message"""
    console.print(f"[danger]❌ {message}[/danger]")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[warning]⚠ {message}[/warning]")


def print_info(message: str):
    """Print info message"""
    console.print(f"[info]ℹ {message}[/info]")