#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Phone Module
Multi-country phone number OSINT (ID, US, UK, MY, IN)
"""

import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from typing import Dict, List, Optional
from datetime import datetime

from modules.base import BaseModule
from sources.phone_db import PhoneProviderDB


class PhoneModule(BaseModule):
    """Phone OSINT - Real number parsing for 5 countries"""
    
    def __init__(self, session):
        super().__init__(session)
        self.name = "phone"
        self.provider_db = PhoneProviderDB()
        
        # Country codes mapping
        self.country_codes = {
            'ID': 62, 'US': 1, 'GB': 44, 'MY': 60, 'IN': 91
        }
    
    async def scan(self, phone: str) -> Dict:
        """Scan phone number"""
        try:
            # Clean input
            phone = phone.strip()
            
            # Try to parse with phonenumbers
            parsed = None
            detected_country = None
            
            # Try with different country defaults
            for country in ['ID', 'US', 'GB', 'MY', 'IN']:
                try:
                    parsed = phonenumbers.parse(phone, country)
                    if phonenumbers.is_possible_number(parsed):
                        detected_country = country
                        break
                except:
                    continue
            
            if not parsed:
                # Try without country
                try:
                    parsed = phonenumbers.parse(phone, None)
                except:
                    return self.error_result(phone, "Invalid phone number format")
            
            if not phonenumbers.is_valid_number(parsed):
                return self.error_result(phone, "Invalid phone number")
            
            # Get basic info
            national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
            # Get country info
            country_code = parsed.country_code
            country_iso = phonenumbers.region_code_for_number(parsed) or detected_country
            country_name = geocoder.description_for_number(parsed, "en") or "Unknown"
            
            # Get location (if available)
            location = geocoder.description_for_number(parsed, "en")
            if location == country_name:
                location = None
            
            # Get carrier/provider
            provider = carrier.name_for_number(parsed, "en")
            
            # If carrier not found, try our database
            if not provider and country_iso:
                provider = self.provider_db.get_provider(e164, country_iso)
            
            # Get line type
            num_type = phonenumbers.number_type(parsed)
            type_map = {
                0: "Fixed Line",
                1: "Mobile",
                2: "Fixed/Mobile",
                3: "Toll Free",
                4: "Premium Rate",
                5: "Shared Cost",
                6: "VoIP",
                7: "Personal Number",
                8: "Pager",
                9: "Universal Access",
                10: "Unknown"
            }
            line_type = type_map.get(num_type, "Unknown")
            
            # Get timezones
            tz = timezone.time_zones_for_number(parsed)
            
            # Check if mobile (for WhatsApp)
            is_mobile = num_type in [1, 2]  # Mobile or Fixed/Mobile
            
            result = {
                'input': phone,
                'e164': e164,
                'national': national,
                'international': international,
                'country_code': country_code,
                'country': country_name,
                'country_iso': country_iso,
                'location': location,
                'provider': provider or 'Unknown',
                'line_type': line_type,
                'is_mobile': is_mobile,
                'timezones': list(tz) if tz else [],
                'valid': True,
                'possible': phonenumbers.is_possible_number(parsed),
                'timestamp': datetime.now().isoformat()
            }
            
            # Add country-specific formatting
            result['formats'] = {
                'e164': e164,
                'international': international,
                'national': national,
                'rfc3966': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)
            }
            
            # Generate possible usernames from phone
            result['possible_usernames'] = self._generate_usernames(e164, country_iso)
            
            sources = ['phonenumbers']
            if provider and provider != 'Unknown':
                sources.append('provider_db')
            
            return self.create_result(phone, result, sources)
            
        except Exception as e:
            return self.error_result(phone, str(e))
    
    def _generate_usernames(self, phone: str, country: str) -> List[str]:
        """Generate possible usernames from phone number"""
        clean = phone.lstrip('+').replace(' ', '')
        usernames = [
            clean,
            clean[-9:],  # Last 9 digits
            clean[-8:],  # Last 8 digits
        ]
        
        # Country-specific formats
        if country == 'ID':
            if clean.startswith('62'):
                usernames.append('0' + clean[2:])  # Local format
        elif country == 'GB':
            if clean.startswith('44'):
                usernames.append('0' + clean[2:])  # UK local
        elif country == 'MY':
            if clean.startswith('60'):
                usernames.append('0' + clean[2:])  # Malaysia local
        elif country == 'IN':
            if clean.startswith('91'):
                usernames.append('0' + clean[2:])  # India local
        
        return list(set(usernames))[:10]