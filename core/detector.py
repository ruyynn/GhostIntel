#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Entity Detector (robust, works offline)"""

import re
import ipaddress
from dataclasses import dataclass, field
from typing import Optional, Tuple, List


@dataclass
class Entity:
    raw: str
    type: str          # username | email | domain | phone | ip | url
    normalized: str
    confidence: float
    country: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class EntityDetector:
    # Email pattern (RFC 5322 compliant)
    EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')
    
    # IP patterns
    IPV4_RE = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    IPV6_RE = re.compile(r'^[0-9a-fA-F:]+$')
    
    # URL pattern
    URL_RE = re.compile(r'^https?://', re.I)
    
    # Domain pattern with better TLD validation
    DOMAIN_RE = re.compile(r'^([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}$')
    
    # Phone patterns for 8 countries
    PHONE_PATTERNS = {
        'ID': re.compile(r'^(\+62|62|0)8[1-9]\d{6,10}$'),      # Indonesia
        'US': re.compile(r'^(\+1|1)?[2-9]\d{2}[2-9]\d{6}$'),    # USA
        'GB': re.compile(r'^(\+44|44|0)[1-9]\d{9,10}$'),        # UK
        'MY': re.compile(r'^(\+60|60|0)1\d{8,9}$'),              # Malaysia
        'IN': re.compile(r'^(\+91|91|0)[6-9]\d{9}$'),            # India
        'AU': re.compile(r'^(\+61|61|0)[2-9]\d{8}$'),            # Australia
        'SG': re.compile(r'^(\+65|65)[6-9]\d{7}$'),              # Singapore
        'PH': re.compile(r'^(\+63|63|0)9\d{9}$'),                # Philippines
        'TH': re.compile(r'^(\+66|66|0)[689]\d{8}$'),            # Thailand
        'VN': re.compile(r'^(\+84|84|0)[3-9]\d{8}$'),            # Vietnam
    }
    
    # Country code mapping
    CC_MAP = {
        '62': 'ID', '1': 'US', '44': 'GB', '60': 'MY', '91': 'IN',
        '61': 'AU', '65': 'SG', '63': 'PH', '66': 'TH', '84': 'VN'
    }
    
    # Common TLDs for domain detection
    COMMON_TLDS = {
        'com', 'net', 'org', 'io', 'co', 'id', 'uk', 'gov', 'edu', 'my', 'sg',
        'info', 'biz', 'app', 'dev', 'tech', 'ai', 'cloud', 'store', 'shop',
        'tv', 'me', 'us', 'au', 'in', 'jp', 'kr', 'cn', 'de', 'fr', 'nl',
        'ru', 'br', 'it', 'es', 'ca', 'au', 'nz', 'za', 'in', 'sg', 'my',
        'ph', 'th', 'vn', 'hk', 'tw', 'kr', 'jp'
    }
    
    # Username blacklist (common patterns that are not usernames)
    USERNAME_BLACKLIST = {
        'admin', 'administrator', 'root', 'support', 'help', 'info',
        'contact', 'webmaster', 'postmaster', 'mailer-daemon', 'noreply'
    }
    
    def detect(self, text: str) -> Entity:
        """
        Detect entity type from input string
        Returns Entity object with type and normalized value
        """
        text = text.strip()
        if not text:
            return Entity(raw=text, type='unknown', normalized='', confidence=0.0)
        
        # 1. Email (highest priority)
        if self.EMAIL_RE.match(text):
            return Entity(
                raw=text,
                type='email',
                normalized=text.lower(),
                confidence=1.0,
                metadata={'domain': text.split('@')[1].lower()}
            )
        
        # 2. URL → extract domain
        if self.URL_RE.match(text):
            from urllib.parse import urlparse
            parsed = urlparse(text)
            domain = parsed.netloc.split(':')[0]
            if domain.startswith('www.'):
                domain = domain[4:]
            return Entity(
                raw=text,
                type='domain',
                normalized=domain,
                confidence=0.95,
                metadata={'url': text, 'scheme': parsed.scheme}
            )
        
        # 3. Domain (with better TLD validation)
        if self.DOMAIN_RE.match(text) and '.' in text:
            # Extract TLD
            parts = text.rsplit('.', 1)
            tld = parts[-1].lower()
            
            # Check if TLD is valid or looks like domain
            if tld in self.COMMON_TLDS or len(tld) <= 3:
                d = text.lower()
                if d.startswith('www.'):
                    d = d[4:]
                return Entity(
                    raw=text,
                    type='domain',
                    normalized=d,
                    confidence=0.9,
                    metadata={'tld': tld}
                )
        
        # 4. IPv4
        if self.IPV4_RE.match(text):
            try:
                ip = ipaddress.ip_address(text)
                if ip.is_private:
                    confidence = 0.95
                else:
                    confidence = 1.0
                return Entity(
                    raw=text,
                    type='ip',
                    normalized=str(ip),
                    confidence=confidence,
                    metadata={'version': 4, 'is_private': ip.is_private}
                )
            except ValueError:
                pass
        
        # 5. IPv6
        if ':' in text and self.IPV6_RE.match(text):
            try:
                ip = ipaddress.ip_address(text)
                return Entity(
                    raw=text,
                    type='ip',
                    normalized=str(ip),
                    confidence=1.0,
                    metadata={'version': 6}
                )
            except ValueError:
                pass
        
        # 6. Phone number (with multi-country support)
        cleaned = re.sub(r'[\s\-\(\)\.]', '', text)
        digits = re.sub(r'\D', '', cleaned)
        
        if 8 <= len(digits) <= 15:
            # Try to detect country from country code
            detected_iso = None
            for code, iso in self.CC_MAP.items():
                if digits.startswith(code):
                    detected_iso = iso
                    break
            
            for iso, pattern in self.PHONE_PATTERNS.items():
                if pattern.match(cleaned):
                    # Normalize to digits only
                    norm = digits
                    if digits.startswith('0'):
                        # Local format without country code
                        cc = {v: k for k, v in self.CC_MAP.items()}.get(iso, '')
                        norm = cc + digits[1:] if cc else digits
                    
                    # Add to metadata
                    metadata = {
                        'country_code': digits[:2] if len(digits) > 2 else '',
                        'local_format': digits if digits.startswith('0') else f"0{digits}" if len(digits) == 10 else digits
                    }
                    
                    return Entity(
                        raw=text,
                        type='phone',
                        normalized=norm,
                        confidence=0.95,
                        country=iso,
                        metadata=metadata
                    )
        
        # 7. Check if it's a UUID
        uuid_match = re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', text.lower())
        if uuid_match:
            return Entity(
                raw=text,
                type='uuid',
                normalized=text.lower(),
                confidence=0.85,
                metadata={'format': 'uuid'}
            )
        
        # 8. Check if it's a Bitcoin address
        bitcoin_match = re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', text)
        if bitcoin_match:
            return Entity(
                raw=text,
                type='bitcoin',
                normalized=text,
                confidence=0.85,
                metadata={'currency': 'BTC'}
            )
        
        # 9. Check if it's an Ethereum address
        eth_match = re.match(r'^0x[a-fA-F0-9]{40}$', text)
        if eth_match:
            return Entity(
                raw=text,
                type='ethereum',
                normalized=text.lower(),
                confidence=0.85,
                metadata={'currency': 'ETH'}
            )
        
        # 10. Default → username
        u = text.lstrip('@').lower()
        
        # Check blacklist
        if u in self.USERNAME_BLACKLIST:
            confidence = 0.5
        else:
            confidence = 0.8
        
        return Entity(
            raw=text,
            type='username',
            normalized=u,
            confidence=confidence,
            metadata={'original_case': text}
        )
    
    def detect_batch(self, texts: List[str]) -> List[Entity]:
        """Detect multiple texts in batch"""
        return [self.detect(t) for t in texts]
    
    def get_type_confidence(self, text: str, entity_type: str) -> float:
        """
        Get confidence for a specific entity type
        Returns 0.0 if not matching
        """
        entity = self.detect(text)
        if entity.type == entity_type:
            return entity.confidence
        return 0.0
    
    def is_email(self, text: str) -> bool:
        """Check if text is an email"""
        return bool(self.EMAIL_RE.match(text))
    
    def is_domain(self, text: str) -> bool:
        """Check if text is a domain"""
        return bool(self.DOMAIN_RE.match(text)) and '.' in text
    
    def is_ip(self, text: str) -> bool:
        """Check if text is an IP address"""
        try:
            ipaddress.ip_address(text)
            return True
        except ValueError:
            return False
    
    def is_phone(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Check if text is a phone number
        Returns (is_phone, country_iso)
        """
        cleaned = re.sub(r'[\s\-\(\)\.]', '', text)
        for iso, pattern in self.PHONE_PATTERNS.items():
            if pattern.match(cleaned):
                return True, iso
        return False, None
    
    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract all entities from a block of text
        Useful for parsing free-form text
        """
        entities = []
        
        # Split by common separators
        words = re.split(r'[\s,;:]+', text)
        
        for word in words:
            if word:
                entity = self.detect(word)
                if entity.confidence > 0.7:
                    entities.append(entity)
        
        # Remove duplicates
        seen = set()
        unique = []
        for e in entities:
            key = (e.type, e.normalized)
            if key not in seen:
                seen.add(key)
                unique.append(e)
        
        return unique


# Singleton instance
detector = EntityDetector()