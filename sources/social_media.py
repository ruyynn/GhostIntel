#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.5 - Social Media Database (Enhanced)
120+ platform URLs for username checking
Includes all platforms from v2.0 + additional improvements
"""

from typing import List, Dict, Any


class SocialMediaDB:
    """Database of social media platforms - Enhanced v2.5"""
    
    def __init__(self):
        self.platforms = self._load_platforms()
    
    def _load_platforms(self) -> List[Dict[str, Any]]:
        """Load all platforms - 120+ total"""
        return [
            # ==================== SOCIAL NETWORKS ====================
            {"name": "Facebook", "url": "https://facebook.com/{}", "category": "social"},
            {"name": "Twitter", "url": "https://twitter.com/{}", "category": "social"},
            {"name": "Instagram", "url": "https://instagram.com/{}", "category": "social"},
            {"name": "LinkedIn", "url": "https://linkedin.com/in/{}", "category": "professional"},
            {"name": "TikTok", "url": "https://tiktok.com/@{}", "category": "social"},
            {"name": "Snapchat", "url": "https://snapchat.com/add/{}", "category": "social"},
            {"name": "Pinterest", "url": "https://pinterest.com/{}", "category": "social"},
            {"name": "Reddit", "url": "https://reddit.com/user/{}", "category": "forum"},
            {"name": "Tumblr", "url": "https://{}.tumblr.com", "category": "blog"},
            {"name": "Threads", "url": "https://threads.net/@{}", "category": "social"},
            {"name": "Bluesky", "url": "https://bsky.app/profile/{}", "category": "social"},
            {"name": "Mastodon.social", "url": "https://mastodon.social/@{}", "category": "social"},
            {"name": "Mastodon.online", "url": "https://mastodon.online/@{}", "category": "social"},
            {"name": "Truth Social", "url": "https://truthsocial.com/@{}", "category": "social"},
            {"name": "Parler", "url": "https://parler.com/profile/{}", "category": "social"},
            {"name": "Gab", "url": "https://gab.com/{}", "category": "social"},
            {"name": "Gettr", "url": "https://gettr.com/user/{}", "category": "social"},
            {"name": "Telegram", "url": "https://t.me/{}", "category": "messaging"},
            {"name": "WhatsApp", "url": "https://wa.me/{}", "category": "messaging"},
            {"name": "Discord", "url": "https://discord.com/users/{}", "category": "chat"},
            {"name": "Signal", "url": "https://signal.me/#p/{}", "category": "messaging"},
            {"name": "VK", "url": "https://vk.com/{}", "category": "social"},
            {"name": "Odnoklassniki", "url": "https://ok.ru/{}", "category": "social"},
            {"name": "Weibo", "url": "https://weibo.com/{}", "category": "social"},
            {"name": "WeChat", "url": "https://wechat.com/{}", "category": "messaging"},
            
            # ==================== INDONESIAN PLATFORMS ====================
            {"name": "Kaskus", "url": "https://kaskus.co.id/profile/{}", "category": "forum"},
            {"name": "Kompasiana", "url": "https://kompasiana.com/{}", "category": "blog"},
            {"name": "Detik Forum", "url": "https://forum.detik.com/member.php?username={}", "category": "forum"},
            {"name": "Indowebster", "url": "https://indowebster.com/user/{}", "category": "forum"},
            {"name": "Lintas.me", "url": "https://lintas.me/user/{}", "category": "social"},
            {"name": "IDN Times", "url": "https://idntimes.com/{}", "category": "blog"},
            {"name": "Liputan6", "url": "https://liputan6.com/{}", "category": "news"},
            {"name": "Tribun News", "url": "https://tribunnews.com/{}", "category": "news"},
            {"name": "Suara.com", "url": "https://suara.com/{}", "category": "news"},
            {"name": "Merdeka", "url": "https://merdeka.com/{}", "category": "news"},
            
            # ==================== DEVELOPER PLATFORMS ====================
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
            {"name": "Bugzilla", "url": "https://bugzilla.mozilla.org/user_profile?user_id={}", "category": "security"},
            
            # ==================== CODING PLATFORMS ====================
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
            {"name": "Codingame", "url": "https://codingame.com/profile/{}", "category": "coding"},
            {"name": "Exercism", "url": "https://exercism.org/profiles/{}", "category": "coding"},
            
            # ==================== FORUMS & COMMUNITIES ====================
            {"name": "Quora", "url": "https://quora.com/profile/{}", "category": "forum"},
            {"name": "Medium", "url": "https://medium.com/@{}", "category": "blog"},
            {"name": "Dev.to", "url": "https://dev.to/{}", "category": "dev"},
            {"name": "HackerNews", "url": "https://news.ycombinator.com/user?id={}", "category": "forum"},
            {"name": "ProductHunt", "url": "https://producthunt.com/@{}", "category": "tech"},
            {"name": "StackOverflow", "url": "https://stackoverflow.com/users/{}", "category": "dev"},
            {"name": "AskUbuntu", "url": "https://askubuntu.com/users/{}", "category": "forum"},
            {"name": "ServerFault", "url": "https://serverfault.com/users/{}", "category": "forum"},
            {"name": "SuperUser", "url": "https://superuser.com/users/{}", "category": "forum"},
            {"name": "4chan", "url": "https://4chan.org/{}", "category": "forum"},
            {"name": "9GAG", "url": "https://9gag.com/u/{}", "category": "forum"},
            {"name": "Imgur", "url": "https://imgur.com/user/{}", "category": "social"},
            
            # ==================== VIDEO & STREAMING ====================
            {"name": "YouTube", "url": "https://youtube.com/@{}", "category": "video"},
            {"name": "Twitch", "url": "https://twitch.tv/{}", "category": "streaming"},
            {"name": "Vimeo", "url": "https://vimeo.com/{}", "category": "video"},
            {"name": "Dailymotion", "url": "https://dailymotion.com/{}", "category": "video"},
            {"name": "Kick", "url": "https://kick.com/{}", "category": "streaming"},
            {"name": "Rumble", "url": "https://rumble.com/user/{}", "category": "video"},
            {"name": "Odysee", "url": "https://odysee.com/@{}", "category": "video"},
            {"name": "Trovo", "url": "https://trovo.live/{}", "category": "streaming"},
            {"name": "Facebook Gaming", "url": "https://facebook.com/gaming/{}", "category": "streaming"},
            
            # ==================== MUSIC ====================
            {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "category": "music"},
            {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "category": "music"},
            {"name": "Bandcamp", "url": "https://bandcamp.com/{}", "category": "music"},
            {"name": "Mixcloud", "url": "https://mixcloud.com/{}", "category": "music"},
            {"name": "Last.fm", "url": "https://last.fm/user/{}", "category": "music"},
            {"name": "Genius", "url": "https://genius.com/{}", "category": "music"},
            {"name": "Audiomack", "url": "https://audiomack.com/{}", "category": "music"},
            
            # ==================== GAMING ====================
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
            {"name": "Battle.net", "url": "https://battle.net/{}", "category": "gaming"},
            {"name": "Riot Games", "url": "https://riotgames.com/{}", "category": "gaming"},
            
            # ==================== PROFESSIONAL ====================
            {"name": "Upwork", "url": "https://upwork.com/fl/{}", "category": "freelance"},
            {"name": "Fiverr", "url": "https://fiverr.com/{}", "category": "freelance"},
            {"name": "Freelancer", "url": "https://freelancer.com/u/{}", "category": "freelance"},
            {"name": "Toptal", "url": "https://toptal.com/{}", "category": "freelance"},
            {"name": "AngelList", "url": "https://angel.co/u/{}", "category": "professional"},
            {"name": "Crunchbase", "url": "https://crunchbase.com/person/{}", "category": "business"},
            {"name": "ResearchGate", "url": "https://researchgate.net/profile/{}", "category": "academic"},
            {"name": "Academia.edu", "url": "https://academia.edu/{}", "category": "academic"},
            {"name": "Google Scholar", "url": "https://scholar.google.com/citations?user={}", "category": "academic"},
            {"name": "ORCID", "url": "https://orcid.org/{}", "category": "academic"},
            
            # ==================== OTHER ====================
            {"name": "Wikipedia", "url": "https://wikipedia.org/wiki/User:{}", "category": "wiki"},
            {"name": "Fandom", "url": "https://fandom.com/wiki/User:{}", "category": "wiki"},
            {"name": "Archive.org", "url": "https://archive.org/details/@{}", "category": "archive"},
            {"name": "Patreon", "url": "https://patreon.com/{}", "category": "funding"},
            {"name": "BuyMeACoffee", "url": "https://buymeacoffee.com/{}", "category": "funding"},
            {"name": "Ko-fi", "url": "https://ko-fi.com/{}", "category": "funding"},
            {"name": "Gumroad", "url": "https://gumroad.com/{}", "category": "funding"},
            {"name": "Linktree", "url": "https://linktr.ee/{}", "category": "bio"},
            {"name": "Behance", "url": "https://behance.net/{}", "category": "creative"},
            {"name": "Dribbble", "url": "https://dribbble.com/{}", "category": "creative"},
            {"name": "ArtStation", "url": "https://artstation.com/{}", "category": "creative"},
            {"name": "DeviantArt", "url": "https://deviantart.com/{}", "category": "creative"},
            {"name": "Flickr", "url": "https://flickr.com/people/{}", "category": "photo"},
            {"name": "500px", "url": "https://500px.com/{}", "category": "photo"},
            {"name": "Unsplash", "url": "https://unsplash.com/@{}", "category": "photo"},
            {"name": "Pexels", "url": "https://pexels.com/@{}", "category": "photo"},
            {"name": "Goodreads", "url": "https://goodreads.com/{}", "category": "books"},
            {"name": "Letterboxd", "url": "https://letterboxd.com/{}", "category": "movies"},
            {"name": "IMDb", "url": "https://imdb.com/user/{}", "category": "movies"},
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
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        return list(set(p['category'] for p in self.platforms))