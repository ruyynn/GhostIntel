#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Social Media Database
100+ platform URLs for username checking
"""

from typing import List, Dict, Any


class SocialMediaDB:
    """Database of social media platforms"""
    
    def __init__(self):
        self.platforms = self._load_platforms()
    
    def _load_platforms(self) -> List[Dict[str, Any]]:
        """Load all platforms"""
        return [
            # Social Networks
            {"name": "Facebook", "url": "https://facebook.com/{}", "category": "social"},
            {"name": "Twitter", "url": "https://twitter.com/{}", "category": "social"},
            {"name": "Instagram", "url": "https://instagram.com/{}", "category": "social"},
            {"name": "LinkedIn", "url": "https://linkedin.com/in/{}", "category": "professional"},
            {"name": "TikTok", "url": "https://tiktok.com/@{}", "category": "social"},
            {"name": "Snapchat", "url": "https://snapchat.com/add/{}", "category": "social"},
            {"name": "Pinterest", "url": "https://pinterest.com/{}", "category": "social"},
            {"name": "Reddit", "url": "https://reddit.com/user/{}", "category": "forum"},
            {"name": "Tumblr", "url": "https://{}.tumblr.com", "category": "blog"},
            {"name": "Mastodon.social", "url": "https://mastodon.social/@{}", "category": "social"},
            {"name": "Mastodon.online", "url": "https://mastodon.online/@{}", "category": "social"},
            {"name": "Truth Social", "url": "https://truthsocial.com/@{}", "category": "social"},
            {"name": "Parler", "url": "https://parler.com/profile/{}", "category": "social"},
            {"name": "Gab", "url": "https://gab.com/{}", "category": "social"},
            {"name": "Gettr", "url": "https://gettr.com/user/{}", "category": "social"},
            
            # Developer Platforms
            {"name": "GitHub", "url": "https://github.com/{}", "category": "dev"},
            {"name": "GitLab", "url": "https://gitlab.com/{}", "category": "dev"},
            {"name": "Bitbucket", "url": "https://bitbucket.org/{}/", "category": "dev"},
            {"name": "SourceForge", "url": "https://sourceforge.net/u/{}", "category": "dev"},
            {"name": "Codeberg", "url": "https://codeberg.org/{}", "category": "dev"},
            {"name": "Gitee", "url": "https://gitee.com/{}", "category": "dev"},
            {"name": "Giters", "url": "https://giters.com/{}", "category": "dev"},
            {"name": "HackerOne", "url": "https://hackerone.com/{}", "category": "security"},
            {"name": "Bugcrowd", "url": "https://bugcrowd.com/{}", "category": "security"},
            {"name": "Intigriti", "url": "https://intigriti.com/researcher/{}", "category": "security"},
            {"name": "Keybase", "url": "https://keybase.io/{}", "category": "security"},
            
            # Coding Platforms
            {"name": "Replit", "url": "https://replit.com/@{}", "category": "dev"},
            {"name": "Codepen", "url": "https://codepen.io/{}", "category": "dev"},
            {"name": "CodeSandbox", "url": "https://codesandbox.io/u/{}", "category": "dev"},
            {"name": "Glitch", "url": "https://glitch.com/@{}", "category": "dev"},
            {"name": "StackBlitz", "url": "https://stackblitz.com/@{}", "category": "dev"},
            {"name": "JSFiddle", "url": "https://jsfiddle.net/user/{}/", "category": "dev"},
            {"name": "LeetCode", "url": "https://leetcode.com/{}", "category": "coding"},
            {"name": "HackerRank", "url": "https://hackerrank.com/{}", "category": "coding"},
            {"name": "CodeChef", "url": "https://codechef.com/users/{}", "category": "coding"},
            {"name": "TopCoder", "url": "https://topcoder.com/members/{}", "category": "coding"},
            {"name": "Kaggle", "url": "https://kaggle.com/{}", "category": "data"},
            
            # Messaging
            {"name": "Telegram", "url": "https://t.me/{}", "category": "messaging"},
            {"name": "WhatsApp", "url": "https://wa.me/{}", "category": "messaging"},
            {"name": "Discord", "url": "https://discord.com/users/{}", "category": "chat"},
            {"name": "Slack", "url": "https://{}.slack.com", "category": "chat"},
            {"name": "Matrix", "url": "https://matrix.to/#/@{}:matrix.org", "category": "chat"},
            
            # Forums
            {"name": "Quora", "url": "https://quora.com/profile/{}", "category": "forum"},
            {"name": "Medium", "url": "https://medium.com/@{}", "category": "blog"},
            {"name": "Dev.to", "url": "https://dev.to/{}", "category": "dev"},
            {"name": "HackerNews", "url": "https://news.ycombinator.com/user?id={}", "category": "forum"},
            {"name": "ProductHunt", "url": "https://producthunt.com/@{}", "category": "tech"},
            {"name": "StackOverflow", "url": "https://stackoverflow.com/users/{}", "category": "dev"},
            {"name": "AskUbuntu", "url": "https://askubuntu.com/users/{}", "category": "forum"},
            {"name": "ServerFault", "url": "https://serverfault.com/users/{}", "category": "forum"},
            
            # Video/Streaming
            {"name": "YouTube", "url": "https://youtube.com/@{}", "category": "video"},
            {"name": "Twitch", "url": "https://twitch.tv/{}", "category": "streaming"},
            {"name": "Vimeo", "url": "https://vimeo.com/{}", "category": "video"},
            {"name": "Dailymotion", "url": "https://dailymotion.com/{}", "category": "video"},
            {"name": "Kick", "url": "https://kick.com/{}", "category": "streaming"},
            {"name": "Rumble", "url": "https://rumble.com/user/{}", "category": "video"},
            {"name": "Odysee", "url": "https://odysee.com/@{}", "category": "video"},
            
            # Music
            {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "category": "music"},
            {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "category": "music"},
            {"name": "Bandcamp", "url": "https://bandcamp.com/{}", "category": "music"},
            {"name": "Mixcloud", "url": "https://mixcloud.com/{}", "category": "music"},
            {"name": "Last.fm", "url": "https://last.fm/user/{}", "category": "music"},
            {"name": "Genius", "url": "https://genius.com/{}", "category": "music"},
            
            # Gaming
            {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "category": "gaming"},
            {"name": "Steam Group", "url": "https://steamcommunity.com/groups/{}", "category": "gaming"},
            {"name": "Epic Games", "url": "https://epicgames.com/id/{}", "category": "gaming"},
            {"name": "Xbox", "url": "https://xbox.com/player/{}", "category": "gaming"},
            {"name": "PlayStation", "url": "https://psnprofiles.com/{}", "category": "gaming"},
            {"name": "Nintendo", "url": "https://nintendo.com/{}", "category": "gaming"},
            {"name": "Minecraft", "url": "https://namemc.com/profile/{}", "category": "gaming"},
            {"name": "Roblox", "url": "https://roblox.com/user/{}", "category": "gaming"},
            {"name": "Chess.com", "url": "https://chess.com/member/{}", "category": "gaming"},
            {"name": "Lichess", "url": "https://lichess.org/@/{}", "category": "gaming"},
            
            # Indonesian Platforms
            {"name": "Kaskus", "url": "https://kaskus.co.id/profile/{}", "category": "forum"},
            {"name": "Kompasiana", "url": "https://kompasiana.com/{}", "category": "blog"},
            {"name": "Detik Forum", "url": "https://forum.detik.com/member.php?username={}", "category": "forum"},
            {"name": "Indowebster", "url": "https://indowebster.com/user/{}", "category": "forum"},
            {"name": "Lintas.me", "url": "https://lintas.me/user/{}", "category": "social"},
            
            # Professional
            {"name": "Upwork", "url": "https://upwork.com/fl/{}", "category": "freelance"},
            {"name": "Fiverr", "url": "https://fiverr.com/{}", "category": "freelance"},
            {"name": "Freelancer", "url": "https://freelancer.com/u/{}", "category": "freelance"},
            {"name": "Toptal", "url": "https://toptal.com/{}", "category": "freelance"},
            {"name": "AngelList", "url": "https://angel.co/u/{}", "category": "professional"},
            {"name": "Crunchbase", "url": "https://crunchbase.com/person/{}", "category": "business"},
            {"name": "ResearchGate", "url": "https://researchgate.net/profile/{}", "category": "academic"},
            {"name": "Academia.edu", "url": "https://academia.edu/{}", "category": "academic"},
            
            # Other
            {"name": "Wikipedia", "url": "https://wikipedia.org/wiki/User:{}", "category": "wiki"},
            {"name": "Fandom", "url": "https://fandom.com/wiki/User:{}", "category": "wiki"},
            {"name": "Archive.org", "url": "https://archive.org/details/@{}", "category": "archive"},
            {"name": "Patreon", "url": "https://patreon.com/{}", "category": "funding"},
            {"name": "BuyMeACoffee", "url": "https://buymeacoffee.com/{}", "category": "funding"},
            {"name": "Ko-fi", "url": "https://ko-fi.com/{}", "category": "funding"},
        ]
    
    def get_all_platforms(self) -> List[Dict]:
        """Get all platforms"""
        return self.platforms
    
    def get_platforms_by_category(self, category: str) -> List[Dict]:
        """Get platforms by category"""
        return [p for p in self.platforms if p['category'] == category]
    
    def get_platform_count(self) -> int:
        """Get total number of platforms"""
        return len(self.platforms)