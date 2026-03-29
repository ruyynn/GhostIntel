#!/usr/bin/env python3
"""GhostIntel v2.5 - DNS helper with fallback nameservers and DoH support"""

import dns.asyncresolver
import dns.resolver
import asyncio
from typing import List, Optional, Dict, Any


class DNSHelper:
    """Enhanced DNS resolver with multiple fallback options"""
    
    # Public DNS servers (IPv4)
    PUBLIC_NAMESERVERS = [
        '8.8.8.8',      # Google Primary
        '8.8.4.4',      # Google Secondary
        '1.1.1.1',      # Cloudflare Primary
        '1.0.0.1',      # Cloudflare Secondary
        '9.9.9.9',      # Quad9
        '149.112.112.112', # Quad9 Secondary
        '208.67.222.222',  # OpenDNS
        '208.67.220.220',  # OpenDNS Secondary
        '77.88.8.8',      # Yandex DNS
        '77.88.8.1',      # Yandex DNS Secondary
        '185.228.168.9',  # CleanBrowsing
        '185.228.169.9',  # CleanBrowsing Secondary
        '94.140.14.14',   # AdGuard DNS
        '94.140.15.15',   # AdGuard DNS Secondary
    ]
    
    # DNS over HTTPS endpoints (for privacy)
    DOH_ENDPOINTS = [
        'https://cloudflare-dns.com/dns-query',
        'https://dns.google/dns-query',
        'https://dns.quad9.net/dns-query',
        'https://doh.opendns.com/dns-query',
        'https://doh.cleanbrowsing.org/doh/family-filter/',
        'https://dns.adguard.com/dns-query',
    ]
    
    # DNS over TLS servers
    DOT_SERVERS = [
        '1.1.1.1',      # Cloudflare
        '8.8.8.8',      # Google
        '9.9.9.9',      # Quad9
        '94.140.14.14', # AdGuard
    ]
    
    def __init__(self, timeout: float = 5.0, use_doh: bool = False):
        self.timeout = timeout
        self.lifetime = timeout * 2
        self.use_doh = use_doh
        self._resolver_cache = {}
    
    def make_resolver(self, nameservers: Optional[List[str]] = None) -> dns.asyncresolver.Resolver:
        """
        Create resolver with specified or default nameservers
        
        Args:
            nameservers: List of DNS server IPs, or None for defaults
        """
        r = dns.asyncresolver.Resolver(configure=False)
        
        if nameservers:
            r.nameservers = nameservers
        else:
            r.nameservers = self.PUBLIC_NAMESERVERS.copy()
        
        r.timeout = self.timeout
        r.lifetime = self.lifetime
        
        return r
    
    async def resolve_with_fallback(self, domain: str, qtype: str = 'A', 
                                    max_retries: int = 3) -> List[Any]:
        """
        Resolve DNS with multiple fallback nameservers
        
        Args:
            domain: Domain name to resolve
            qtype: DNS record type (A, AAAA, MX, etc.)
            max_retries: Maximum number of nameserver attempts
        
        Returns:
            List of resolved records, empty list if all fail
        """
        for i in range(min(max_retries, len(self.PUBLIC_NAMESERVERS))):
            try:
                # Try with different nameservers each attempt
                nameservers = self.PUBLIC_NAMESERVERS[i*2:(i+1)*2]
                if not nameservers:
                    nameservers = self.PUBLIC_NAMESERVERS[:2]
                
                resolver = self.make_resolver(nameservers)
                answer = await resolver.resolve(domain, qtype)
                return answer
                
            except dns.exception.DNSException:
                continue
            except Exception:
                continue
        
        return []
    
    async def resolve_multi(self, domain: str, qtypes: List[str]) -> Dict[str, List[Any]]:
        """
        Resolve multiple record types in parallel
        
        Args:
            domain: Domain name
            qtypes: List of DNS record types
        
        Returns:
            Dictionary mapping qtype to list of records
        """
        async def resolve_one(qtype):
            try:
                return qtype, await self.resolve_with_fallback(domain, qtype)
            except Exception:
                return qtype, []
        
        tasks = [resolve_one(qtype) for qtype in qtypes]
        results = await asyncio.gather(*tasks)
        
        return {qtype: records for qtype, records in results}
    
    async def get_all_records(self, domain: str) -> Dict[str, Any]:
        """
        Get all common DNS records for a domain
        
        Returns:
            Dictionary with A, AAAA, MX, NS, TXT, SOA, CNAME records
        """
        qtypes = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        return await self.resolve_multi(domain, qtypes)
    
    async def check_dnssec(self, domain: str) -> bool:
        """
        Check if domain has DNSSEC enabled
        """
        try:
            # Try to get RRSIG record
            result = await self.resolve_with_fallback(domain, 'RRSIG')
            return bool(result)
        except Exception:
            return False
    
    async def get_txt_records_parsed(self, domain: str) -> Dict[str, List[str]]:
        """
        Get and parse TXT records (SPF, DKIM, DMARC)
        
        Returns:
            Dictionary with spf, dkim, dmarc records
        """
        result = {
            'spf': [],
            'dkim': [],
            'dmarc': [],
            'other': []
        }
        
        txt_records = await self.resolve_with_fallback(domain, 'TXT')
        
        for r in txt_records:
            for s in r.strings:
                text = s.decode() if isinstance(s, bytes) else str(s)
                
                if text.startswith('v=spf1'):
                    result['spf'].append(text)
                elif 'v=DKIM1' in text or 'k=rsa' in text:
                    result['dkim'].append(text)
                elif text.startswith('v=DMARC1'):
                    result['dmarc'].append(text)
                else:
                    result['other'].append(text[:200])
        
        return result
    
    async def resolve_dmarc(self, domain: str) -> Optional[str]:
        """
        Resolve DMARC record specifically
        """
        dmarc_domain = f"_dmarc.{domain}"
        try:
            records = await self.resolve_with_fallback(dmarc_domain, 'TXT')
            for r in records:
                for s in r.strings:
                    text = s.decode() if isinstance(s, bytes) else str(s)
                    if text.startswith('v=DMARC1'):
                        return text
        except Exception:
            pass
        return None
    
    async def resolve_dkim(self, domain: str, selector: str = 'default') -> Optional[str]:
        """
        Resolve DKIM record for a specific selector
        
        Args:
            domain: Domain name
            selector: DKIM selector (e.g., 'default', 'google', 'k1')
        
        Returns:
            DKIM record if found, None otherwise
        """
        dkim_domain = f"{selector}._domainkey.{domain}"
        try:
            records = await self.resolve_with_fallback(dkim_domain, 'TXT')
            for r in records:
                for s in r.strings:
                    text = s.decode() if isinstance(s, bytes) else str(s)
                    if 'v=DKIM1' in text or 'k=rsa' in text:
                        return text
        except Exception:
            pass
        return None
    
    async def find_dkim_selector(self, domain: str) -> Optional[str]:
        """
        Try common DKIM selectors to find one that works
        
        Returns:
            First working selector or None
        """
        common_selectors = [
            'default', 'google', 'k1', 'mail', 'dkim', 'selector1',
            'selector2', '2016', '2017', '2018', '2019', '2020',
            's1', 's2', 's3', 'mx', 'pm', 'proton'
        ]
        
        for selector in common_selectors:
            result = await self.resolve_dkim(domain, selector)
            if result:
                return selector
        
        return None
    
    async def resolve_mx_priorities(self, domain: str) -> List[Dict[str, Any]]:
        """
        Resolve MX records with priorities sorted
        
        Returns:
            List of dicts with 'exchange' and 'priority'
        """
        mx_records = []
        try:
            answers = await self.resolve_with_fallback(domain, 'MX')
            for r in answers:
                mx_records.append({
                    'exchange': str(r.exchange).rstrip('.'),
                    'priority': r.preference
                })
            # Sort by priority
            mx_records.sort(key=lambda x: x['priority'])
        except Exception:
            pass
        
        return mx_records
    
    async def reverse_dns(self, ip: str) -> Optional[str]:
        """
        Perform reverse DNS lookup
        """
        try:
            import dns.reversename
            reverse_name = dns.reversename.from_address(ip)
            answers = await self.resolve_with_fallback(str(reverse_name), 'PTR')
            if answers:
                return str(answers[0]).rstrip('.')
        except Exception:
            pass
        return None


# Singleton instance for easy import
_default_helper = None


def make_resolver(timeout: float = 5.0, use_doh: bool = False) -> dns.asyncresolver.Resolver:
    """
    Create resolver with public DNS fallback (compatible with old API)
    
    Args:
        timeout: DNS query timeout in seconds
        use_doh: Whether to use DNS over HTTPS (requires aiohttp)
    
    Returns:
        dns.asyncresolver.Resolver instance
    """
    if use_doh:
        # For DoH, we need to use a different approach
        # This is a simplified version - full DoH would require aiohttp
        from warnings import warn
        warn("DNS over HTTPS requires additional configuration. Using standard DNS.")
    
    r = dns.asyncresolver.Resolver(configure=False)
    r.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4', '9.9.9.9']
    r.timeout = timeout
    r.lifetime = timeout * 2
    return r


def get_helper(timeout: float = 5.0, use_doh: bool = False) -> DNSHelper:
    """
    Get or create DNSHelper singleton
    
    Args:
        timeout: DNS query timeout
        use_doh: Whether to use DNS over HTTPS
    
    Returns:
        DNSHelper instance
    """
    global _default_helper
    if _default_helper is None:
        _default_helper = DNSHelper(timeout=timeout, use_doh=use_doh)
    return _default_helper