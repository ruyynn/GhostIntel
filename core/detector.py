#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Entity Detector Module
Auto-detects entity types from user input
"""

import re
import ipaddress
from dataclasses import dataclass
from typing import Optional, Tuple
import tldextract


@dataclass
class Entity:
    """Represents a detected entity"""
    raw: str
    type: str  # username, email, domain, phone, ip
    normalized: str
    confidence: float  # 0.0 - 1.0
    country: Optional[str] = None
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class EntityDetector:
    """Detects entity types from input strings"""
    
    # Regex patterns
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    IP_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    URL_PATTERN = re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.IGNORECASE)
    
    # Phone patterns for supported countries
    PHONE_PATTERNS = {
        'ID': re.compile(r'^(\+62|62|0)8[1-9][0-9]{6,10}$'),  # Indonesia
        'US': re.compile(r'^(\+1|1)?[2-9][0-9]{2}[2-9][0-9]{6}$'),  # USA
        'GB': re.compile(r'^(\+44|44|0)[1-9][0-9]{9,10}$'),  # UK
        'MY': re.compile(r'^(\+60|60|0)1[0-9]{8,9}$'),  # Malaysia
        'IN': re.compile(r'^(\+91|91|0)[6-9][0-9]{9}$'),  # India
    }
    
    # Country codes mapping
    COUNTRY_CODES = {
        '62': 'ID', '1': 'US', '44': 'GB', '60': 'MY', '91': 'IN'
    }
    
    def detect(self, text: str) -> Entity:
        """
        Detect entity type from input string
        Returns Entity object with type and normalized value
        """
        text = text.strip()
        
        # 1. Check email
        if self.EMAIL_PATTERN.match(text):
            return Entity(
                raw=text,
                type="email",
                normalized=text.lower(),
                confidence=1.0
            )
        
        # 2. Check URL
        if self.URL_PATTERN.match(text):
            extracted = tldextract.extract(text)
            domain = f"{extracted.domain}.{extracted.suffix}"
            return Entity(
                raw=text,
                type="domain",
                normalized=domain,
                confidence=0.95,
                metadata={'url': text}
            )
        
        # 3. Check domain
        extracted = tldextract.extract(text)
        if extracted.suffix:
            domain = f"{extracted.domain}.{extracted.suffix}"
            return Entity(
                raw=text,
                type="domain",
                normalized=domain,
                confidence=0.9
            )
        
        # 4. Check IP
        if self.IP_PATTERN.match(text):
            try:
                ip = ipaddress.ip_address(text)
                return Entity(
                    raw=text,
                    type="ip",
                    normalized=str(ip),
                    confidence=1.0,
                    metadata={'version': ip.version}
                )
            except ValueError:
                pass
        
        # 5. Check phone (try all country patterns)
        cleaned = re.sub(r'[\s\-\(\)]', '', text)
        digits = re.sub(r'\D', '', cleaned)
        
        if 8 <= len(digits) <= 15:
            # Try to detect country from country code
            country = None
            for code, iso in self.COUNTRY_CODES.items():
                if digits.startswith(code):
                    country = iso
                    break
            
            # Try each pattern
            for iso, pattern in self.PHONE_PATTERNS.items():
                if pattern.match(cleaned):
                    # Normalize to E.164 format
                    if digits.startswith('0'):
                        if iso == 'ID':
                            normalized = '62' + digits[1:]
                        elif iso == 'GB':
                            normalized = '44' + digits[1:]
                        elif iso == 'MY':
                            normalized = '60' + digits[1:]
                        elif iso == 'IN':
                            normalized = '91' + digits[1:]
                        else:
                            normalized = digits
                    else:
                        normalized = digits
                    
                    return Entity(
                        raw=text,
                        type="phone",
                        normalized=normalized,
                        confidence=0.95,
                        country=iso,
                        metadata={'country_code': code if 'code' in locals() else None}
                    )
        
        # 6. Default to username
        username = text.lstrip('@')
        return Entity(
            raw=text,
            type="username",
            normalized=username,
            confidence=0.8
        )


# Singleton instance
detector = EntityDetector()