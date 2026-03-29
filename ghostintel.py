#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GHOSTINTEL v2.5 - Advanced OSINT Framework
Enhanced with batch processing, markdown output, and more options
"""
import asyncio
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.banner import show_banner, console
from core.engine import GhostIntelEngine
from core.utils import print_help, print_version
from reports.generator import ReportGenerator


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="GhostIntel v2.5 - Advanced OSINT Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    
    # Main command
    parser.add_argument("command", nargs="?", choices=["investigate", "scan", "help"],
                        help="Command: investigate (default), scan, help")
    parser.add_argument("target", nargs="?", help="Target to investigate")
    
    # Investigation flags
    parser.add_argument("-u", "--username", metavar="USERNAME", help="Investigate username")
    parser.add_argument("-e", "--email", metavar="EMAIL", help="Investigate email")
    parser.add_argument("-p", "--phone", metavar="PHONE", help="Investigate phone number")
    parser.add_argument("-d", "--domain", metavar="DOMAIN", help="Investigate domain")
    parser.add_argument("-i", "--ip", metavar="IP", help="Investigate IP address")
    
    # Web UI
    parser.add_argument("-web", "--web", action="store_true", help="Launch web UI")
    parser.add_argument("--port", type=int, default=7331, help="Web UI port (default: 7331)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    
    # Report options
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("-o", "--output", metavar="FILE", help="Save report to file")
    parser.add_argument("--output-dir", metavar="DIR", default="output", 
                        help="Output directory for reports (default: output)")
    parser.add_argument("--format", choices=["json", "html", "txt", "md", "all"], 
                        default="json", help="Output format (default: json)")
    parser.add_argument("--compress", action="store_true", 
                        help="Compress JSON output with gzip")
    
    # Batch processing
    parser.add_argument("--batch", metavar="FILE", 
                        help="Batch scan: file with one target per line")
    parser.add_argument("--batch-delay", type=float, default=1.0,
                        help="Delay between batch scans in seconds (default: 1.0)")
    
    # Investigation options
    parser.add_argument("--timeout", type=int, default=12, 
                        help="Request timeout in seconds (default: 12)")
    parser.add_argument("--threads", type=int, default=25, 
                        help="Concurrent threads (default: 25)")
    parser.add_argument("--deep", action="store_true", 
                        help="Deep investigation (run all relevant modules)")
    
    # Output options
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--quiet", action="store_true", help="Suppress output (only save report)")
    
    # Help flags
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    return parser.parse_args()


async def batch_scan(targets: list, args) -> dict:
    """Scan multiple targets from a file"""
    results = {}
    engine = GhostIntelEngine(timeout=args.timeout, max_concurrent=args.threads)
    
    console.print(f"\n[bold cyan]📦 Batch scanning {len(targets)} targets[/bold cyan]\n")
    
    async with engine:
        for idx, target in enumerate(targets, 1):
            target = target.strip()
            if not target or target.startswith('#'):
                continue
            
            console.print(f"[{idx}/{len(targets)}] 🔍 Scanning: [yellow]{target}[/yellow]")
            
            try:
                # Auto-detect type
                from core.detector import detector
                entity = detector.detect(target)
                target_type = entity.type
                norm_target = entity.normalized
                
                if args.deep:
                    result = await engine.investigate_all(norm_target, target_type)
                else:
                    result = await engine.investigate(norm_target, target_type)
                
                if result:
                    results[target] = result
                    console.print(f"  [green]✅ Found {len(result.get('data', {}).get('found', [])) if result.get('data') else 0} results[/green]")
                else:
                    console.print(f"  [yellow]⚠️ No results[/yellow]")
                    
            except Exception as e:
                console.print(f"  [red]❌ Error: {e}[/red]")
                if args.debug:
                    import traceback
                    traceback.print_exc()
            
            # Delay between scans
            if idx < len(targets):
                await asyncio.sleep(args.batch_delay)
    
    return results


async def main_async():
    args = parse_arguments()
    
    # Version
    if args.version:
        print_version()
        return
    
    # Web UI
    if args.web:
        from web.server import start_web_server
        if not args.no_color:
            show_banner()
        start_web_server(port=args.port, open_browser=not args.no_browser)
        return
    
    # Help
    if args.help or args.command == "help" or (not any([args.username, args.email, args.phone, args.domain, args.ip, args.target, args.batch])):
        print_help()
        return
    
    # Show banner
    if not args.no_color and not args.quiet:
        show_banner()
    
    # Batch processing
    if args.batch:
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not targets:
                console.print("[red]❌ No targets found in batch file[/red]")
                return
            
            results = await batch_scan(targets, args)
            
            # Generate summary report for batch
            if results and (args.report or args.output):
                rg = ReportGenerator(output_dir=args.output_dir)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if args.format == "all":
                    # Save all formats
                    base_name = args.output or f"ghostintel_batch_{timestamp}"
                    files = await rg.save_all_formats(results, base_name)
                    console.print(f"\n[green]✅ Batch reports saved: {len(files)} files[/green]")
                else:
                    fname = args.output or f"ghostintel_batch_{timestamp}.{args.format}"
                    if args.format == "json":
                        f = await rg.save_json(results, fname, compress=args.compress)
                    elif args.format == "html":
                        f = await rg.save_html(results, fname)
                    elif args.format == "txt":
                        f = await rg.save_txt(results, fname)
                    elif args.format == "md":
                        f = await rg.save_markdown(results, fname)
                    console.print(f"\n[green]✅ Batch report saved: {f}[/green]")
            
            console.print(f"\n[bold green]📊 Batch Summary:[/bold green]")
            console.print(f"  Total targets: {len(targets)}")
            console.print(f"  Successful: {len(results)}")
            console.print(f"  Failed: {len(targets) - len(results)}")
            
        except FileNotFoundError:
            console.print(f"[red]❌ Batch file not found: {args.batch}[/red]")
        except Exception as e:
            console.print(f"[red]❌ Batch error: {e}[/red]")
            if args.debug:
                import traceback
                traceback.print_exc()
        return
    
    # Single target
    engine = GhostIntelEngine(timeout=args.timeout, max_concurrent=args.threads)
    
    target, target_type = None, None
    if args.username:   target, target_type = args.username, "username"
    elif args.email:    target, target_type = args.email,    "email"
    elif args.phone:    target, target_type = args.phone,    "phone"
    elif args.domain:   target, target_type = args.domain,   "domain"
    elif args.ip:       target, target_type = args.ip,       "ip"
    elif args.target:   target, target_type = args.target,   "auto"
    
    if not target:
        console.print("[red]❌ No target specified[/red]")
        return
    
    # Deep investigation with report
    if args.report or args.output or args.deep:
        if not args.quiet:
            console.print(f"\n[bold cyan]🔍 Deep Investigation: [yellow]{target}[/yellow][/bold cyan]")
        
        async with engine:
            results = await engine.investigate_all(target, target_type)
        
        if results:
            rg = ReportGenerator(output_dir=args.output_dir)
            
            # Handle "all" format
            if args.format == "all":
                base_name = args.output or None
                files = await rg.save_all_formats(results, base_name)
                if not args.quiet:
                    console.print(f"\n[green]✅ Reports saved: {len(files)} files[/green]")
            else:
                fname = args.output
                if args.format == "json":
                    f = await rg.save_json(results, fname, compress=args.compress)
                elif args.format == "html":
                    f = await rg.save_html(results, fname)
                elif args.format == "txt":
                    f = await rg.save_txt(results, fname)
                elif args.format == "md":
                    f = await rg.save_markdown(results, fname)
                else:
                    f = await rg.save_json(results, fname)
                
                if not args.quiet:
                    console.print(f"\n[green]✅ Report saved: {f}[/green]")
            
            if not args.quiet:
                await engine.display_summary(results)
        else:
            if not args.quiet:
                console.print("[red]❌ No results found[/red]")
    
    # Quick investigation
    else:
        async with engine:
            result = await engine.investigate(target, target_type)
            if result and not args.quiet:
                await engine.display_result(result)
            elif not result and not args.quiet:
                console.print("[red]❌ No results found[/red]")


def main():
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main_async())
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠  Interrupted[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Fatal: {e}[/red]")
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    from datetime import datetime  # For batch timestamp
    main()