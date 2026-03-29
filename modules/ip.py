#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - IP Module (upgraded)"""

import socket
import ipaddress
import asyncio
from typing import Dict, Optional
from datetime import datetime
import aiohttp
from modules.base import BaseModule


class IPModule(BaseModule):
    def __init__(self, session):
        super().__init__(session)
        self.name = "ip"
        
        # Geolocation APIs (free, no key required)
        self.geo_apis = [
            "http://ip-api.com/json/{}?fields=status,message,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,asname,mobile,proxy,hosting,query",
            "https://ipapi.co/{}/json/",
            "https://ipinfo.io/{}/json",  # Free tier with limited requests
        ]
        
        # RDAP servers for all RIRs
        self.rdap_servers = [
            'https://rdap.arin.net/registry/ip/{}',      # North America
            'https://rdap.db.ripe.net/ip/{}',            # Europe, Middle East, Central Asia
            'https://rdap.apnic.net/ip/{}',              # Asia Pacific
            'https://rdap.lacnic.net/rdap/ip/{}',        # Latin America
            'https://rdap.afrinic.net/rdap/ip/{}',       # Africa
        ]
        
        # Simple cache untuk mengurangi request duplikat
        self._cache = {}
        self._cache_ttl = 3600  # 1 hour cache

    async def scan(self, target: str) -> Dict:
        ip = target.strip()
        
        # Check cache
        cache_key = f"ip_{ip}"
        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if (datetime.now() - cached_time).total_seconds() < self._cache_ttl:
                return cached_result
        
        try:
            ip_obj = ipaddress.ip_address(ip)
        except ValueError:
            try:
                ip = socket.gethostbyname(target.strip())
                ip_obj = ipaddress.ip_address(ip)
            except Exception:
                return self.error_result(target, "Invalid IP or hostname")

        result = {
            'ip': ip,
            'input': target,
            'version': ip_obj.version,
            'is_private': ip_obj.is_private,
            'is_loopback': ip_obj.is_loopback,
            'is_multicast': ip_obj.is_multicast,
            'is_global': ip_obj.is_global,
            'is_reserved': ip_obj.is_reserved,
            'reverse_dns': None,
            'country': None, 'country_code': None,
            'region': None, 'city': None, 'zip': None,
            'lat': None, 'lon': None,
            'timezone': None,
            'isp': None, 'org': None,
            'asn': None, 'asn_name': None,
            'is_mobile': False,
            'is_proxy': False,
            'is_hosting': False,
            'is_crawler': False,
            'is_tor': False,
            'rdap': {},
            'abuse_contact': None,
            'risk_score': None,  # 0-100, higher = more risky
            'timestamp': datetime.now().isoformat()
        }

        # Reverse DNS
        try:
            result['reverse_dns'] = socket.gethostbyaddr(ip)[0]
        except Exception:
            pass

        if not ip_obj.is_private and not ip_obj.is_loopback and not ip_obj.is_reserved:
            geo, rdap = await asyncio.gather(
                self._geolocate(ip),
                self._rdap(ip)
            )
            if geo:
                result.update(geo)
            if rdap:
                result['rdap'] = rdap
                if rdap.get('abuse_email'):
                    result['abuse_contact'] = rdap['abuse_email']
            
            # Calculate risk score based on available data
            result['risk_score'] = self._calculate_risk_score(result)
        else:
            result['note'] = 'Private/loopback/reserved IP — limited data available'

        sources = ['reverse_dns']
        if result.get('country'):
            sources.append('ip-api.com')
        if result.get('rdap'):
            sources.append('rdap')
        
        final_result = self.create_result(ip, result, sources)
        
        # Cache result
        self._cache[cache_key] = (datetime.now(), final_result)
        
        return final_result

    async def _geolocate(self, ip: str) -> Optional[Dict]:
        """Get geolocation data from multiple APIs with fallback"""
        
        # Try ip-api.com first (fastest, most detailed)
        try:
            async with self.session.get(
                self.geo_apis[0].format(ip),
                timeout=aiohttp.ClientTimeout(total=5)
            ) as r:
                if r.status == 200:
                    d = await r.json()
                    if d.get('status') == 'success':
                        return {
                            'country': d.get('country'),
                            'country_code': d.get('countryCode'),
                            'region': d.get('regionName'),
                            'city': d.get('city'),
                            'zip': d.get('zip'),
                            'lat': d.get('lat'),
                            'lon': d.get('lon'),
                            'timezone': d.get('timezone'),
                            'isp': d.get('isp'),
                            'org': d.get('org'),
                            'asn': d.get('as', '').split()[0] if d.get('as') else None,
                            'asn_name': d.get('asname'),
                            'is_mobile': d.get('mobile', False),
                            'is_proxy': d.get('proxy', False),
                            'is_hosting': d.get('hosting', False),
                        }
        except Exception:
            pass

        # Fallback: ipapi.co
        try:
            async with self.session.get(
                self.geo_apis[1].format(ip),
                timeout=aiohttp.ClientTimeout(total=5)
            ) as r:
                if r.status == 200:
                    d = await r.json()
                    if not d.get('error'):
                        return {
                            'country': d.get('country_name'),
                            'country_code': d.get('country_code'),
                            'region': d.get('region'),
                            'city': d.get('city'),
                            'zip': d.get('postal'),
                            'lat': d.get('latitude'),
                            'lon': d.get('longitude'),
                            'timezone': d.get('timezone'),
                            'isp': d.get('org'),
                            'org': d.get('org'),
                            'asn': d.get('asn'),
                            'asn_name': None,
                            'is_mobile': d.get('mobile', False),
                            'is_proxy': d.get('proxy', False),
                            'is_hosting': d.get('hosting', False),
                        }
        except Exception:
            pass

        # Second fallback: ipinfo.io (limited but free)
        try:
            async with self.session.get(
                self.geo_apis[2].format(ip),
                timeout=aiohttp.ClientTimeout(total=5)
            ) as r:
                if r.status == 200:
                    d = await r.json()
                    if d and 'country' in d:
                        # Parse ASN from org field (e.g., "AS15169 Google LLC")
                        asn = None
                        asn_name = None
                        org = d.get('org', '')
                        if org and org.startswith('AS'):
                            parts = org.split(' ', 1)
                            asn = parts[0]
                            if len(parts) > 1:
                                asn_name = parts[1]
                        
                        return {
                            'country': d.get('country'),
                            'country_code': d.get('country'),
                            'region': d.get('region'),
                            'city': d.get('city'),
                            'zip': d.get('postal'),
                            'lat': float(d.get('loc', '0,0').split(',')[0]) if d.get('loc') else None,
                            'lon': float(d.get('loc', '0,0').split(',')[1]) if d.get('loc') else None,
                            'timezone': d.get('timezone'),
                            'isp': d.get('org'),
                            'org': d.get('org'),
                            'asn': asn,
                            'asn_name': asn_name,
                            'is_mobile': False,
                            'is_proxy': False,
                            'is_hosting': False,
                        }
        except Exception:
            pass
            
        return None

    async def _rdap(self, ip: str) -> Dict:
        """RDAP lookup with multiple RIR servers"""
        for url_tpl in self.rdap_servers:
            try:
                async with self.session.get(
                    url_tpl.format(ip),
                    timeout=aiohttp.ClientTimeout(total=5),
                    headers={'Accept': 'application/rdap+json'}
                ) as r:
                    if r.status == 200:
                        d = await r.json(content_type=None)
                        info = {}
                        info['rir'] = url_tpl.split('/')[2].split('.')[0].upper()
                        info['handle'] = d.get('handle')
                        info['network'] = d.get('name')
                        info['type'] = d.get('type')
                        info['start_address'] = d.get('startAddress')
                        info['end_address'] = d.get('endAddress')
                        info['ip_version'] = d.get('ipVersion')

                        # Extract organization and abuse contact from entities
                        for ent in d.get('entities', []):
                            roles = ent.get('roles', [])
                            vcard = ent.get('vcardArray', [None, []])[1]
                            for field in vcard:
                                if not isinstance(field, list):
                                    continue
                                if field[0] == 'fn' and 'organization' not in info:
                                    if any(r in roles for r in ['registrant', 'administrative', 'technical']):
                                        info['organization'] = field[3]
                                if field[0] == 'email':
                                    if 'abuse' in roles:
                                        info['abuse_email'] = field[3]
                                    elif 'administrative' in roles and 'abuse_email' not in info:
                                        info['admin_email'] = field[3]
                                if field[0] == 'tel' and 'abuse' in roles:
                                    info['abuse_phone'] = field[3]

                        # Events
                        for ev in d.get('events', []):
                            action = ev.get('eventAction')
                            date = ev.get('eventDate', '')[:10]
                            if action == 'registration':
                                info['registered'] = date
                            elif action == 'last changed':
                                info['last_changed'] = date
                            elif action == 'expiration':
                                info['expires'] = date

                        # Remarks/notices
                        if d.get('remarks'):
                            info['remarks'] = d.get('remarks')[0].get('description', [''])[0][:200]

                        return info
            except Exception:
                continue
        return {}

    def _calculate_risk_score(self, data: Dict) -> int:
        """
        Calculate risk score (0-100) based on IP attributes
        Higher score = more suspicious/risky
        """
        score = 0
        
        # Proxy/VPN detection (+30)
        if data.get('is_proxy'):
            score += 30
        
        # Hosting/Data center (+20)
        if data.get('is_hosting'):
            score += 20
        
        # Mobile network (+5 - less risky but still dynamic)
        if data.get('is_mobile'):
            score += 5
        
        # No reverse DNS (+10)
        if not data.get('reverse_dns'):
            score += 10
        
        # No abuse contact (+15)
        if not data.get('abuse_contact'):
            score += 15
        
        # Private/unknown ASN (+10)
        if not data.get('asn'):
            score += 10
        
        # Cap at 100
        return min(score, 100)
    
    async def bulk_lookup(self, ips: list) -> Dict[str, Dict]:
        """Bulk IP lookup (for multiple IPs)"""
        results = {}
        tasks = [self.scan(ip) for ip in ips]
        scan_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for ip, result in zip(ips, scan_results):
            if isinstance(result, dict) and not result.get('error'):
                results[ip] = result
            else:
                results[ip] = {'error': str(result) if result else 'Lookup failed'}
        
        return results
    
    def clear_cache(self):
        """Clear the IP lookup cache"""
        self._cache.clear()