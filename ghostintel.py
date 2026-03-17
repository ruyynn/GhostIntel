#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GHOSTINTEL v2.0 - API-Less OSINT Mashup Engine
Main entry point
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.banner import show_banner, console
from core.engine import GhostIntelEngine
from core.utils import print_help, print_version
from reports.generator import ReportGenerator


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="GhostIntel v2.0 - OSINT Mashup Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    
    # Main command
    parser.add_argument("command", nargs="?", choices=["investigate", "scan", "help"], 
                        help="Command: investigate (default), scan, help")
    
    # Target
    parser.add_argument("target", nargs="?", help="Target to investigate")
    
    # Investigation flags
    parser.add_argument("-u", "--username", metavar="USERNAME", help="Investigate username")
    parser.add_argument("-e", "--email", metavar="EMAIL", help="Investigate email")
    parser.add_argument("-p", "--phone", metavar="PHONE", help="Investigate phone number")
    parser.add_argument("-d", "--domain", metavar="DOMAIN", help="Investigate domain")
    parser.add_argument("-i", "--ip", metavar="IP", help="Investigate IP address")
    
    # Options
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("-o", "--output", metavar="FILE", help="Save report to file")
    parser.add_argument("--format", choices=["json", "html", "txt"], default="json", 
                        help="Output format (default: json)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--threads", type=int, default=20, help="Concurrent threads")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    # Help flags
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    
    return parser.parse_args()


async def main_async():
    """Main async function"""
    args = parse_arguments()
    
    # Handle help
    if args.help or args.command == "help" or (not args.target and not any([args.username, args.email, args.phone, args.domain, args.ip])):
        print_help()
        return
    
    # Handle version
    if args.version:
        print_version()
        return
    
    # Show banner
    if not args.no_color:
        show_banner()
    
    # Initialize engine
    engine = GhostIntelEngine(
        timeout=args.timeout,
        max_concurrent=args.threads
    )
    
    # Determine target
    target = None
    target_type = None
    
    if args.username:
        target = args.username
        target_type = "username"
    elif args.email:
        target = args.email
        target_type = "email"
    elif args.phone:
        target = args.phone
        target_type = "phone"
    elif args.domain:
        target = args.domain
        target_type = "domain"
    elif args.ip:
        target = args.ip
        target_type = "ip"
    elif args.target:
        target = args.target
        target_type = "auto"  # Auto-detect
    
    if not target:
        console.print("[red]❌ No target specified[/red]")
        return
    
    # Run investigation
    if args.report or args.output:
        # Comprehensive investigation with report
        console.print(f"\n[bold cyan]🔍 Comprehensive investigation: [yellow]{target}[/yellow][/bold cyan]")
        
        async with engine:
            results = await engine.investigate_all(target, target_type)
        
        # Generate report
        if results:
            report_gen = ReportGenerator()
            
            filename = args.output if args.output else None
            
            if args.format == "json":
                report_file = await report_gen.save_json(results, filename)
            elif args.format == "html":
                report_file = await report_gen.save_html(results, filename)
            else:
                report_file = await report_gen.save_txt(results, filename)
            
            console.print(f"\n[green]✅ Report saved: {report_file}[/green]")
            
            # Display summary
            await engine.display_summary(results)
    else:
        # Quick investigation
        async with engine:
            result = await engine.investigate(target, target_type)
            if result:
                await engine.display_result(result)


def main():
    """Main entry point"""
    try:
        # Windows event loop fix
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        asyncio.run(main_async())
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Error: {str(e)}[/red]")
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()