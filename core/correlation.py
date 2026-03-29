#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.5 - Correlation Engine
Connects intelligence from different modules with relationship mapping
"""

import re
from typing import Dict, List, Any, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class CorrelationEngine:
    """Correlates data from multiple OSINT modules - Enhanced v2.5"""
    
    def __init__(self):
        self.entities = defaultdict(set)
        self.connections = []
        self.relationships = defaultdict(list)  # Store relationships between entities
        self.confidence_scores = defaultdict(float)  # Confidence in correlations
        
    def correlate(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Correlate data from all modules
        Returns connected intelligence graph
        """
        self.entities.clear()
        self.connections = []
        self.relationships.clear()
        self.confidence_scores.clear()
        
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
        
        # Build relationship graph
        self._build_relationships()
        
        # Calculate correlation confidence
        self._calculate_confidence()
        
        # Convert sets to lists for JSON serialization
        entities_serializable = {}
        for etype, entity_set in self.entities.items():
            entities_serializable[etype] = sorted(list(entity_set))
        
        # Build correlation result
        correlation = {
            'primary': self._get_primary_entity(results),
            'entities': entities_serializable,
            'connections': self.connections,
            'relationships': dict(self.relationships),
            'summary': self._generate_summary(),
            'confidence': dict(self.confidence_scores),
            'graph': self._build_graph(),
            'timestamp': datetime.now().isoformat()
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
                # Create relationship
                if username:
                    self.relationships[f"{username}→{email}"].append('possible_email')
        
        # Add platforms and profile names
        for profile in data.get('found', []):
            platform = profile.get('platform')
            if platform:
                self.entities['platform'].add(platform)
                if username:
                    self.relationships[f"{username}→{platform}"].append('profile_on')
            
            # Extract profile name if different from username
            profile_name = profile.get('profile_name')
            if profile_name and profile_name != username:
                self.entities['profile_name'].add(profile_name)
                if username:
                    self.relationships[f"{username}→{profile_name}"].append('alias')
        
        # Add categories
        for cat in data.get('categories', []):
            self.entities['category'].add(cat)
    
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
                self.relationships[f"{email}→{username}"].append('username_from_email')
                self.relationships[f"{email}→{domain}"].append('domain_from_email')
        
        # Add MX records as domains
        for mx in data.get('mx_records', []):
            exchange = mx.get('exchange') if isinstance(mx, dict) else mx
            if exchange:
                self.entities['mail_server'].add(exchange)
                if email:
                    self.relationships[f"{email}→{exchange}"].append('mail_server')
        
        # Add breach info
        if data.get('breach_info') and data['breach_info'].get('has_breaches'):
            for breach in data['breach_info'].get('breaches', []):
                breach_name = breach.get('name')
                if breach_name:
                    self.entities['breach'].add(breach_name)
                    if email:
                        self.relationships[f"{email}→{breach_name}"].append('breached_in')
        
        # Add gravatar if exists
        if data.get('gravatar'):
            self.entities['gravatar'].add(data['gravatar'])
    
    def _correlate_phone(self, data: Dict):
        """Extract entities from phone results"""
        phone = data.get('e164') or data.get('input')
        if phone:
            self.entities['phone'].add(phone)
        
        # Add provider
        provider = data.get('provider')
        if provider and provider != 'Unknown':
            self.entities['provider'].add(provider)
            if phone:
                self.relationships[f"{phone}→{provider}"].append('carrier')
        
        # Add country
        country = data.get('country_iso')
        if country:
            self.entities['country'].add(country)
            if phone:
                self.relationships[f"{phone}→{country}"].append('located_in')
        
        # Add location
        location = data.get('location')
        if location and location != data.get('country'):
            self.entities['location'].add(location)
            if phone:
                self.relationships[f"{phone}→{location}"].append('located_in')
        
        # Add possible handles
        for handle in data.get('possible_handles', []):
            self.entities['possible_handle'].add(handle)
            if phone:
                self.relationships[f"{phone}→{handle}"].append('possible_handle')
    
    def _correlate_domain(self, data: Dict):
        """Extract entities from domain results"""
        domain = data.get('domain')
        if domain:
            self.entities['domain'].add(domain)
        
        # Add IPs
        for ip in data.get('ip_addresses', []):
            self.entities['ip'].add(ip)
            if domain:
                self.relationships[f"{domain}→{ip}"].append('resolves_to')
        
        # Add nameservers as domains
        for ns in data.get('nameservers', []):
            self.entities['nameserver'].add(ns)
            if domain:
                self.relationships[f"{domain}→{ns}"].append('nameserver')
        
        # Add MX exchanges
        for mx in data.get('mx_records', []):
            exchange = mx.get('exchange') if isinstance(mx, dict) else mx
            if exchange:
                self.entities['mail_server'].add(exchange)
                if domain:
                    self.relationships[f"{domain}→{exchange}"].append('mail_server')
        
        # Add technologies
        for tech in data.get('technologies', []):
            self.entities['technology'].add(tech)
            if domain:
                self.relationships[f"{domain}→{tech}"].append('uses_tech')
        
        # Add SSL issuer
        ssl_info = data.get('ssl_info', {})
        if ssl_info.get('issuer'):
            issuer = ssl_info['issuer']
            self.entities['ssl_issuer'].add(issuer)
            if domain:
                self.relationships[f"{domain}→{issuer}"].append('ssl_issued_by')
        
        # Add CNAME
        if data.get('cname_record'):
            cname = data['cname_record']
            self.entities['domain'].add(cname)
            if domain:
                self.relationships[f"{domain}→{cname}"].append('cname_to')
    
    def _correlate_ip(self, data: Dict):
        """Extract entities from IP results"""
        ip = data.get('ip')
        if ip:
            self.entities['ip'].add(ip)
        
        # Add reverse DNS
        rdns = data.get('reverse_dns')
        if rdns:
            self.entities['domain'].add(rdns)
            if ip:
                self.relationships[f"{ip}→{rdns}"].append('ptr_record')
        
        # Add ASN
        asn = data.get('asn')
        if asn:
            self.entities['asn'].add(asn)
            if ip:
                self.relationships[f"{ip}→{asn}"].append('belongs_to_asn')
        
        # Add ISP
        isp = data.get('isp')
        if isp:
            self.entities['isp'].add(isp)
            if ip:
                self.relationships[f"{ip}→{isp}"].append('isp')
        
        # Add organization
        org = data.get('org')
        if org and org != isp:
            self.entities['organization'].add(org)
            if ip:
                self.relationships[f"{ip}→{org}"].append('owned_by')
        
        # Add RDAP organization
        rdap = data.get('rdap', {})
        if rdap.get('organization'):
            org_name = rdap['organization']
            self.entities['rdap_org'].add(org_name)
            if ip:
                self.relationships[f"{ip}→{org_name}"].append('registered_to')
        
        # Add abuse contact
        if data.get('abuse_contact'):
            self.entities['abuse_contact'].add(data['abuse_contact'])
            if ip:
                self.relationships[f"{ip}→{data['abuse_contact']}"].append('abuse_contact')
    
    def _build_relationships(self):
        """Build relationship graph between entities"""
        # Connect emails to domains
        for email in self.entities.get('email', []):
            if '@' in email:
                domain = email.split('@')[1]
                if domain in self.entities.get('domain', set()):
                    self.connections.append(f"{email} → {domain}")
        
        # Connect domains to IPs
        for domain in self.entities.get('domain', []):
            for ip in self.entities.get('ip', []):
                # This is a potential connection - actual verification would need DNS
                # But for correlation, we'll add it if there's any relationship
                if any(f"{domain}→{ip}" in str(r) for r in self.relationships.values()):
                    self.connections.append(f"{domain} → {ip}")
        
        # Connect usernames to emails
        for username in self.entities.get('username', []):
            for email in self.entities.get('email', []):
                if username in email:
                    self.connections.append(f"{username} → {email}")
        
        # Connect phones to providers
        for phone in self.entities.get('phone', []):
            for provider in self.entities.get('provider', []):
                self.connections.append(f"{phone} → {provider}")
        
        # Connect IPs to ASNs
        for ip in self.entities.get('ip', []):
            for asn in self.entities.get('asn', []):
                self.connections.append(f"{ip} → {asn}")
    
    def _calculate_confidence(self):
        """Calculate confidence scores for correlations"""
        for entity_type, entities in self.entities.items():
            for entity in entities:
                # Base confidence
                base_conf = 0.5
                
                # Increase confidence if entity appears in multiple contexts
                connection_count = len([c for c in self.connections if entity in c])
                if connection_count > 3:
                    base_conf += 0.3
                elif connection_count > 1:
                    base_conf += 0.15
                
                # Check if entity is primary
                if entity == self._get_primary_entity({}):
                    base_conf += 0.2
                
                self.confidence_scores[entity] = min(base_conf, 1.0)
    
    def _build_graph(self) -> Dict[str, List[str]]:
        """Build a graph representation of correlations"""
        graph = defaultdict(list)
        
        for connection in self.connections:
            if ' → ' in connection:
                source, target = connection.split(' → ')
                graph[source].append(target)
        
        return dict(graph)
    
    def _get_primary_entity(self, results: Dict) -> str:
        """Get the primary entity being investigated"""
        for module, result in results.items():
            if result and 'target' in result:
                return result['target']
        return "Unknown"
    
    def _generate_summary(self) -> Dict[str, int]:
        """Generate summary of found entities"""
        summary = {
            entity_type: len(items)
            for entity_type, items in self.entities.items()
        }
        
        # Add connection count
        summary['total_connections'] = len(self.connections)
        
        return summary
    
    def find_related(self, entity: str) -> List[str]:
        """
        Find all entities related to a given entity
        """
        related = set()
        
        for connection in self.connections:
            if connection.startswith(f"{entity} → "):
                related.add(connection.split(' → ')[1])
            elif connection.endswith(f" → {entity}"):
                related.add(connection.split(' → ')[0])
        
        return sorted(list(related))
    
    def get_entity_count(self) -> int:
        """Get total number of unique entities"""
        return sum(len(items) for items in self.entities.values())
    
    def export_graph(self) -> Dict[str, Any]:
        """
        Export correlation graph for visualization
        Suitable for tools like Graphviz, D3.js, etc.
        """
        nodes = []
        for etype, entities in self.entities.items():
            for entity in entities:
                nodes.append({
                    'id': entity,
                    'type': etype,
                    'confidence': self.confidence_scores.get(entity, 0.5)
                })
        
        edges = []
        for connection in self.connections:
            if ' → ' in connection:
                source, target = connection.split(' → ')
                edges.append({
                    'source': source,
                    'target': target,
                    'type': 'correlates'
                })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'total_entities': len(nodes),
                'total_connections': len(edges),
                'timestamp': datetime.now().isoformat()
            }
        }