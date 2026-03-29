#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.5 - Base Module
All modules inherit from this class
Enhanced with logging, retry, rate limiting, and caching
"""

import asyncio
import logging
import time
import aiohttp  # <-- TAMBAHKAN INI!
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from functools import wraps

# Setup logging
logger = logging.getLogger("ghostintel")


class BaseModule:
    """Base class for all OSINT modules - Enhanced v2.5"""
    
    def __init__(self, session):
        self.session = session
        self.name = "base"
        
        # Rate limiting settings
        self._last_request_time = 0
        self._min_request_interval = 0.05  # 50ms minimum between requests
        self._request_count = 0
        self._rate_limit_window = 60  # seconds
        self._max_requests_per_window = 60  # max 60 requests per minute
        
        # Retry settings
        self._max_retries = 3
        self._retry_delay = 1  # seconds
        self._retry_backoff = 2  # multiplier
        
        # Cache settings
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes default cache
        
        # Progress tracking
        self._progress_callback = None
        self._current_step = 0
        self._total_steps = 0
    
    async def scan(self, target: str) -> Dict[str, Any]:
        """
        Scan target and return results
        To be implemented by child classes
        """
        raise NotImplementedError
    
    def create_result(self, target: str, data: Dict, sources: list) -> Dict:
        """Create standardized result dictionary"""
        return {
            'module': self.name,
            'target': target,
            'data': data,
            'sources': sources,
            'timestamp': datetime.now().isoformat(),
            'version': '2.5.0'
        }
    
    def error_result(self, target: str, error: str) -> Dict:
        """Create error result"""
        logger.error(f"{self.name}: {error} for target {target}")
        return {
            'module': self.name,
            'target': target,
            'error': error,
            'timestamp': datetime.now().isoformat(),
            'version': '2.5.0'
        }
    
    # ==================== RATE LIMITING ====================
    
    async def _wait_for_rate_limit(self):
        """Wait if needed to respect rate limits"""
        now = time.time()
        
        # Check per-request minimum interval
        elapsed = now - self._last_request_time
        if elapsed < self._min_request_interval:
            await asyncio.sleep(self._min_request_interval - elapsed)
        
        self._last_request_time = time.time()
        self._request_count += 1
        
        # Check per-window rate limit
        if self._request_count > self._max_requests_per_window:
            logger.warning(f"{self.name}: Rate limit reached, waiting...")
            await asyncio.sleep(self._rate_limit_window)
            self._request_count = 0
    
    def set_rate_limit(self, requests_per_second: float = 20, 
                       min_interval: float = 0.05):
        """
        Set rate limiting parameters
        requests_per_second: maximum requests per second
        min_interval: minimum time between requests in seconds
        """
        self._max_requests_per_window = int(requests_per_second * self._rate_limit_window)
        self._min_request_interval = min_interval
    
    # ==================== RETRY MECHANISM ====================
    
    async def _retry_request(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with retry on failure
        """
        last_error = None
        delay = self._retry_delay
        
        for attempt in range(self._max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self._max_retries - 1:
                    logger.debug(f"{self.name}: Retry {attempt + 1}/{self._max_retries} after {delay}s: {e}")
                    await asyncio.sleep(delay)
                    delay *= self._retry_backoff
                else:
                    logger.error(f"{self.name}: All retries failed: {e}")
                    raise
        
        raise last_error
    
    def set_retry(self, max_retries: int = 3, delay: float = 1, backoff: int = 2):
        """Set retry parameters"""
        self._max_retries = max_retries
        self._retry_delay = delay
        self._retry_backoff = backoff
    
    # ==================== CACHING ====================
    
    def _get_cache_key(self, target: str, *args) -> str:
        """Generate cache key for target and arguments"""
        key_parts = [self.name, target]
        key_parts.extend(str(arg) for arg in args)
        return ":".join(key_parts)
    
    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Get result from cache if not expired"""
        if key in self._cache:
            result, timestamp = self._cache[key]
            if (datetime.now() - timestamp).total_seconds() < self._cache_ttl:
                logger.debug(f"{self.name}: Cache hit for {key}")
                return result
            else:
                del self._cache[key]
        return None
    
    def _save_to_cache(self, key: str, result: Dict):
        """Save result to cache"""
        self._cache[key] = (result, datetime.now())
        logger.debug(f"{self.name}: Cached {key}")
    
    def clear_cache(self):
        """Clear all cached results for this module"""
        self._cache.clear()
        logger.info(f"{self.name}: Cache cleared")
    
    def set_cache_ttl(self, ttl: int):
        """Set cache TTL in seconds"""
        self._cache_ttl = ttl
    
    # ==================== PROGRESS TRACKING ====================
    
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Set callback for progress updates
        callback(step, total, message)
        """
        self._progress_callback = callback
    
    def _update_progress(self, message: str = "", step: int = None):
        """Update progress if callback is set"""
        if self._progress_callback:
            current_step = step if step is not None else self._current_step
            self._progress_callback(current_step, self._total_steps, message)
    
    def set_total_steps(self, total: int):
        """Set total steps for progress tracking"""
        self._total_steps = total
        self._current_step = 0
    
    def increment_step(self, message: str = ""):
        """Increment current step and update progress"""
        self._current_step += 1
        self._update_progress(message)
    
    # ==================== UTILITY METHODS ====================
    
    async def _safe_request(self, url: str, method: str = 'GET', 
                           **kwargs) -> Optional[aiohttp.ClientResponse]:
        """
        Make a safe HTTP request with rate limiting and retry
        """
        async def _request():
            await self._wait_for_rate_limit()
            async with self.session.request(method, url, **kwargs) as resp:
                return resp
        
        try:
            return await self._retry_request(_request)
        except Exception as e:
            logger.error(f"{self.name}: Request failed for {url}: {e}")
            return None
    
    async def _fetch_json(self, url: str, **kwargs) -> Optional[Dict]:
        """Fetch and parse JSON with error handling"""
        resp = await self._safe_request(url, **kwargs)
        if resp and resp.status == 200:
            try:
                return await resp.json()
            except Exception as e:
                logger.error(f"{self.name}: JSON parse error for {url}: {e}")
        return None
    
    async def _fetch_text(self, url: str, **kwargs) -> Optional[str]:
        """Fetch text content with error handling"""
        resp = await self._safe_request(url, **kwargs)
        if resp and resp.status == 200:
            try:
                return await resp.text()
            except Exception as e:
                logger.error(f"{self.name}: Text fetch error for {url}: {e}")
        return None
    
    def _sanitize_target(self, target: str) -> str:
        """Sanitize target string"""
        return target.strip().lower()
    
    def _is_valid_domain(self, domain: str) -> bool:
        """Basic domain validation"""
        import re
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9](\.[a-zA-Z]{2,})+$'
        return bool(re.match(pattern, domain))
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Basic IP validation"""
        import ipaddress
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False
    
    # ==================== METRICS ====================
    
    def get_metrics(self) -> Dict:
        """Get module metrics"""
        return {
            'module': self.name,
            'request_count': self._request_count,
            'cache_size': len(self._cache),
            'cache_ttl': self._cache_ttl,
            'retry_settings': {
                'max_retries': self._max_retries,
                'delay': self._retry_delay,
                'backoff': self._retry_backoff
            },
            'rate_limit': {
                'min_interval': self._min_request_interval,
                'max_per_window': self._max_requests_per_window,
                'window_seconds': self._rate_limit_window
            }
        }