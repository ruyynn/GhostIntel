#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Domain Module (upgraded)"""

import asyncio
import re
import ssl
import socket
import aiohttp
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse
import dns.asyncresolver
import dns.exception
import dns.rdatatype
from modules.base import BaseModule


class DomainModule(BaseModule):
    def __init__(self, session):
        super().__init__(session)
        self.name = "domain"
        
        # Expanded technology detection patterns
        self.tech_patterns = {
            # CMS
            'WordPress': ['wp-content', 'wp-includes', 'wp-json', 'wordpress'],
            'Joomla': ['joomla', 'com_content', 'com_users'],
            'Drupal': ['drupal', 'sites/default', 'core/misc'],
            'Magento': ['magento', 'skin/frontend', 'Mage.Cookies'],
            'Shopify': ['cdn.shopify', 'myshopify.com', 'shopify'],
            'Wix': ['wix.com', 'wix-static', 'wix-code'],
            'Squarespace': ['squarespace', 'static.squarespace'],
            'Ghost': ['ghost.org', 'ghost-blog'],
            
            # JavaScript Frameworks
            'React': ['react', '_reactRoot', 'react-dom'],
            'Vue.js': ['__vue', 'vue.js', 'vue-router', 'vuex'],
            'Angular': ['ng-version', 'ng-app', 'angular'],
            'Next.js': ['__next', 'next.js', '_next/static'],
            'Nuxt.js': ['__nuxt', 'nuxt.js', '_nuxt/'],
            'Svelte': ['__svelte', 'svelte-'],
            'Alpine.js': ['x-data', 'alpine'],
            'HTMX': ['htmx', 'hx-'],
            
            # Libraries
            'jQuery': ['jquery', 'jQuery'],
            'Bootstrap': ['bootstrap', 'bs.'],
            'Tailwind': ['tailwind', 'tw-'],
            'FontAwesome': ['fontawesome', 'fa-'],
            'Google Fonts': ['fonts.googleapis', 'fonts.gstatic'],
            
            # Backend
            'PHP': ['.php', 'PHPSESSID'],
            'Python': ['python', 'django', 'flask'],
            'Ruby on Rails': ['rails', 'ruby', '.rb'],
            'Node.js': ['node', 'express'],
            'Java': ['.jsp', 'JSESSIONID', 'java'],
            'ASP.NET': ['.aspx', 'ASP.NET', '__VIEWSTATE'],
            
            # CDN & Security
            'Cloudflare': ['cloudflare', '__cfduid', 'cf-ray'],
            'Fastly': ['fastly', 'x-served-by'],
            'AWS CloudFront': ['cloudfront', 'x-amz-cf'],
            'Akamai': ['akamai', 'akamaiedge'],
            'Incapsula': ['incapsula', 'visid_incap'],
            'Sucuri': ['sucuri', 'x-sucuri-id'],
            
            # Servers
            'nginx': ['nginx', 'nginx/'],
            'Apache': ['apache', 'apache/'],
            'IIS': ['iis', 'microsoft-iis'],
            'LiteSpeed': ['litespeed', 'lscache'],
            'Caddy': ['caddy', 'caddy/'],
            'OpenResty': ['openresty'],
            
            # E-commerce
            'WooCommerce': ['woocommerce', 'wc-'],
            'BigCommerce': ['bigcommerce', 'bc-'],
            'PrestaShop': ['prestashop', 'ps_'],
            'OpenCart': ['opencart', 'route=common'],
            
            # Analytics
            'Google Analytics': ['google-analytics', 'ga.js', 'gtag'],
            'Facebook Pixel': ['fbq(', 'facebook-pixel'],
            'Hotjar': ['hotjar', 'hj-'],
            'Matomo': ['matomo', 'piwik'],
            
            # Payment
            'Stripe': ['stripe', 'js.stripe'],
            'PayPal': ['paypal', 'paypalobjects'],
            'Midtrans': ['midtrans', 'veritrans'],
            'Xendit': ['xendit'],
            
            # Indonesian
            'Tokopedia': ['tokopedia', 'tokocdn'],
            'Bukalapak': ['bukalapak', 'blibli'],
            'Traveloka': ['traveloka', 'tiket'],
            'Gojek': ['gojek', 'gopay'],
        }

    async def scan(self, domain: str) -> Dict:
        domain = domain.lower().strip()
        if '://' in domain:
            domain = urlparse(domain).netloc
        domain = domain.split(':')[0].split('/')[0]
        if domain.startswith('www.'):
            domain = domain[4:]
        if not domain or '.' not in domain:
            return self.error_result(domain, "Invalid domain")

        from core.dns_helper import make_resolver
        resolver = make_resolver()
        resolver.timeout = 5
        resolver.lifetime = 8

        result = {
            'domain': domain,
            'ip_addresses': [],
            'ipv6_addresses': [],
            'nameservers': [],
            'mx_records': [],
            'txt_records': [],
            'spf_record': None,
            'dkim_records': [],
            'dmarc_record': None,
            'soa_record': None,
            'cname_record': None,
            'ptr_record': None,
            'http_status': None,
            'https_status': None,
            'redirect_url': None,
            'server_header': None,
            'x_powered_by': None,
            'title': None,
            'description': None,
            'technologies': [],
            'security_headers': {},
            'ssl_info': {},
            'dnssec': False,
            'response_time_ms': None,
            'timestamp': datetime.now().isoformat()
        }

        # DNS lookups in parallel
        async def resolve(qtype):
            try:
                return await resolver.resolve(domain, qtype)
            except Exception:
                return []

        # Additional DNS lookups
        a, aaaa, ns, mx, txt, soa = await asyncio.gather(
            resolve('A'), resolve('AAAA'), resolve('NS'),
            resolve('MX'), resolve('TXT'), resolve('SOA')
        )

        result['ip_addresses'] = [str(r) for r in a]
        result['ipv6_addresses'] = [str(r) for r in aaaa]
        result['nameservers'] = [str(r).rstrip('.') for r in ns]

        # MX Records
        if mx:
            result['mx_records'] = sorted(
                [{'exchange': str(r.exchange).rstrip('.'), 'priority': r.preference} for r in mx],
                key=lambda x: x['priority']
            )

        # TXT Records with SPF/DKIM/DMARC detection
        if txt:
            for rd in txt:
                for s in rd.strings:
                    t = s.decode() if isinstance(s, bytes) else str(s)
                    result['txt_records'].append(t[:500])
                    
                    # SPF detection
                    if t.startswith('v=spf1'):
                        result['spf_record'] = t[:300]
                    
                    # DKIM detection (looks like v=DKIM1 or k=rsa)
                    elif 'v=DKIM1' in t or 'k=rsa' in t:
                        result['dkim_records'].append(t[:300])
                    
                    # DMARC detection
                    elif t.startswith('v=DMARC1'):
                        result['dmarc_record'] = t[:300]

        # SOA Record
        if soa:
            for r in soa:
                result['soa_record'] = {
                    'mname': str(r.mname).rstrip('.'),
                    'rname': str(r.rname).rstrip('.'),
                    'serial': r.serial,
                    'refresh': r.refresh,
                    'retry': r.retry,
                    'expire': r.expire,
                    'minimum': r.minimum
                }

        # CNAME Record
        try:
            cn = await resolver.resolve(domain, 'CNAME')
            for r in cn:
                result['cname_record'] = str(r.target).rstrip('.')
        except Exception:
            pass

        # PTR Record (reverse DNS)
        try:
            if result['ip_addresses']:
                ptr_name = dns.reversename.from_address(result['ip_addresses'][0])
                ptr = await resolver.resolve(ptr_name, 'PTR')
                result['ptr_record'] = str(ptr[0]).rstrip('.')
        except Exception:
            pass

        # DNSSEC
        try:
            # Check if domain has DNSSEC by looking for RRSIG
            await resolver.resolve(domain, 'RRSIG')
            result['dnssec'] = True
        except Exception:
            result['dnssec'] = False

        # HTTP/HTTPS checks
        start_time = datetime.now()
        headers_result, title_result = await asyncio.gather(
            self._check_http(domain),
            self._get_title(domain)
        )
        end_time = datetime.now()
        result['response_time_ms'] = int((end_time - start_time).total_seconds() * 1000)

        if headers_result:
            result.update(headers_result)
        if title_result:
            result['title'] = title_result.get('title')
            result['description'] = title_result.get('description')
            result['technologies'] = title_result.get('technologies', [])

        # SSL/TLS Info for HTTPS
        if result.get('https_status') == 200 or result.get('https_status'):
            result['ssl_info'] = await self._get_ssl_info(domain)

        sources = ['dns']
        if result['http_status'] or result['https_status']:
            sources.append('http')
        if result['ssl_info']:
            sources.append('ssl')
        
        return self.create_result(domain, result, sources)

    async def _check_http(self, domain: str) -> Dict:
        """Check HTTP/HTTPS responses"""
        info = {}
        for proto in ('https', 'http'):
            try:
                async with self.session.get(
                    f'{proto}://{domain}',
                    timeout=aiohttp.ClientTimeout(total=5),
                    allow_redirects=True,
                    ssl=False
                ) as r:
                    key = f'{proto}_status'
                    info[key] = r.status
                    h = dict(r.headers)
                    
                    info['server_header'] = h.get('Server') or h.get('server')
                    info['x_powered_by'] = h.get('X-Powered-By')
                    info['redirect_url'] = str(r.url) if str(r.url) != f'{proto}://{domain}' else None
                    
                    # Security headers
                    info['security_headers'] = {
                        'hsts': 'Strict-Transport-Security' in h,
                        'csp': 'Content-Security-Policy' in h,
                        'xframe': 'X-Frame-Options' in h,
                        'xcto': 'X-Content-Type-Options' in h,
                        'rp': 'Referrer-Policy' in h,
                        'feature_policy': 'Permissions-Policy' in h or 'Feature-Policy' in h,
                        'cross_origin': 'Cross-Origin-Resource-Policy' in h,
                    }
                    break
            except asyncio.TimeoutError:
                pass
            except Exception:
                pass
        return info

    async def _get_title(self, domain: str) -> Dict:
        """Get website title and description"""
        for proto in ('https', 'http'):
            try:
                async with self.session.get(
                    f'{proto}://{domain}',
                    timeout=aiohttp.ClientTimeout(total=5),
                    ssl=False
                ) as r:
                    if r.status == 200:
                        html = await r.text(errors='ignore', limit=500000)  # 500KB limit
                        
                        # Title extraction
                        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
                        title = title_match.group(1).strip()[:200] if title_match else None
                        
                        # Description extraction
                        desc_match = re.search(
                            r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)',
                            html, re.I
                        )
                        description = desc_match.group(1).strip()[:300] if desc_match else None
                        
                        # Technology detection
                        techs = self._detect_tech(html, dict(r.headers))
                        
                        return {
                            'title': title,
                            'description': description,
                            'technologies': techs
                        }
            except asyncio.TimeoutError:
                pass
            except Exception:
                pass
        return {}

    async def _get_ssl_info(self, domain: str) -> Dict:
        """Get SSL/TLS certificate information"""
        ssl_info = {}
        try:
            # Create SSL context
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            # Connect to the domain
            reader, writer = await asyncio.open_connection(
                domain, 443, ssl=ctx, server_hostname=domain
            )
            
            # Get certificate
            sock = writer.get_extra_info('socket')
            ssl_obj = sock.getpeercert()
            
            if ssl_obj:
                # Parse certificate
                subject = dict(x[0] for x in ssl_obj['subject'])
                issuer = dict(x[0] for x in ssl_obj['issuer'])
                
                ssl_info = {
                    'issuer': issuer.get('organizationName', issuer.get('commonName', 'Unknown')),
                    'subject': subject.get('commonName', ''),
                    'valid_from': ssl_obj.get('notBefore', ''),
                    'valid_to': ssl_obj.get('notAfter', ''),
                    'serial': ssl_obj.get('serialNumber', ''),
                    'version': ssl_obj.get('version', ''),
                    'san': ssl_obj.get('subjectAltName', []),
                    'is_valid': True
                }
                
                # Check if certificate is expired
                from datetime import datetime as dt
                exp_date = dt.strptime(ssl_obj['notAfter'], '%b %d %H:%M:%S %Y %Z')
                ssl_info['days_left'] = (exp_date - dt.now()).days
                ssl_info['is_expired'] = ssl_info['days_left'] < 0
                
            writer.close()
            await writer.wait_closed()
            
        except asyncio.TimeoutError:
            ssl_info = {'error': 'Connection timeout', 'is_valid': False}
        except ssl.SSLError as e:
            ssl_info = {'error': str(e), 'is_valid': False}
        except Exception as e:
            ssl_info = {'error': str(e), 'is_valid': False}
            
        return ssl_info

    def _detect_tech(self, html: str, headers: dict) -> List[str]:
        """Detect technologies from HTML and headers"""
        techs = []
        combined = (html[:200000] + str(headers)).lower()  # Limit HTML size
        
        for tech, patterns in self.tech_patterns.items():
            for pattern in patterns:
                if pattern.lower() in combined:
                    techs.append(tech)
                    break
        
        # Remove duplicates while preserving order
        seen = set()
        unique_techs = []
        for t in techs:
            if t not in seen:
                seen.add(t)
                unique_techs.append(t)
        
        return unique_techs[:20]  # Limit to 20 technologies