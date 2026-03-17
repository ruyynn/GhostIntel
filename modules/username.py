#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Username Module
username checking across 50+ platforms via HTTP probing
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

from modules.base import BaseModule
from sources.social_media import SocialMediaDB


class UsernameModule(BaseModule):
    """Username OSINT - platform checking"""
    
    def __init__(self, session: aiohttp.ClientSession):
        super().__init__(session)
        self.name = "username"
        self.social_db = SocialMediaDB()
        
        # Headers to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    async def scan(self, username: str) -> Dict:
        """
        Scan username across all platforms
        """
        username = username.strip().lstrip('@')
        
        if not username:
            return self.error_result(username, "Empty username")
        
        # Get all platforms
        platforms = self.social_db.get_all_platforms()
        
        found = []
        semaphore = asyncio.Semaphore(15)  # Limit concurrency
        
        async def check_platform(platform: Dict) -> Optional[Dict]:
            """Check single platform"""
            async with semaphore:
                url = platform['url'].format(username)
                
                try:
                    async with self.session.get(
                        url,
                        headers=self.headers,
                        timeout=5,
                        allow_redirects=True,
                        ssl=False
                    ) as resp:
                        
                        if resp.status == 200:
                            # Get page title to verify it's not a 404 page
                            try:
                                html = await resp.text()
                                soup = BeautifulSoup(html, 'html.parser')
                                title = soup.title.string.lower() if soup.title else ""
                                
                                # Check for "not found" patterns
                                not_found_patterns = [
                                    'not found', 'page not found', '404',
                                    'user not found', 'doesn\'t exist',
                                    'no such user', 'profile not found'
                                ]
                                
                                if any(pattern in title for pattern in not_found_patterns):
                                    return None
                                
                                # Try to get profile name
                                name = None
                                name_selectors = ['h1', '.profile-name', '.full-name', '[class*="name"]']
                                for selector in name_selectors:
                                    elem = soup.select_one(selector)
                                    if elem:
                                        name = elem.get_text().strip()[:100]
                                        break
                                
                                return {
                                    'platform': platform['name'],
                                    'url': str(resp.url),
                                    'category': platform.get('category', 'social'),
                                    'status': 'active',
                                    'profile_name': name
                                }
                            except:
                                # If can't parse, assume it's valid
                                return {
                                    'platform': platform['name'],
                                    'url': str(resp.url),
                                    'category': platform.get('category', 'social'),
                                    'status': 'active'
                                }
                
                except asyncio.TimeoutError:
                    pass
                except Exception:
                    pass
                
                return None
        
        # Check all platforms
        tasks = [check_platform(p) for p in platforms]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result:
                found.append(result)
        
        # Generate possible emails
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com']
        possible_emails = [f"{username}@{domain}" for domain in domains]
        
        # Generate possible usernames variations
        variations = self._generate_variations(username)
        
        result = {
            'username': username,
            'total_checked': len(platforms),
            'total_found': len(found),
            'found': found,
            'profiles': [f['url'] for f in found],
            'possible_emails': possible_emails[:5],
            'variations': variations[:10],
            'categories': list(set([f['category'] for f in found])),
            'timestamp': datetime.now().isoformat()
        }
        
        sources = [f['platform'] for f in found]
        return self.create_result(username, result, sources)
    
    def _generate_variations(self, username: str) -> List[str]:
        """Generate username variations"""
        variations = []
        
        # Common variations
        variations.append(username.lower())
        variations.append(username.upper())
        variations.append(username.capitalize())
        
        # Add numbers
        for i in range(10):
            variations.append(f"{username}{i}")
            variations.append(f"{username}_{i}")
        
        # Add common suffixes
        suffixes = ['real', 'official', 'admin', 'support', 'help', 'team']
        for suffix in suffixes:
            variations.append(f"{username}{suffix}")
            variations.append(f"{username}_{suffix}")
        
        # Remove duplicates
        return list(set(variations))[:20]