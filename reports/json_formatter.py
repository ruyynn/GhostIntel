#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - JSON Formatter
Format results as JSON
"""

import json
from datetime import datetime
from typing import Dict, Any


class JSONFormatter:
    """Format results as JSON"""
    
    @staticmethod
    def format(results: Dict[str, Any]) -> str:
        """Format results to JSON string"""
        data = {
            'generated': datetime.now().isoformat(),
            'version': '2.0.0',
            'results': JSONFormatter._make_serializable(results)
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def _make_serializable(obj: Any) -> Any:
        """Make object JSON serializable"""
        if isinstance(obj, dict):
            return {k: JSONFormatter._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [JSONFormatter._make_serializable(i) for i in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return str(obj)