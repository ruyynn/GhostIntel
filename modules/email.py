#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Email Module
Real email investigation via DNS and public sources
"""

import re
import dns.asyncresolver
import dns.exception
import hashlib
from typing import Dict, List, Optional
from datetime import datetime

from modules.base import BaseModule


class EmailModule(BaseModule):
    """Email OSINT - Real DNS and web checks"""
    
    def __init__(self, session):
        super().__init__(session)
        self.name = "email"
        self.email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    async def scan(self, email: str) -> Dict:
        """Scan email address"""
        email = email.lower().strip()
        
        if not self.email_regex.match(email):
            return self.error_result(email, "Invalid email format")
        
        parts = email.split('@')
        username = parts[0]
        domain = parts[1]
        
        result = {
            'email': email,
            'username': username,
            'domain': domain,
            'valid_format': True,
            'mx_records': [],
            'spf': None,
            'dmarc': None,
            'has_website': False,
            'gravatar': None,
            'disposable': await self._check_disposable(domain),
            'free_provider': self._is_free_provider(domain)
        }
        
        resolver = dns.asyncresolver.Resolver()
        
        # Get MX records
        try:
            answers = await resolver.resolve(domain, 'MX')
            for rdata in answers:
                result['mx_records'].append({
                    'exchange': str(rdata.exchange).rstrip('.'),
                    'priority': rdata.preference
                })
            # Sort by priority
            result['mx_records'].sort(key=lambda x: x['priority'])
        except dns.exception.DNSException:
            pass
        
        # Get SPF record (TXT with v=spf1)
        try:
            answers = await resolver.resolve(domain, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    txt = txt_string.decode() if isinstance(txt_string, bytes) else str(txt_string)
                    if txt.startswith('v=spf1'):
                        result['spf'] = txt
                        break
        except:
            pass
        
        # Get DMARC record
        try:
            dmarc_domain = f"_dmarc.{domain}"
            answers = await resolver.resolve(dmarc_domain, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    txt = txt_string.decode() if isinstance(txt_string, bytes) else str(txt_string)
                    if txt.startswith('v=DMARC1'):
                        result['dmarc'] = txt
                        break
        except:
            pass
        
        # Check if domain has website
        try:
            async with self.session.get(f"http://{domain}", timeout=3, allow_redirects=True) as resp:
                result['has_website'] = resp.status == 200
                if resp.status == 200:
                    result['website_url'] = f"http://{domain}"
        except:
            try:
                async with self.session.get(f"https://{domain}", timeout=3, allow_redirects=True) as resp:
                    result['has_website'] = resp.status == 200
                    if resp.status == 200:
                        result['website_url'] = f"https://{domain}"
            except:
                pass
        
        # Check Gravatar
        email_hash = hashlib.md5(email.encode()).hexdigest()
        gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
        try:
            async with self.session.get(gravatar_url, timeout=2) as resp:
                if resp.status == 200 and resp.headers.get('Content-Type', '').startswith('image/'):
                    result['gravatar'] = gravatar_url
                    
                    # Try to get profile
                    profile_url = f"https://www.gravatar.com/{email_hash}"
                async with self.session.get(profile_url, timeout=2) as profile_resp:
                        if profile_resp.status == 200:
                            result['gravatar_profile'] = profile_url
        except:
            pass
        
        # Generate possible usernames
        result['possible_usernames'] = self._generate_usernames(username)
        
        sources = ['dns']
        if result['gravatar']:
            sources.append('gravatar')
        if result['mx_records']:
            sources.append('mx_lookup')
        
        return self.create_result(email, result, sources)
    
    async def _check_disposable(self, domain: str) -> bool:
        """Check if domain is disposable email provider"""
        disposable_domains = [
            'tempmail.com', 'throwaway.com', 'mailinator.com', 'guerrillamail.com',
            'sharklasers.com', 'yopmail.com', '10minutemail.com', 'temp-mail.org',
            'getnada.com', 'trashmail.com', 'wegwerfmail.de', 'spambox.us',
            'maildrop.cc', 'tempinbox.com', 'dispostable.com', 'fakeinbox.com'
        ]
        return domain.lower() in disposable_domains
    
    def _is_free_provider(self, domain: str) -> bool:
        """Check if domain is free email provider"""
        free_providers = [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com',
            'protonmail.com', 'proton.me', 'pm.me', 'mail.com', 'yandex.com',
            'icloud.com', 'me.com', 'live.com', 'msn.com', 'gmx.com', 'gmx.net'
        ]
        return domain.lower() in free_providers
    
    def _generate_usernames(self, username: str) -> List[str]:
        """Generate possible username variations"""
        usernames = [username]
        
        # Remove dots
        if '.' in username:
            usernames.append(username.replace('.', ''))
            usernames.append(username.replace('.', '_'))
        
        # Remove underscores
        if '_' in username:
            usernames.append(username.replace('_', ''))
        
        # Add common prefixes
        prefixes = ['real', 'official', 'the', 'mr', 'ms', 'dr']
        for prefix in prefixes:
            usernames.append(f"{prefix}{username}")
            usernames.append(f"{prefix}_{username}")
        
        return list(set(usernames))[:10]