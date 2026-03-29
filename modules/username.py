#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Username Module (Enhanced)"""

import asyncio
import random
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
from modules.base import BaseModule
from sources.social_media import SocialMediaDB


class UsernameModule(BaseModule):  # <-- PASTIKAN NAMA CLASS INI
    def __init__(self, session: aiohttp.ClientSession):
        super().__init__(session)
        self.name = "username"
        self.social_db = SocialMediaDB()
        
        # Rotating User-Agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        ]
        
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def _get_headers(self) -> Dict:
        """Get headers with random User-Agent"""
        headers = self.base_headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        return headers

    async def scan(self, username: str) -> Dict:
        username = username.strip().lstrip('@')
        if not username:
            return self.error_result(username, "Empty username")

        platforms = self.social_db.get_all_platforms()
        found = []
        semaphore = asyncio.Semaphore(10)

        async def check_platform(platform: Dict) -> Optional[Dict]:
            async with semaphore:
                url = platform['url'].format(username)
                headers = self._get_headers()
                
                try:
                    async with self.session.get(
                        url, 
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=8),
                        allow_redirects=True,
                        ssl=False
                    ) as resp:
                        
                        if resp.status == 429:
                            await asyncio.sleep(2)
                            return None
                        
                        if resp.status == 200:
                            try:
                                html = await resp.text(encoding='utf-8', errors='ignore', limit=200000)
                                soup = BeautifulSoup(html, 'html.parser')
                                title = (soup.title.string or '').lower() if soup.title else ''
                                
                                # Filter not found
                                not_found = ['404', 'page not found', 'user not found', 
                                            "doesn't exist", 'profile not found']
                                
                                body_text = html.lower()[:5000]
                                if any(b in title for b in not_found) or \
                                   any(b in body_text for b in ['user not found', 'page not found']):
                                    return None
                                
                                # Cari nama profil
                                name = None
                                name_selectors = [
                                    'h1', 'h2', '.profile-name', '.displayname',
                                    '[class*="name"]', '[class*="username"]',
                                    '.full-name', '.profile-header-name',
                                    'meta[property="og:title"]', 'title'
                                ]
                                for sel in name_selectors:
                                    try:
                                        if sel.startswith('meta'):
                                            el = soup.select_one(sel)
                                            if el and el.get('content'):
                                                name = el.get('content')[:80]
                                                break
                                        else:
                                            el = soup.select_one(sel)
                                            if el and el.get_text(strip=True):
                                                name = el.get_text(strip=True)[:80]
                                                break
                                    except:
                                        continue
                                
                                return {
                                    'platform': platform['name'],
                                    'url': str(resp.url),
                                    'category': platform.get('category', 'social'),
                                    'profile_name': name,
                                    'status': 'found'
                                }
                            except Exception:
                                return {
                                    'platform': platform['name'],
                                    'url': str(resp.url),
                                    'category': platform.get('category', 'social'),
                                    'profile_name': None,
                                    'status': 'found'
                                }
                        
                        elif resp.status in (301, 302, 307, 308):
                            loc = resp.headers.get('Location', '')
                            if username.lower() in loc.lower() or 'profile' in loc.lower():
                                return {
                                    'platform': platform['name'],
                                    'url': loc,
                                    'category': platform.get('category', 'social'),
                                    'profile_name': None,
                                    'status': 'redirect'
                                }
                            
                except (asyncio.TimeoutError, aiohttp.ClientError):
                    pass
                except Exception:
                    pass
                return None

        # Process in batches
        batch_size = 10
        for i in range(0, len(platforms), batch_size):
            batch = platforms[i:i+batch_size]
            tasks = [check_platform(p) for p in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for r in results:
                if isinstance(r, dict) and r:
                    found.append(r)
            
            if i + batch_size < len(platforms):
                await asyncio.sleep(random.uniform(0.3, 0.8))

        # By category
        by_cat = {}
        for f in found:
            cat = f.get('category', 'other')
            by_cat.setdefault(cat, []).append(f)

        possible_emails = [f"{username}@{d}" for d in
                           ['gmail.com', 'yahoo.com', 'outlook.com', 
                            'hotmail.com', 'protonmail.com', 'mail.com']]

        data = {
            'username': username,
            'total_checked': len(platforms),
            'total_found': len(found),
            'found': found,
            'by_category': by_cat,
            'profiles': [f['url'] for f in found],
            'possible_emails': possible_emails,
            'variations': self._generate_variations(username)[:10],
            'categories': list(by_cat.keys()),
            'timestamp': datetime.now().isoformat()
        }
        return self.create_result(username, data, [f['platform'] for f in found])

    def _generate_variations(self, u: str) -> List[str]:
        v = [u.lower(), u.upper(), u.capitalize()]
        for i in range(5):
            v += [f"{u}{i}", f"{u}_{i}", f"{u}.{i}"]
        for s in ['real', 'official', 'admin', '_id', '_official', 'official_']:
            v += [f"{u}{s}", f"{s}{u}"]
        return list(dict.fromkeys(v))