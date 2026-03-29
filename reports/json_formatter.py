#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.5 - JSON Formatter
Format results as JSON with enhanced features
"""

import json
import gzip
from datetime import datetime
from typing import Dict, Any, Optional, Union
from pathlib import Path


class JSONFormatter:
    """Format results as JSON - Enhanced v2.5"""
    
    VERSION = "2.5.0"
    
    @staticmethod
    def format(results: Dict[str, Any], pretty: bool = True, 
               include_metadata: bool = True) -> str:
        """
        Format results to JSON string
        
        Args:
            results: Results dictionary
            pretty: Pretty print with indentation
            include_metadata: Include generation metadata
        """
        if include_metadata:
            data = {
                'generated': datetime.now().isoformat(),
                'version': JSONFormatter.VERSION,
                'tool': 'GhostIntel',
                'results': JSONFormatter._make_serializable(results)
            }
        else:
            data = JSONFormatter._make_serializable(results)
        
        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False, default=str)
        else:
            return json.dumps(data, ensure_ascii=False, default=str)
    
    @staticmethod
    def format_minified(results: Dict[str, Any]) -> str:
        """Format results as minified JSON (no spaces, no metadata)"""
        return JSONFormatter.format(results, pretty=False, include_metadata=False)
    
    @staticmethod
    def format_compact(results: Dict[str, Any]) -> str:
        """Format results as compact JSON (with metadata but no extra spaces)"""
        data = {
            'generated': datetime.now().isoformat(),
            'version': JSONFormatter.VERSION,
            'results': JSONFormatter._make_serializable(results)
        }
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False, default=str)
    
    @staticmethod
    async def save_to_file(results: Dict[str, Any], 
                          filepath: Union[str, Path],
                          pretty: bool = True,
                          compress: bool = False) -> Path:
        """
        Save formatted JSON to file
        
        Args:
            results: Results dictionary
            filepath: Path to save file
            pretty: Pretty print
            compress: Gzip compress the output
        """
        import aiofiles
        
        filepath = Path(filepath)
        json_str = JSONFormatter.format(results, pretty=pretty)
        
        if compress:
            filepath = filepath.with_suffix('.json.gz')
            async with aiofiles.open(filepath, 'wb') as f:
                compressed = gzip.compress(json_str.encode('utf-8'), compresslevel=6)
                await f.write(compressed)
        else:
            if not filepath.suffix:
                filepath = filepath.with_suffix('.json')
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json_str)
        
        return filepath
    
    @staticmethod
    def format_stream(results: Dict[str, Any]) -> str:
        """
        Format as JSONL (JSON Lines) for streaming - one module per line
        Useful for processing large datasets
        """
        lines = []
        serialized = JSONFormatter._make_serializable(results)
        
        for module_name, module_result in serialized.items():
            if module_name.startswith('_'):
                continue
            line = json.dumps({
                'module': module_name,
                'data': module_result,
                'timestamp': datetime.now().isoformat()
            }, ensure_ascii=False, default=str)
            lines.append(line)
        
        return '\n'.join(lines)
    
    @staticmethod
    def _make_serializable(obj: Any) -> Any:
        """Make object JSON serializable - improved version"""
        if isinstance(obj, dict):
            return {k: JSONFormatter._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [JSONFormatter._make_serializable(i) for i in obj]
        elif isinstance(obj, set):
            return sorted(list(obj))
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            # Handle custom objects
            return JSONFormatter._make_serializable(obj.__dict__)
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        else:
            # Fallback: convert to string
            return str(obj)
    
    @staticmethod
    def validate(json_str: str) -> bool:
        """Validate if string is valid JSON"""
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False
    
    @staticmethod
    def get_stats(json_str: str) -> Dict[str, Any]:
        """Get statistics about the JSON data"""
        if not JSONFormatter.validate(json_str):
            return {'error': 'Invalid JSON'}
        
        data = json.loads(json_str)
        
        def count_items(obj):
            if isinstance(obj, dict):
                return len(obj) + sum(count_items(v) for v in obj.values())
            elif isinstance(obj, list):
                return len(obj) + sum(count_items(i) for i in obj)
            return 0
        
        stats = {
            'size_bytes': len(json_str.encode('utf-8')),
            'size_kb': round(len(json_str.encode('utf-8')) / 1024, 2),
            'top_level_keys': len(data) if isinstance(data, dict) else 1,
            'total_items': count_items(data),
            'modules': [k for k in data.get('results', {}).keys() 
                       if not k.startswith('_')] if 'results' in data else []
        }
        
        return stats
    
    @staticmethod
    def merge(*json_strings: str) -> str:
        """Merge multiple JSON results into one"""
        merged_results = {}
        
        for json_str in json_strings:
            if not JSONFormatter.validate(json_str):
                continue
            data = json.loads(json_str)
            
            if 'results' in data:
                for key, value in data['results'].items():
                    if key not in merged_results:
                        merged_results[key] = value
        
        return JSONFormatter.format(merged_results)