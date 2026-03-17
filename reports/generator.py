#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Report Generator
Generates JSON, HTML, and TXT reports
"""

import json
import aiofiles
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from jinja2 import Template

from reports.html_template import HTML_TEMPLATE


class ReportGenerator:
    """Generate reports in various formats"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_json(self, results: Dict, filename: Optional[str] = None) -> Path:
        """Save results as JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ghostintel_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Prepare data
        data = {
            'generated': datetime.now().isoformat(),
            'version': '2.0.0',
            'results': self._make_serializable(results)
        }
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=2, ensure_ascii=False))
        
        return filepath
    
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
        
        return filepath
    
    async def save_txt(self, results: Dict, filename: Optional[str] = None) -> Path:
        """Save results as text report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ghostintel_{timestamp}.txt"
        
        filepath = self.output_dir / filename
        
        lines = []
        lines.append("=" * 60)
        lines.append("GHOSTINTEL v2.0 - INVESTIGATION REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        lines.append("")
        
        for module_name, result in results.items():
            if module_name.startswith('_'):
                continue
                
            if result and 'data' in result:
                lines.append(f"[{module_name.upper()} MODULE]")
                lines.append("-" * 40)
                
                data = result['data']
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        lines.append(f"  {key}: {json.dumps(value, indent=2)}")
                    else:
                        lines.append(f"  {key}: {value}")
                
                if 'sources' in result:
                    lines.append(f"  Sources: {', '.join(result['sources'])}")
                lines.append("")
        
        # Add correlation if available
        if '_correlation' in results:
            corr = results['_correlation']
            lines.append("[CORRELATION]")
            lines.append("-" * 40)
            if 'entities' in corr:
                for etype, entities in corr['entities'].items():
                    lines.append(f"  {etype}: {', '.join(list(entities)[:10])}")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append("End of Report")
        lines.append("=" * 60)
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write('\n'.join(lines))
        
        return filepath
    
    def _make_serializable(self, obj):
        """Make object JSON serializable"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(i) for i in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return str(obj)
    
    def _prepare_html_data(self, results: Dict) -> Dict:
        """Prepare data for HTML template"""
        modules = {}
        target = "Unknown"
        
        for name, result in results.items():
            if name.startswith('_'):
                continue
                
            if result and 'data' in result:
                modules[name] = {
                    'name': name,
                    'data': result['data'],
                    'sources': result.get('sources', [])
                }
                
                # Get target from first module
                if target == "Unknown" and 'target' in result:
                    target = result['target']
        
        # Get correlation
        correlation = results.get('_correlation', {})
        
        return {
            'target': target,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'modules': modules,
            'correlation': correlation,
            'total_modules': len(modules)
        }