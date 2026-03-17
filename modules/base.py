#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Base Module
All modules inherit from this class
"""

from datetime import datetime
from typing import Dict, Any, Optional


class BaseModule:
    """Base class for all OSINT modules"""
    
    def __init__(self, session):
        self.session = session
        self.name = "base"
    
    async def scan(self, target: str) -> Dict[str, Any]:
        """
        Scan target and return results
        To be implemented by child classes
        """
        raise NotImplementedError
    
    def create_result(self, target: str, data: Dict, sources: list) -> Dict:
        """Create standardized result dictionary"""
        return {
            'module': self.name,
            'target': target,
            'data': data,
            'sources': sources,
            'timestamp': datetime.now().isoformat()
        }
    
    def error_result(self, target: str, error: str) -> Dict:
        """Create error result"""
        return {
            'module': self.name,
            'target': target,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }