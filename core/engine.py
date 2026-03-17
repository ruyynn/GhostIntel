#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Main Engine
Orchestrates all OSINT modules and correlation
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Any
from rich.table import Table
from rich.tree import Tree
from rich import box
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from core.banner import console
from core.detector import detector, Entity
from core.correlation import CorrelationEngine
from modules.username import UsernameModule
from modules.email import EmailModule
from modules.phone import PhoneModule
from modules.domain import DomainModule
from modules.ip import IPModule


class GhostIntelEngine:
    """Main investigation engine"""
    
    def __init__(self, timeout: int = 10, max_concurrent: int = 20):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.session = None
        self.results = {}
        self.correlation = CorrelationEngine()
        self.modules = {}
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
            }
        )
        
        # Initialize modules
        self.modules = {
            'username': UsernameModule(self.session),
            'email': EmailModule(self.session),
            'phone': PhoneModule(self.session),
            'domain': DomainModule(self.session),
            'ip': IPModule(self.session)
        }
        
        return self
    
    async def __aexit__(self, *args):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def investigate(self, target: str, target_type: str = None) -> Dict:
        """
        Investigate a single target with appropriate module
        """
        # Detect type if auto
        if not target_type or target_type == 'auto':
            entity = detector.detect(target)
            target_type = entity.type
            target = entity.normalized
        
        console.print(f"\n[cyan]🔍 Investigating: [bold]{target}[/bold] ([yellow]{target_type.upper()}[/yellow])[/cyan]")
        
        # Get module
        module = self.modules.get(target_type)
        if not module:
            console.print(f"[red]❌ No module available for type: {target_type}[/red]")
            return {}
        
        # Run investigation
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                console=console
            ) as progress:
                progress.add_task(description=f"Running {target_type} module...", total=None)
                result = await module.scan(target)
            
            if result:
                self.results[target_type] = result
                return result
            else:
                console.print(f"[red]❌ No results found[/red]")
                return {}
                
        except Exception as e:
            console.print(f"[red]❌ Error: {str(e)}[/red]")
            return {}
    
    async def investigate_all(self, target: str, target_type: str = None) -> Dict[str, Any]:
        """
        Investigate target across all relevant modules
        """
        # Detect type if auto
        if not target_type or target_type == 'auto':
            entity = detector.detect(target)
            target_type = entity.type
            target = entity.normalized
        
        # Show header
        console.print(f"\n[bold cyan]╔══ Comprehensive Investigation ══╗[/bold cyan]")
        console.print(f"[white]Target:[/white] [bold yellow]{target}[/bold yellow]")
        console.print(f"[white]Type:[/white] [bold green]{target_type.upper()}[/bold green]")
        console.print(f"[white]Started:[/white] [dim]{datetime.now().strftime('%H:%M:%S')}[/dim]\n")
        
        # Determine which modules to run
        module_map = {
            'username': ['username', 'email'],
            'email': ['email', 'username', 'domain'],
            'phone': ['phone'],
            'domain': ['domain', 'ip'],
            'ip': ['ip', 'domain'],
        }
        
        modules_to_run = module_map.get(target_type, ['username', 'email', 'phone', 'domain', 'ip'])
        
        # Run modules with progress
        results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task(
                description=f"[cyan]Running investigations...[/cyan]",
                total=len(modules_to_run)
            )
            
            for module_name in modules_to_run:
                module = self.modules.get(module_name)
                if module:
                    progress.update(task, description=f"[cyan]Running {module_name} module...[/cyan]")
                    
                    try:
                        result = await module.scan(target)
                        if result and result.get('data'):
                            results[module_name] = result
                    except Exception as e:
                        console.print(f"  [red]✗ {module_name} failed: {str(e)[:50]}[/red]")
                    
                    progress.update(task, advance=1)
                    await asyncio.sleep(0.1)  # Small delay for UI
        
        self.results = results
        
        # Correlate data
        if results:
            console.print("\n[cyan]🔄 Correlating intelligence...[/cyan]")
            correlations = self.correlation.correlate(results)
            self.results['_correlation'] = correlations
        
        return results
    
    async def display_result(self, result: Dict):
        """Display a single result"""
        if not result:
            return
        
        module = result.get('module', 'unknown')
        data = result.get('data', {})
        
        display_methods = {
            'username': self._display_username,
            'email': self._display_email,
            'phone': self._display_phone,
            'domain': self._display_domain,
            'ip': self._display_ip
        }
        
        display_func = display_methods.get(module)
        if display_func:
            display_func(data)
    
    async def display_summary(self, results: Dict):
        """Display summary of all results"""
        console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        console.print("[bold]INVESTIGATION SUMMARY[/bold]".center(40))
        console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        # Create summary table
        table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
        table.add_column("Module", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Findings", style="white")
        
        for module_name, result in results.items():
            if module_name.startswith('_'):
                continue
                
            if result and result.get('data'):
                data = result['data']
                
                if module_name == 'username':
                    findings = f"{data.get('total_found', 0)} platforms"
                elif module_name == 'email':
                    findings = f"{len(data.get('mx_records', []))} MX records"
                elif module_name == 'phone':
                    findings = data.get('provider', 'Unknown')
                elif module_name == 'domain':
                    findings = f"{len(data.get('ip_addresses', []))} IPs"
                elif module_name == 'ip':
                    findings = data.get('country', 'Unknown')
                else:
                    findings = "Data found"
                
                table.add_row(
                    module_name.upper(),
                    "✅ FOUND",
                    findings
                )
            else:
                table.add_row(
                    module_name.upper(),
                    "⚠️ NO DATA",
                    "-"
                )
        
        console.print(table)
        
        # Show correlation if available
        if '_correlation' in results:
            corr = results['_correlation']
            entities = corr.get('entities', [])
            
            if entities:
                console.print("\n[bold yellow]🔗 Correlated Intelligence:[/bold yellow]")
                
                tree = Tree(f"[bold cyan]{corr.get('primary', 'Target')}[/bold cyan]")
                
                for entity_type, entity_list in entities.items():
                    if entity_list:
                        branch = tree.add(f"[yellow]{entity_type}[/yellow]")
                        for entity in entity_list[:5]:
                            branch.add(f"[dim]{entity}[/dim]")
                
                console.print(tree)
    
    def _display_username(self, data: Dict):
        """Display username results"""
        found = data.get('found', [])
        console.print(Panel(
            f"[bold cyan]Username: [yellow]{data.get('username')}[/yellow][/bold cyan]\n\n"
            f"[green]✅ Found on {len(found)} platforms[/green]\n"
            + "\n".join([f"  • [cyan]{p['platform']}[/cyan]: [dim]{p['url']}[/dim]" for p in found[:10]]),
            title="👤 Username OSINT",
            border_style="cyan",
            box=box.HEAVY_EDGE
        ))
    
    def _display_email(self, data: Dict):
        """Display email results"""
        console.print(Panel(
            f"[bold cyan]Email: [yellow]{data.get('email')}[/yellow][/bold cyan]\n\n"
            f"[white]Domain:[/white] [green]{data.get('domain')}[/green]\n"
            f"[white]MX Records:[/white] {len(data.get('mx_records', []))}\n"
            f"[white]SPF Record:[/white] {'✅ Yes' if data.get('spf') else '❌ No'}\n"
            f"[white]DMARC:[/white] {'✅ Yes' if data.get('dmarc') else '❌ No'}\n"
            f"[white]Gravatar:[/white] {'✅ Yes' if data.get('gravatar') else '❌ No'}",
            title="📧 Email OSINT",
            border_style="cyan",
            box=box.HEAVY_EDGE
        ))
    
    def _display_phone(self, data: Dict):
        """Display phone results"""
        console.print(Panel(
            f"[bold cyan]Phone: [yellow]{data.get('input')}[/yellow][/bold cyan]\n\n"
            f"[white]Formatted:[/white] [green]{data.get('international')}[/green]\n"
            f"[white]Country:[/white] {data.get('country')} ({data.get('country_iso')})\n"
            f"[white]Provider:[/white] {data.get('provider', 'Unknown')}\n"
            f"[white]Line Type:[/white] {data.get('line_type')}\n"
            f"[white]Location:[/white] {data.get('location', 'N/A')}\n"
            f"[white]Valid:[/white] {'✅ Yes' if data.get('valid') else '❌ No'}",
            title="📱 Phone OSINT",
            border_style="cyan",
            box=box.HEAVY_EDGE
        ))
    
    def _display_domain(self, data: Dict):
        """Display domain results"""
        console.print(Panel(
            f"[bold cyan]Domain: [yellow]{data.get('domain')}[/yellow][/bold cyan]\n\n"
            f"[white]IP Addresses:[/white] {', '.join(data.get('ip_addresses', [])[:3])}\n"
            f"[white]Nameservers:[/white] {len(data.get('nameservers', []))}\n"
            f"[white]MX Records:[/white] {len(data.get('mx_records', []))}\n"
            f"[white]Website:[/white] {'✅ Yes' if data.get('http_status') == 200 else '❌ No'}\n"
            f"[white]Title:[/white] {data.get('title', 'N/A')[:50]}",
            title="🌐 Domain OSINT",
            border_style="cyan",
            box=box.HEAVY_EDGE
        ))
    
    def _display_ip(self, data: Dict):
        """Display IP results"""
        console.print(Panel(
            f"[bold cyan]IP: [yellow]{data.get('ip')}[/yellow][/bold cyan]\n\n"
            f"[white]Country:[/white] {data.get('country', 'Unknown')}\n"
            f"[white]City:[/white] {data.get('city', 'Unknown')}\n"
            f"[white]ISP:[/white] {data.get('isp', 'Unknown')}\n"
            f"[white]Organization:[/white] {data.get('org', 'Unknown')}\n"
            f"[white]ASN:[/white] {data.get('asn', 'N/A')}\n"
            f"[white]Reverse DNS:[/white] {data.get('reverse_dns', 'N/A')}",
            title="🌍 IP OSINT",
            border_style="cyan",
            box=box.HEAVY_EDGE
        ))