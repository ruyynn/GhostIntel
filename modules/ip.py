#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - IP Module
IP investigation via RDAP, whois, and DNS
"""

import socket
import ipaddress
import asyncio
from typing import Dict, Optional
from datetime import datetime
import aiohttp

from modules.base import BaseModule


class IPModule(BaseModule):
    """IP OSINT - Real RDAP, reverse DNS, and geolocation"""
    
    def __init__(self, session):
        super().__init__(session)
        self.name = "ip"
        
        # Free geolocation API (no key required)
        self.geo_api = "http://ip-api.com/json/{}"
        
        # RDAP servers by region
        self.rdap_servers = {
            'ARIN': 'https://rdap.arin.net/registry/ip/{}',
            'RIPE': 'https://rdap.db.ripe.net/ip/{}',
            'APNIC': 'https://rdap.apnic.net/ip/{}',
            'LACNIC': 'https://rdap.lacnic.net/rdap/ip/{}',
            'AFRINIC': 'https://rdap.afrinic.net/rdap/ip/{}'
        }
    
    async def scan(self, target: str) -> Dict:
        """Scan IP address"""
        # Try to resolve if domain
        ip = target
        try:
            ip_obj = ipaddress.ip_address(ip)
        except ValueError:
            try:
                ip = socket.gethostbyname(target)
                ip_obj = ipaddress.ip_address(ip)
            except:
                return self.error_result(target, "Invalid IP or hostname")
        
        result = {
            'ip': ip,
            'version': ip_obj.version,
            'is_private': ip_obj.is_private,
            'is_loopback': ip_obj.is_loopback,
            'is_multicast': ip_obj.is_multicast,
            'reverse_dns': None,
            'geo': {},
            'rdap': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Reverse DNS
        try:
            result['reverse_dns'] = socket.gethostbyaddr(ip)[0]
        except:
            pass
        
        # Geolocation for public IPs
        if not ip_obj.is_private and not ip_obj.is_loopback:
            geo_data = await self._get_geolocation(ip)
            if geo_data:
                result['geo'] = geo_data
                # Flatten some fields for easy access
                result['country'] = geo_data.get('country')
                result['city'] = geo_data.get('city')
                result['isp'] = geo_data.get('isp')
                result['org'] = geo_data.get('org')
                result['asn'] = geo_data.get('as')
                result['lat'] = geo_data.get('lat')
                result['lon'] = geo_data.get('lon')
            
            # RDAP lookup
            rdap_data = await self._rdap_lookup(ip)
            if rdap_data:
                result['rdap'] = rdap_data
        
        sources = ['dns']
        if result['geo']:
            sources.append('ip-api.com')
        if result['rdap']:
            sources.append('rdap')
        
        return self.create_result(ip, result, sources)
    
    async def _get_geolocation(self, ip: str) -> Optional[Dict]:
        """Get geolocation from ip-api.com (free, no key)"""
        try:
            async with self.session.get(
                self.geo_api.format(ip),
                timeout=3
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('status') == 'success':
                        return {
                            'country': data.get('country'),
                            'countryCode': data.get('countryCode'),
                            'region': data.get('regionName'),
                            'city': data.get('city'),
                            'zip': data.get('zip'),
                            'lat': data.get('lat'),
                            'lon': data.get('lon'),
                            'timezone': data.get('timezone'),
                            'isp': data.get('isp'),
                            'org': data.get('org'),
                            'as': data.get('as'),
                            'mobile': data.get('mobile', False),
                            'proxy': data.get('proxy', False),
                            'hosting': data.get('hosting', False)
                        }
        except:
            pass
        return None
    
    async def _rdap_lookup(self, ip: str) -> Dict:
        """RDAP lookup for IP information"""
        rdap_result = {}
        
        for rir, url in self.rdap_servers.items():
            try:
                async with self.session.get(
                    url.format(ip),
                    timeout=3,
                    headers={'Accept': 'application/json'}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        rdap_result['rir'] = rir
                        
                        if 'handle' in data:
                            rdap_result['handle'] = data['handle']
                        
                        if 'name' in data:
                            rdap_result['network'] = data['name']
                        
                        # Extract organization
                        if 'entities' in data:
                            for entity in data['entities']:
                                if 'vcardArray' in entity:
                                    for vcard in entity['vcardArray'][1:]:
                                        if vcard[0] == 'fn':
                                            rdap_result['organization'] = vcard[3]
                                        elif vcard[0] == 'email':
                                            rdap_result['email'] = vcard[3]
                        
                        # Get events
                        if 'events' in data:
                            for event in data['events']:
                                action = event.get('eventAction')
                                date = event.get('eventDate')
                                if action == 'registration':
                                    rdap_result['registered'] = date
                                elif action == 'last changed':
                                    rdap_result['changed'] = date
                        
                        break  # Stop after first successful
            except:
                continue
        
        return rdap_result