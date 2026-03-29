#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.5 - Report Generator
Generates JSON, HTML, TXT, and Markdown reports
Enhanced with compression, batch processing, and better formatting
"""

import json
import aiofiles
import gzip
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Any
from jinja2 import Template

from reports.html_template import HTML_TEMPLATE
from core.banner import console


class ReportGenerator:
    """Generate reports in various formats - Enhanced v2.5"""
    
    def __init__(self, output_dir: str = "output", compress: bool = False):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.compress = compress
        self.version = "2.5.0"
    
    # ==================== JSON REPORT ====================
    
    async def save_json(self, results: Dict, filename: Optional[str] = None, 
                        pretty: bool = True, compress: bool = None) -> Path:
        """Save results as JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ghostintel_{timestamp}.json"
        
        filepath = self.output_dir / filename
        use_compress = compress if compress is not None else self.compress
        
        # Prepare data
        data = {
            'generated': datetime.now().isoformat(),
            'version': self.version,
            'tool': 'GhostIntel',
            'results': self._make_serializable(results)
        }
        
        # JSON string
        if pretty:
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            json_str = json.dumps(data, ensure_ascii=False)
        
        # Write with or without compression
        if use_compress:
            filepath = filepath.with_suffix('.json.gz')
            async with aiofiles.open(filepath, 'wb') as f:
                compressed = gzip.compress(json_str.encode('utf-8'), compresslevel=6)
                await f.write(compressed)
            console.print(f"[green]✅ Compressed JSON report saved: {filepath}[/green]")
        else:
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json_str)
            console.print(f"[green]✅ JSON report saved: {filepath}[/green]")
        
        return filepath
    
    # ==================== HTML REPORT ====================
    
    async def save_html(self, results: Dict, filename: Optional[str] = None) -> Path:
        """Save results as HTML report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ghostintel_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        # Prepare template data
        template_data = self._prepare_html_data(results)
        
        # Render template
        template = Template(HTML_TEMPLATE)
        html_content = template.render(**template_data)
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(html_content)
        
        console.print(f"[green]✅ HTML report saved: {filepath}[/green]")
        return filepath
    
    # ==================== TXT REPORT ====================
    
    async def save_txt(self, results: Dict, filename: Optional[str] = None) -> Path:
        """Save results as text report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ghostintel_{timestamp}.txt"
        
        filepath = self.output_dir / filename
        
        lines = []
        lines.append("=" * 70)
        lines.append(f"GHOSTINTEL v{self.version} - INVESTIGATION REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")
        
        for module_name, result in results.items():
            if module_name.startswith('_'):
                continue
                
            if result and 'data' in result:
                lines.append(f"\n┌─[ {module_name.upper()} MODULE ]─" + "─" * 40)
                lines.append("│")
                
                data = result['data']
                for key, value in data.items():
                    if key == 'timestamp':
                        continue
                    
                    # Format key
                    key_display = key.replace('_', ' ').title()
                    
                    if isinstance(value, dict):
                        lines.append(f"│  📁 {key_display}:")
                        for sub_key, sub_val in value.items():
                            if isinstance(sub_val, (dict, list)):
                                lines.append(f"│     {sub_key}: {json.dumps(sub_val, indent=2)[:100]}")
                            else:
                                lines.append(f"│     {sub_key}: {sub_val}")
                    elif isinstance(value, list):
                        if value and isinstance(value[0], dict):
                            lines.append(f"│  📋 {key_display}:")
                            for i, item in enumerate(value[:10]):
                                if isinstance(item, dict):
                                    item_str = ', '.join(f"{k}:{v}" for k, v in list(item.items())[:3])
                                    lines.append(f"│     {i+1}. {item_str[:80]}")
                                else:
                                    lines.append(f"│     {i+1}. {item}")
                            if len(value) > 10:
                                lines.append(f"│     ... and {len(value)-10} more")
                        else:
                            lines.append(f"│  📋 {key_display}: {', '.join(str(v)[:50] for v in value[:5])}")
                            if len(value) > 5:
                                lines.append(f"│     ... and {len(value)-5} more")
                    else:
                        # Handle boolean values nicely
                        if isinstance(value, bool):
                            value_str = "✓ Yes" if value else "✗ No"
                        else:
                            value_str = str(value)[:100]
                        lines.append(f"│  • {key_display}: {value_str}")
                
                if 'sources' in result:
                    lines.append(f"│")
                    lines.append(f"│  🔍 Sources: {', '.join(result['sources'])}")
                lines.append("│")
                lines.append("└" + "─" * 68)
                lines.append("")
        
        # Add correlation if available
        if '_correlation' in results:
            corr = results['_correlation']
            lines.append("\n┌─[ CORRELATION ]─" + "─" * 50)
            lines.append("│")
            lines.append(f"│  🎯 Primary Target: {corr.get('primary', 'Unknown')}")
            lines.append("│")
            
            if 'entities' in corr:
                for etype, entities in corr['entities'].items():
                    if entities:
                        lines.append(f"│  🔗 {etype.upper()}:")
                        for entity in entities[:10]:
                            lines.append(f"│     ↳ {entity}")
                        if len(entities) > 10:
                            lines.append(f"│     ... and {len(entities)-10} more")
                        lines.append("│")
            
            if 'summary' in corr:
                lines.append("│  📊 Summary:")
                for etype, count in corr['summary'].items():
                    lines.append(f"│     • {etype}: {count}")
            
            lines.append("│")
            lines.append("└" + "─" * 68)
        
        lines.append("\n" + "=" * 70)
        lines.append("End of Report")
        lines.append("=" * 70)
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write('\n'.join(lines))
        
        console.print(f"[green]✅ Text report saved: {filepath}[/green]")
        return filepath
    
    # ==================== MARKDOWN REPORT ====================
    
    async def save_markdown(self, results: Dict, filename: Optional[str] = None) -> Path:
        """Save results as Markdown report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ghostintel_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        lines = []
        lines.append(f"# 👻 GhostIntel v{self.version} Investigation Report\n")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("---\n")
        
        for module_name, result in results.items():
            if module_name.startswith('_'):
                continue
                
            if result and 'data' in result:
                lines.append(f"\n## 📦 {module_name.upper()} MODULE\n")
                
                data = result['data']
                for key, value in data.items():
                    if key == 'timestamp':
                        continue
                    
                    key_display = key.replace('_', ' ').title()
                    
                    if isinstance(value, dict):
                        lines.append(f"### {key_display}\n")
                        for sub_key, sub_val in value.items():
                            lines.append(f"- **{sub_key}:** `{sub_val}`")
                        lines.append("")
                    elif isinstance(value, list):
                        if value and isinstance(value[0], dict):
                            lines.append(f"### {key_display}\n")
                            for i, item in enumerate(value):
                                item_str = ' | '.join(f"**{k}**: {v}" for k, v in list(item.items())[:3])
                                lines.append(f"{i+1}. {item_str}")
                            lines.append("")
                        else:
                            lines.append(f"- **{key_display}:** {', '.join(str(v)[:50] for v in value[:10])}")
                            if len(value) > 10:
                                lines.append(f"  *... and {len(value)-10} more*")
                    else:
                        if isinstance(value, bool):
                            value_str = "✅ Yes" if value else "❌ No"
                        else:
                            value_str = str(value)[:100]
                        lines.append(f"- **{key_display}:** {value_str}")
                
                if 'sources' in result:
                    lines.append(f"\n**Sources:** {', '.join(result['sources'])}")
                lines.append("")
        
        # Add correlation
        if '_correlation' in results:
            corr = results['_correlation']
            lines.append("\n## 🔗 Intelligence Correlation\n")
            lines.append(f"**Primary Target:** {corr.get('primary', 'Unknown')}\n")
            
            if 'entities' in corr:
                lines.append("### Entities Found\n")
                for etype, entities in corr['entities'].items():
                    if entities:
                        lines.append(f"**{etype.upper()}:**")
                        for entity in entities[:10]:
                            lines.append(f"- `{entity}`")
                        if len(entities) > 10:
                            lines.append(f"*... and {len(entities)-10} more*")
                        lines.append("")
        
        lines.append("\n---\n")
        lines.append(f"*Report generated by GhostIntel v{self.version} | © 2026 Ruyynn*")
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write('\n'.join(lines))
        
        console.print(f"[green]✅ Markdown report saved: {filepath}[/green]")
        return filepath
    
    # ==================== BATCH PROCESSING ====================
    
    async def save_all_formats(self, results: Dict, base_name: Optional[str] = None) -> List[Path]:
        """Save report in all formats"""
        files = []
        
        if not base_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"ghostintel_{timestamp}"
        
        tasks = [
            self.save_json(results, f"{base_name}.json"),
            self.save_html(results, f"{base_name}.html"),
            self.save_txt(results, f"{base_name}.txt"),
            self.save_markdown(results, f"{base_name}.md"),
        ]
        
        files = await asyncio.gather(*tasks)
        
        console.print(f"[green]✅ All reports saved to {self.output_dir}/[/green]")
        return files
    
    # ==================== UTILITY METHODS ====================
    
    def _make_serializable(self, obj: Any) -> Any:
        """Make object JSON serializable"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(i) for i in obj]
        elif isinstance(obj, set):
            return sorted(list(obj))
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        else:
            return str(obj)
    
    def _prepare_html_data(self, results: Dict) -> Dict:
        """Prepare data for HTML template"""
        modules = {}
        target = "Unknown"
        
        # First pass: collect modules
        for name, result in results.items():
            if name.startswith('_'):
                continue
                
            if result and 'data' in result:
                data = self._make_serializable(result['data'])
                
                modules[name] = {
                    'name': name,
                    'data': data,
                    'sources': result.get('sources', [])
                }
                
                if target == "Unknown" and 'target' in result:
                    target = result['target']
        
        # Get correlation and ensure it's serializable
        correlation = results.get('_correlation', {})
        correlation = self._make_serializable(correlation)
        
        # Final check for entities
        if correlation and 'entities' in correlation:
            for etype, entities in correlation['entities'].items():
                if isinstance(entities, set):
                    correlation['entities'][etype] = list(entities)
                elif not isinstance(entities, list):
                    correlation['entities'][etype] = []
        
        return {
            'target': target,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'modules': modules,
            'correlation': correlation,
            'total_modules': len(modules),
            'version': self.version
        }
    
    def get_output_dir(self) -> Path:
        """Get output directory path"""
        return self.output_dir
    
    def clean_old_reports(self, days: int = 30):
        """Delete reports older than specified days"""
        import time
        now = time.time()
        cutoff = now - (days * 86400)
        
        deleted = 0
        for file in self.output_dir.glob("ghostintel_*"):
            if file.stat().st_mtime < cutoff:
                file.unlink()
                deleted += 1
        
        if deleted:
            console.print(f"[dim]Cleaned up {deleted} old report(s)[/dim]")


# Import asyncio for batch processing
import asyncio