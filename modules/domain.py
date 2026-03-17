#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Domain Module
domain investigation via DNS and HTTP
"""

import asyncio
import dns.asyncresolver
import dns.exception
import dns.reversename
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

from modules.base import BaseModule


class DomainModule(BaseModule):
    """Domain OSINT - Real DNS and HTTP checks"""
    
    def __init__(self, session):
        super().__init__(session)
        self.name = "domain"
    
    async def scan(self, domain: str) -> Dict:
        """Scan domain"""
        # Clean domain
        domain = domain.lower().strip()
        
        # Remove protocol and path
        if '://' in domain:
            domain = urlparse(domain).netloc
        
        # Remove www
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Remove port and path
        domain = domain.split(':')[0].split('/')[0]
        
        if not domain or '.' not in domain:
            return self.error_result(domain, "Invalid domain")
        
        result = {
            'domain': domain,
            'ip_addresses': [],
            'ipv6_addresses': [],
            'nameservers': [],
            'mx_records': [],
            'txt_records': [],
            'soa_record': None,
            'cname_record': None,
            'http_status': None,
            'https_status': None,
            'server_header': None,
            'title': None,
            'timestamp': datetime.now().isoformat()
        }
        
        resolver = dns.asyncresolver.Resolver()
        
        # A records (IPv4)
        try:
            answers = await resolver.resolve(domain, 'A')
            result['ip_addresses'] = [str(r) for r in answers]
        except dns.exception.DNSException:
            pass
        
        # AAAA records (IPv6)
        try:
            answers = await resolver.resolve(domain, 'AAAA')
            result['ipv6_addresses'] = [str(r) for r in answers]
        except:
            pass
        
        # NS records
        try:
            answers = await resolver.resolve(domain, 'NS')
            result['nameservers'] = [str(r).rstrip('.') for r in answers]
        except:
            pass
        
        # MX records
        try:
            answers = await resolver.resolve(domain, 'MX')
            for rdata in answers:
                result['mx_records'].append({
                    'exchange': str(rdata.exchange).rstrip('.'),
                    'priority': rdata.preference
                })
            # Sort by priority
            result['mx_records'].sort(key=lambda x: x['priority'])
        except:
            pass
        
        # TXT records
        try:
            answers = await resolver.resolve(domain, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    txt = txt_string.decode() if isinstance(txt_string, bytes) else str(txt_string)
                    result['txt_records'].append(txt)
        except:
            pass
        
        # SOA record
        try:
            answers = await resolver.resolve(domain, 'SOA')
            for rdata in answers:
                result['soa_record'] = {
                    'mname': str(rdata.mname).rstrip('.'),
                    'rname': str(rdata.rname).rstrip('.'),
                    'serial': rdata.serial,
                    'refresh': rdata.refresh,
                    'retry': rdata.retry,
                    'expire': rdata.expire,
                    'minimum': rdata.minimum
                }
        except:
            pass
        
        # CNAME record
        try:
            answers = await resolver.resolve(domain, 'CNAME')
            for rdata in answers:
                result['cname_record'] = str(rdata.target).rstrip('.')
        except:
            pass
        
        # Check HTTP/HTTPS
        async def check_protocol(proto: str) -> tuple:
            try:
                url = f"{proto}://{domain}"
                async with self.session.get(
                    url,
                    timeout=3,
                    allow_redirects=False,
                    ssl=False
                ) as resp:
                    return resp.status, dict(resp.headers)
            except:
                return None, {}
        
        # Try HTTPS first
        status, headers = await check_protocol('https')
        if status:
            result['https_status'] = status
            result['server_header'] = headers.get('Server')
        else:
            # Try HTTP
            status, headers = await check_protocol('http')
            if status:
                result['http_status'] = status
                result['server_header'] = headers.get('Server')
        
        # Get website title if available
        if result['http_status'] == 200 or result['https_status'] == 200:
            try:
                proto = 'https' if result['https_status'] == 200 else 'http'
                url = f"{proto}://{domain}"
                async with self.session.get(url, timeout=3) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        # Extract title
                        import re
                        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                        if title_match:
                            result['title'] = title_match.group(1).strip()[:200]
            except:
                pass
        
        sources = ['dns']
        if result['http_status'] or result['https_status']:
            sources.append('http')
        
        return self.create_result(domain, result, sources)