#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Email Module (with Breach Detection)"""

import re
import hashlib
import dns.asyncresolver
import dns.exception
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp
from modules.base import BaseModule
from sources.breach_db import BreachDB  # Import breach database


# Disposable email domains
DISPOSABLE = {
    'tempmail.com', 'throwaway.com', 'mailinator.com', 'guerrillamail.com',
    'sharklasers.com', 'yopmail.com', '10minutemail.com', 'temp-mail.org',
    'getnada.com', 'trashmail.com', 'maildrop.cc', 'fakeinbox.com',
    'dispostable.com', 'spamgourmet.com', 'mintemail.com', 'mytrashmail.com',
    'spambox.us', 'tempinbox.com', 'wegwerfmail.de', 'mailnull.com'
}

# Free email providers
FREE_PROVIDERS = {
    'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com',
    'protonmail.com', 'proton.me', 'pm.me', 'mail.com', 'yandex.com',
    'icloud.com', 'me.com', 'live.com', 'msn.com', 'gmx.com', 'gmx.net',
    'zoho.com', 'fastmail.com', 'tutanota.com', 'hey.com'
}


class EmailModule(BaseModule):
    def __init__(self, session):
        super().__init__(session)
        self.name = "email"
        self.email_re = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')
        self.breach_db = BreachDB()  # Initialize breach database

    async def scan(self, email: str) -> Dict:
        email = email.lower().strip()
        if not self.email_re.match(email):
            return self.error_result(email, "Invalid email format")

        username, domain = email.split('@', 1)
        from core.dns_helper import make_resolver
        resolver = make_resolver()
        resolver.timeout = 5
        resolver.lifetime = 8

        # Check for known breaches
        breach_info = self._check_breaches(domain, username)

        result = {
            'email': email,
            'username': username,
            'domain': domain,
            'valid_format': True,
            'mx_records': [],
            'spf': None,
            'dmarc': None,
            'dkim_hint': None,
            'has_website': False,
            'website_url': None,
            'gravatar': None,
            'gravatar_profile': None,
            'gravatar_hash': hashlib.md5(email.encode()).hexdigest(),
            'disposable': domain in DISPOSABLE,
            'free_provider': domain in FREE_PROVIDERS,
            'possible_usernames': self._gen_usernames(username),
            'breach_info': breach_info,  # Added breach info
            'breach_risk': self._calculate_breach_risk(breach_info),  # Risk score
            'timestamp': datetime.now().isoformat()
        }

        # MX records
        try:
            ans = await resolver.resolve(domain, 'MX')
            result['mx_records'] = sorted(
                [{'exchange': str(r.exchange).rstrip('.'), 'priority': r.preference} for r in ans],
                key=lambda x: x['priority']
            )
        except Exception:
            pass

        # TXT (SPF)
        try:
            ans = await resolver.resolve(domain, 'TXT')
            for rd in ans:
                for s in rd.strings:
                    txt = s.decode() if isinstance(s, bytes) else str(s)
                    if txt.startswith('v=spf1'):
                        result['spf'] = txt[:200]
        except Exception:
            pass

        # DMARC
        try:
            ans = await resolver.resolve(f'_dmarc.{domain}', 'TXT')
            for rd in ans:
                for s in rd.strings:
                    txt = s.decode() if isinstance(s, bytes) else str(s)
                    if txt.startswith('v=DMARC1'):
                        result['dmarc'] = txt[:200]
        except Exception:
            pass

        # DKIM common selector
        for sel in ['google', 'k1', 'mail', 'default', 'dkim', 'selector1']:
            try:
                await resolver.resolve(f'{sel}._domainkey.{domain}', 'TXT')
                result['dkim_hint'] = f'{sel}._domainkey.{domain} exists'
                break
            except Exception:
                pass

        # Website check
        for proto in ('https', 'http'):
            try:
                async with self.session.get(
                    f'{proto}://{domain}', timeout=aiohttp.ClientTimeout(total=4),
                    allow_redirects=True, ssl=False
                ) as r:
                    if r.status < 400:
                        result['has_website'] = True
                        result['website_url'] = str(r.url)
                        break
            except Exception:
                pass

        # Gravatar
        gh = result['gravatar_hash']
        try:
            async with self.session.get(
                f'https://www.gravatar.com/avatar/{gh}?d=404',
                timeout=aiohttp.ClientTimeout(total=4)
            ) as r:
                if r.status == 200:
                    result['gravatar'] = f'https://www.gravatar.com/avatar/{gh}'
                    result['gravatar_profile'] = f'https://www.gravatar.com/{gh}'
        except Exception:
            pass

        sources = ['dns']
        if result['gravatar']:   sources.append('gravatar')
        if result['mx_records']: sources.append('mx_lookup')
        if result['spf']:        sources.append('spf')
        if result['breach_info']: sources.append('breach_db')
        
        return self.create_result(email, result, sources)

    def _gen_usernames(self, u: str) -> List[str]:
        names = [u]
        if '.' in u:
            names += [u.replace('.', ''), u.replace('.', '_')]
        if '_' in u:
            names.append(u.replace('_', ''))
        for p in ['real', 'the', 'official', 'mr', 'ms']:
            names += [f'{p}{u}', f'{p}_{u}']
        return list(dict.fromkeys(names))[:12]

    def _check_breaches(self, domain: str, username: str = None) -> Dict:
        """
        Check if domain has known breaches and if username might be affected
        Returns detailed breach information
        """
        # Search breaches by domain
        domain_breaches = self.breach_db.search_by_domain(domain)
        
        # Also search by domain alias (e.g., gmail.com vs google.com)
        domain_aliases = {
            'gmail.com': 'Google',
            'google.com': 'Google',
            'yahoo.com': 'Yahoo',
            'ymail.com': 'Yahoo',
            'hotmail.com': 'Microsoft',
            'outlook.com': 'Microsoft',
            'live.com': 'Microsoft',
            'msn.com': 'Microsoft',
            'facebook.com': 'Facebook',
            'twitter.com': 'Twitter',
            'linkedin.com': 'LinkedIn',
            'tumblr.com': 'Tumblr',
            'dropbox.com': 'Dropbox',
            'canva.com': 'Canva',
            'tokopedia.com': 'Tokopedia',
            'jd.id': 'JD.ID',
            'bhinneka.com': 'Bhinneka',
        }
        
        alias = domain_aliases.get(domain)
        alias_breaches = []
        if alias:
            alias_breaches = self.breach_db.search_by_domain(alias)
        
        all_breaches = domain_breaches + alias_breaches
        # Remove duplicates by name
        unique_breaches = {b['name']: b for b in all_breaches}.values()
        
        if not unique_breaches:
            return {
                'has_breaches': False,
                'message': 'No known data breaches for this domain',
                'breaches': []
            }
        
        # Calculate severity based on breach size and recency
        breach_list = []
        total_records = 0
        highest_risk = 'low'
        
        for breach in unique_breaches:
            records = breach.get('records', 0)
            year = breach.get('year', 2000)
            total_records += records
            
            # Determine risk level
            if records > 100_000_000:
                risk = 'critical'
            elif records > 10_000_000:
                risk = 'high'
            elif records > 1_000_000:
                risk = 'medium'
            else:
                risk = 'low'
            
            if risk == 'critical':
                highest_risk = 'critical'
            elif risk == 'high' and highest_risk != 'critical':
                highest_risk = 'high'
            elif risk == 'medium' and highest_risk not in ['critical', 'high']:
                highest_risk = 'medium'
            
            breach_list.append({
                'name': breach.get('name'),
                'year': year,
                'records': records,
                'risk': risk,
                'description': breach.get('description', ''),
                'data_types': breach.get('data_types', []),
                'country': breach.get('country')
            })
        
        # Check if username might be affected
        username_affected = False
        affected_reason = None
        
        for breach in breach_list:
            if 'usernames' in breach.get('data_types', []):
                username_affected = True
                affected_reason = f"Usernames were exposed in {breach['name']} breach"
                break
            if 'emails' in breach.get('data_types', []):
                username_affected = True
                affected_reason = f"Email addresses were exposed in {breach['name']} breach"
                break
        
        # Sort breaches by year (newest first)
        breach_list.sort(key=lambda x: x['year'], reverse=True)
        
        return {
            'has_breaches': True,
            'message': f'⚠️ This domain has been involved in {len(breach_list)} known data breach(es)',
            'breaches': breach_list[:5],  # Show top 5 most recent
            'total_breaches': len(breach_list),
            'total_records_exposed': total_records,
            'risk_level': highest_risk,
            'username_may_be_affected': username_affected,
            'affected_reason': affected_reason,
            'recommendation': self._get_recommendation(highest_risk, username_affected)
        }
    
    def _calculate_breach_risk(self, breach_info: Dict) -> int:
        """
        Calculate risk score (0-100) based on breach info
        """
        if not breach_info.get('has_breaches'):
            return 0
        
        risk_score = 0
        risk_level = breach_info.get('risk_level', 'low')
        
        if risk_level == 'critical':
            risk_score = 85
        elif risk_level == 'high':
            risk_score = 70
        elif risk_level == 'medium':
            risk_score = 50
        else:
            risk_score = 30
        
        # Add extra points if username may be affected
        if breach_info.get('username_may_be_affected'):
            risk_score += 15
        
        # Cap at 100
        return min(risk_score, 100)
    
    def _get_recommendation(self, risk_level: str, username_affected: bool) -> str:
        """
        Generate security recommendation based on breach info
        """
        if risk_level == 'critical':
            return "IMMEDIATE ACTION REQUIRED: Change all passwords, enable 2FA, and monitor accounts for suspicious activity."
        elif risk_level == 'high':
            return "URGENT: Change your password for this service and any other accounts using the same password. Enable 2FA."
        elif risk_level == 'medium':
            if username_affected:
                return "Consider changing your username/email on this service and use a password manager with unique passwords."
            return "Recommend changing your password if you haven't done so recently. Enable 2FA if available."
        else:
            if username_affected:
                return "Your username may have been exposed. Consider using a different email/username for sensitive accounts."
            return "No immediate action required, but always use unique passwords and enable 2FA where possible."