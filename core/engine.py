#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Main Engine"""

import asyncio
import aiohttp
import socket
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
    """Main OSINT investigation engine"""

    def __init__(self, timeout: int = 12, max_concurrent: int = 25):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.session = None
        self.results = {}
        self.correlation = CorrelationEngine()
        self.modules = {}

    async def __aenter__(self):
        # Gunakan DNS resolver manual dengan nameserver Google
        resolver = aiohttp.resolver.AsyncResolver(
            nameservers=['8.8.8.8', '1.1.1.1', '8.8.4.4']
        )
        
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            ssl=False,
            force_close=True,
            enable_cleanup_closed=True,
            resolver=resolver,  # <-- Ini kuncinya
            ttl_dns_cache=300
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/124.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        self.modules = {
            'username': UsernameModule(self.session),
            'email': EmailModule(self.session),
            'phone': PhoneModule(self.session),
            'domain': DomainModule(self.session),
            'ip': IPModule(self.session),
        }
        return self

    async def __aexit__(self, *args):
        if self.session and not self.session.closed:
            await self.session.close()

    async def investigate(self, target: str, target_type: str = None) -> Dict:
        """Single-module investigation"""
        if not target_type or target_type == 'auto':
            entity = detector.detect(target)
            target_type = entity.type
            target = entity.normalized

        console.print(f"\n[cyan]🔍 Investigating: [bold]{target}[/bold] "
                      f"([yellow]{target_type.upper()}[/yellow])[/cyan]")

        module = self.modules.get(target_type)
        if not module:
            console.print(f"[red]❌ No module for type: {target_type}[/red]")
            return {}

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True, console=console
            ) as progress:
                progress.add_task(description=f"Running {target_type} scan…", total=None)
                result = await module.scan(target)
            if result and not result.get('error'):
                self.results[target_type] = result
                return result
            elif result and result.get('error'):
                console.print(f"[red]❌ {result['error']}[/red]")
                return result
            else:
                console.print("[red]❌ No results[/red]")
                return {}
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            return {}

    async def investigate_all(self, target: str, target_type: str = None) -> Dict[str, Any]:
        """Multi-module deep investigation"""
        if not target_type or target_type == 'auto':
            entity = detector.detect(target)
            target_type = entity.type
            target = entity.normalized

        console.print(f"\n[bold cyan]╔══ Deep Investigation ══╗[/bold cyan]")
        console.print(f"[white]Target :[/white] [bold yellow]{target}[/bold yellow]")
        console.print(f"[white]Type   :[/white] [bold green]{target_type.upper()}[/bold green]")
        console.print(f"[white]Time   :[/white] [dim]{datetime.now().strftime('%H:%M:%S')}[/dim]\n")

        module_map = {
            'username': ['username', 'email'],
            'email':    ['email', 'domain'],
            'phone':    ['phone'],
            'domain':   ['domain', 'ip'],
            'ip':       ['ip', 'domain'],
        }
        modules_to_run = module_map.get(target_type, list(self.modules.keys()))

        results = {}
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(), console=console
        ) as progress:
            task = progress.add_task("[cyan]Running modules…[/cyan]", total=len(modules_to_run))

            for mod_name in modules_to_run:
                mod = self.modules.get(mod_name)
                if mod:
                    progress.update(task, description=f"[cyan]{mod_name}…[/cyan]")
                    try:
                        r = await mod.scan(target)
                        if r and r.get('data'):
                            results[mod_name] = r
                    except Exception as e:
                        console.print(f"  [red]✗ {mod_name}: {str(e)[:60]}[/red]")
                    progress.advance(task)
                    await asyncio.sleep(0.05)

        self.results = results
        if results:
            console.print("\n[cyan]🔄 Correlating intelligence…[/cyan]")
            self.results['_correlation'] = self.correlation.correlate(results)

        return self.results

    async def display_result(self, result: Dict):
        if not result or result.get('error'):
            return
        mod = result.get('module', '')
        data = result.get('data', {})
        fn = {
            'username': self._show_username,
            'email':    self._show_email,
            'phone':    self._show_phone,
            'domain':   self._show_domain,
            'ip':       self._show_ip,
        }.get(mod)
        if fn:
            fn(data)

    async def display_summary(self, results: Dict):
        console.print("\n[bold cyan]═══ INVESTIGATION SUMMARY ═══[/bold cyan]\n")
        t = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
        t.add_column("Module");  t.add_column("Status"); t.add_column("Key Findings")

        for name, result in results.items():
            if name.startswith('_'):
                continue
            if result and result.get('data'):
                d = result['data']
                if name == 'username':   findings = f"{d.get('total_found',0)} platforms found"
                elif name == 'email':    findings = f"{len(d.get('mx_records',[]))} MX | SPF={'✓' if d.get('spf') else '✗'} | DMARC={'✓' if d.get('dmarc') else '✗'}"
                elif name == 'phone':    findings = f"{d.get('provider','?')} | {d.get('country','?')} | {d.get('line_type','?')}"
                elif name == 'domain':   findings = f"IP={','.join(d.get('ip_addresses',[])[:2])} | {d.get('https_status') or d.get('http_status','?')}"
                elif name == 'ip':       findings = f"{d.get('city','?')}, {d.get('country','?')} | {d.get('isp','?')}"
                else:                    findings = "Data found"
                t.add_row(name.upper(), "[green]✅ OK[/green]", findings)
            else:
                t.add_row(name.upper(), "[red]⚠ None[/red]", "—")

        console.print(t)

        if '_correlation' in results:
            corr = results['_correlation']
            entities = corr.get('entities', {})
            if entities:
                console.print("\n[bold yellow]🔗 Correlated Intel:[/bold yellow]")
                tree = Tree(f"[bold cyan]{corr.get('primary','Target')}[/bold cyan]")
                for etype, elist in entities.items():
                    if elist:
                        branch = tree.add(f"[yellow]{etype}[/yellow]")
                        for e in list(elist)[:5]:
                            branch.add(f"[dim]{e}[/dim]")
                console.print(tree)

    # ── Display helpers ──
    def _show_username(self, d):
        found = d.get('found', [])
        lines = [f"[bold cyan]👤 Username:[/bold cyan] [yellow]{d.get('username')}[/yellow]",
                 f"[green]✓ Found on {len(found)} / {d.get('total_checked',0)} platforms[/green]"]
        for p in found[:15]:
            lines.append(f"  [cyan]•[/cyan] [white]{p['platform']:<20}[/white] [dim]{p['url']}[/dim]")
        if len(found) > 15:
            lines.append(f"  [dim]… and {len(found)-15} more[/dim]")
        console.print(Panel('\n'.join(lines), title="👤 USERNAME OSINT", border_style="cyan", box=box.HEAVY_EDGE))

    def _show_email(self, d):
        lines = [
            f"[bold cyan]📧 Email:[/bold cyan] [yellow]{d.get('email')}[/yellow]",
            f"[white]Domain    :[/white] {d.get('domain')}",
            f"[white]MX Records:[/white] {len(d.get('mx_records',[]))} found",
            f"[white]SPF       :[/white] {'[green]✓ Present[/green]' if d.get('spf') else '[red]✗ Missing[/red]'}",
            f"[white]DMARC     :[/white] {'[green]✓ Present[/green]' if d.get('dmarc') else '[yellow]✗ Missing[/yellow]'}",
            f"[white]Disposable:[/white] {'[red]Yes ⚠[/red]' if d.get('disposable') else '[green]No[/green]'}",
            f"[white]Gravatar  :[/white] {'[green]✓ Has profile[/green]' if d.get('gravatar') else 'Not found'}",
            f"[white]Website   :[/white] {'[green]✓ ' + str(d.get('website_url','')) + '[/green]' if d.get('has_website') else '[red]No website[/red]'}",
        ]
        if d.get('breach_hint'):
            lines.append(f"[white]Breach hint:[/white] [yellow]{d['breach_hint']}[/yellow]")
        console.print(Panel('\n'.join(lines), title="📧 EMAIL OSINT", border_style="magenta", box=box.HEAVY_EDGE))

    def _show_phone(self, d):
        lines = [
            f"[bold cyan]📱 Phone:[/bold cyan] [yellow]{d.get('input')}[/yellow]",
            f"[white]International:[/white] [green]{d.get('international')}[/green]",
            f"[white]Country      :[/white] {d.get('country')} ({d.get('country_iso')})",
            f"[white]Provider     :[/white] [cyan]{d.get('provider','Unknown')}[/cyan]",
            f"[white]Type         :[/white] {d.get('line_type')}",
            f"[white]Location     :[/white] {d.get('location') or '—'}",
            f"[white]Timezone     :[/white] {', '.join(d.get('timezones',[])[:2]) or '—'}",
            f"[white]Mobile       :[/white] {'[green]Yes[/green]' if d.get('is_mobile') else 'No'}",
        ]
        if d.get('whatsapp_link'):
            lines.append(f"[white]WhatsApp     :[/white] [green]{d['whatsapp_link']}[/green]")
        console.print(Panel('\n'.join(lines), title="📱 PHONE OSINT", border_style="green", box=box.HEAVY_EDGE))

    def _show_domain(self, d):
        lines = [
            f"[bold cyan]🌐 Domain:[/bold cyan] [yellow]{d.get('domain')}[/yellow]",
            f"[white]IPv4         :[/white] {', '.join(d.get('ip_addresses',[])[:3]) or '[red]None[/red]'}",
            f"[white]IPv6         :[/white] {', '.join(d.get('ipv6_addresses',[])[:2]) or '—'}",
            f"[white]Nameservers  :[/white] {', '.join(d.get('nameservers',[])[:3]) or '—'}",
            f"[white]MX Records   :[/white] {len(d.get('mx_records',[]))}",
            f"[white]HTTPS status :[/white] {d.get('https_status') or '—'}",
            f"[white]HTTP status  :[/white] {d.get('http_status') or '—'}",
            f"[white]Server       :[/white] {d.get('server_header') or '—'}",
            f"[white]Title        :[/white] {(d.get('title') or '—')[:60]}",
        ]
        if d.get('technologies'):
            lines.append(f"[white]Tech stack   :[/white] [cyan]{', '.join(d['technologies'])}[/cyan]")
        if d.get('security_headers'):
            sh = d['security_headers']
            sec = []
            if sh.get('hsts'):   sec.append('[green]HSTS[/green]')
            if sh.get('csp'):    sec.append('[green]CSP[/green]')
            if sh.get('xframe'): sec.append('[green]X-Frame[/green]')
            if sec: lines.append(f"[white]Security     :[/white] {' '.join(sec)}")
        console.print(Panel('\n'.join(lines), title="🌐 DOMAIN OSINT", border_style="yellow", box=box.HEAVY_EDGE))

    def _show_ip(self, d):
        lines = [
            f"[bold cyan]🌍 IP:[/bold cyan] [yellow]{d.get('ip')}[/yellow]",
            f"[white]Country   :[/white] {d.get('country','?')} ({d.get('country_code','?')})",
            f"[white]Region    :[/white] {d.get('region','—')}",
            f"[white]City      :[/white] {d.get('city','—')}",
            f"[white]Coords    :[/white] {d.get('lat','?')}, {d.get('lon','?')}",
            f"[white]ISP       :[/white] {d.get('isp','—')}",
            f"[white]Org       :[/white] {d.get('org','—')}",
            f"[white]ASN       :[/white] {d.get('asn','—')} {d.get('asn_name','')}",
            f"[white]Reverse   :[/white] {d.get('reverse_dns') or '—'}",
            f"[white]Proxy/VPN :[/white] {'[red]⚠ Detected[/red]' if d.get('is_proxy') else '[green]No[/green]'}",
            f"[white]Hosting   :[/white] {'[yellow]Yes (datacenter)[/yellow]' if d.get('is_hosting') else 'No'}",
            f"[white]Mobile ISP:[/white] {'[cyan]Yes[/cyan]' if d.get('is_mobile') else 'No'}",
        ]
        if d.get('rdap',{}).get('organization'):
            lines.append(f"[white]RIR Org   :[/white] {d['rdap']['organization']}")
        if d.get('abuse_contact'):
            lines.append(f"[white]Abuse     :[/white] [yellow]{d['abuse_contact']}[/yellow]")
        console.print(Panel('\n'.join(lines), title="🌍 IP OSINT", border_style="yellow", box=box.HEAVY_EDGE))