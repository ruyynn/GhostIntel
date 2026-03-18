#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Correlation Engine
Connects intelligence from different modules
"""

import re
from typing import Dict, List, Any, Set
from collections import defaultdict


class CorrelationEngine:
    """Correlates data from multiple OSINT modules"""
    
    def __init__(self):
        self.entities = defaultdict(set)
        self.connections = []
    
    def correlate(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Correlate data from all modules
        Returns connected intelligence graph
        """
        self.entities.clear()
        self.connections = []
        
        # Extract all entities
        for module_name, result in results.items():
            if not result or 'data' not in result:
                continue
            
            data = result['data']
            
            if module_name == 'username':
                self._correlate_username(data)
            elif module_name == 'email':
                self._correlate_email(data)
            elif module_name == 'phone':
                self._correlate_phone(data)
            elif module_name == 'domain':
                self._correlate_domain(data)
            elif module_name == 'ip':
                self._correlate_ip(data)
        
        # Convert sets to lists for JSON serialization
        entities_serializable = {}
        for etype, entity_set in self.entities.items():
            entities_serializable[etype] = sorted(list(entity_set))
        
        # Build correlation result
        correlation = {
            'primary': self._get_primary_entity(results),
            'entities': entities_serializable,  # Sudah dalam bentuk list
            'connections': self.connections,
            'summary': self._generate_summary()
        }
        
        return correlation
    
    def _correlate_username(self, data: Dict):
        """Extract entities from username results"""
        username = data.get('username')
        if username:
            self.entities['username'].add(username)
        
        # Add emails from possible emails
        for email in data.get('possible_emails', [])[:5]:
            if '@' in email:
                self.entities['email'].add(email)
                domain = email.split('@')[1]
                self.entities['domain'].add(domain)
        
        # Add platforms
        for profile in data.get('found', []):
            platform = profile.get('platform')
            if platform:
                self.entities['platform'].add(platform)
    
    def _correlate_email(self, data: Dict):
        """Extract entities from email results"""
        email = data.get('email')
        if email:
            self.entities['email'].add(email)
            
            # Extract username and domain
            if '@' in email:
                username, domain = email.split('@')
                self.entities['username'].add(username)
                self.entities['domain'].add(domain)
        
        # Add MX records as domains
        for mx in data.get('mx_records', []):
            exchange = mx.get('exchange') if isinstance(mx, dict) else mx
            if exchange:
                self.entities['mail_server'].add(exchange)
    
    def _correlate_phone(self, data: Dict):
        """Extract entities from phone results"""
        phone = data.get('e164') or data.get('input')
        if phone:
            self.entities['phone'].add(phone)
        
        # Add provider
        provider = data.get('provider')
        if provider and provider != 'Unknown':
            self.entities['provider'].add(provider)
        
        # Add country
        country = data.get('country_iso')
        if country:
            self.entities['country'].add(country)
    
    def _correlate_domain(self, data: Dict):
        """Extract entities from domain results"""
        domain = data.get('domain')
        if domain:
            self.entities['domain'].add(domain)
        
        # Add IPs
        for ip in data.get('ip_addresses', []):
            self.entities['ip'].add(ip)
        
        # Add nameservers as domains
        for ns in data.get('nameservers', []):
            self.entities['nameserver'].add(ns)
        
        # Add MX exchanges
        for mx in data.get('mx_records', []):
            exchange = mx.get('exchange') if isinstance(mx, dict) else mx
            if exchange:
                self.entities['mail_server'].add(exchange)
    
    def _correlate_ip(self, data: Dict):
        """Extract entities from IP results"""
        ip = data.get('ip')
        if ip:
            self.entities['ip'].add(ip)
        
        # Add reverse DNS
        rdns = data.get('reverse_dns')
        if rdns:
            self.entities['domain'].add(rdns)
        
        # Add ASN
        asn = data.get('asn')
        if asn:
            self.entities['asn'].add(asn)
        
        # Add ISP
        isp = data.get('isp')
        if isp:
            self.entities['isp'].add(isp)
    
    def _get_primary_entity(self, results: Dict) -> str:
        """Get the primary entity being investigated"""
        for module, result in results.items():
            if result and 'target' in result:
                return result['target']
        return "Unknown"
    
    def _generate_summary(self) -> Dict[str, int]:
        """Generate summary of found entities"""
        return {
            entity_type: len(items)
            for entity_type, items in self.entities.items()
        }