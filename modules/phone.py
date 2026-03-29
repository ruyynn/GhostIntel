#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GhostIntel v2.5 - Phone Module (upgraded)"""

import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone as pn_tz
from typing import Dict, List, Optional
from datetime import datetime
from modules.base import BaseModule
from sources.phone_db import PhoneProviderDB


class PhoneModule(BaseModule):
    def __init__(self, session):
        super().__init__(session)
        self.name = "phone"
        self.provider_db = PhoneProviderDB()
        
        # Daftar negara yang didukung penuh
        self.supported_countries = ['ID', 'US', 'GB', 'MY', 'IN', 'AU', 'SG', 'PH', 'TH', 'VN']

    async def scan(self, phone: str) -> Dict:
        try:
            phone = phone.strip()
            parsed = None
            detected_country = None

            # Coba parse dengan semua negara yang didukung
            for country in self.supported_countries:
                try:
                    p = phonenumbers.parse(phone, country)
                    if phonenumbers.is_possible_number(p):
                        parsed = p
                        detected_country = country
                        break
                except Exception:
                    continue

            if not parsed:
                try:
                    parsed = phonenumbers.parse(phone, None)
                except Exception:
                    return self.error_result(phone, "Invalid phone number format")

            if not phonenumbers.is_valid_number(parsed):
                return self.error_result(phone, "Not a valid phone number")

            # Format numbers
            national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            rfc3966 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)

            # Country info
            country_iso = phonenumbers.region_code_for_number(parsed) or detected_country
            country_name = geocoder.description_for_number(parsed, "en") or "Unknown"
            location = geocoder.description_for_number(parsed, "en")
            if location == country_name:
                location = None

            # Provider detection
            prov = carrier.name_for_number(parsed, "en")
            if not prov and country_iso:
                # Clean E.164 for provider DB lookup
                clean_number = e164.lstrip('+')
                prov = self.provider_db.get_provider(clean_number, country_iso)
            
            # Special handling for some providers
            if prov:
                # Clean up provider names
                prov = prov.replace('Mobile', '').strip()
                prov = prov.replace('Pvt Ltd', '').strip()

            # Line type
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

            # Timezones
            tz = list(pn_tz.time_zones_for_number(parsed))
            is_mobile = num_type in (1, 2)

            # WhatsApp link for mobile
            wa_link = f"https://wa.me/{e164.lstrip('+')}" if is_mobile else None
            
            # Telegram link (always available)
            tg_link = f"https://t.me/{e164.lstrip('+')}" if is_mobile else None

            # Possible social handles
            digits_only = re.sub(r'\D', '', e164)
            possible_handles = self._make_handles(digits_only, country_iso)

            data = {
                'input': phone,
                'e164': e164,
                'national': national,
                'international': international,
                'rfc3966': rfc3966,
                'country_code': parsed.country_code,
                'country': country_name,
                'country_iso': country_iso,
                'location': location,
                'provider': prov or 'Unknown',
                'line_type': line_type,
                'is_mobile': is_mobile,
                'timezones': tz,
                'valid': True,
                'possible': phonenumbers.is_possible_number(parsed),
                'whatsapp_link': wa_link,
                'telegram_link': tg_link,
                'possible_handles': possible_handles,
                'formats': {
                    'e164': e164,
                    'international': international,
                    'national': national,
                    'rfc3966': rfc3966
                },
                'timestamp': datetime.now().isoformat()
            }

            sources = ['phonenumbers-lib']
            if prov and prov != 'Unknown':
                sources.append('provider_db')
            
            return self.create_result(phone, data, sources)

        except Exception as e:
            return self.error_result(phone, str(e))

    def _make_handles(self, digits: str, country: str) -> List[str]:
        """Generate possible social media handles from phone number"""
        handles = []
        
        # Original digits
        handles.append(digits)
        
        # Last digits variations
        if len(digits) >= 7:
            handles.append(digits[-7:])
        if len(digits) >= 8:
            handles.append(digits[-8:])
        if len(digits) >= 9:
            handles.append(digits[-9:])
        if len(digits) >= 10:
            handles.append(digits[-10:])
        
        # Country-specific local format
        if country == 'ID' and digits.startswith('62'):
            handles.append('0' + digits[2:])  # Local format: 08xx...
        elif country == 'GB' and digits.startswith('44'):
            handles.append('0' + digits[2:])  # Local format: 07xxx...
        elif country == 'MY' and digits.startswith('60'):
            handles.append('0' + digits[2:])  # Local format: 01x...
        elif country == 'IN' and digits.startswith('91'):
            handles.append(digits[2:])  # Local format: 9xxxx...
        elif country == 'AU' and digits.startswith('61'):
            handles.append('0' + digits[2:])  # Local format: 04xx...
        elif country == 'SG' and digits.startswith('65'):
            handles.append(digits[2:])  # SG uses 8-digit without leading 0
        elif country == 'PH' and digits.startswith('63'):
            handles.append('0' + digits[2:])  # Local format: 09xx...
        elif country == 'TH' and digits.startswith('66'):
            handles.append('0' + digits[2:])  # Local format: 08x...
        elif country == 'VN' and digits.startswith('84'):
            handles.append('0' + digits[2:])  # Local format: 09x...
        
        # Add with separators (for some platforms)
        if len(digits) >= 10:
            handles.append(digits[:4] + '-' + digits[4:7] + '-' + digits[7:])
            handles.append(digits[:3] + '-' + digits[3:6] + '-' + digits[6:])
        
        # Remove duplicates and filter
        handles = list(dict.fromkeys(handles))
        handles = [h for h in handles if len(h) >= 6 and h.isdigit()]
        
        return handles[:10]  # Return top 10 variations
    
    def get_country_info(self, country_iso: str) -> Dict:
        """Get additional country-specific info"""
        country_info = {
            'ID': {'name': 'Indonesia', 'whatsapp_prefix': '62', 'telegram_prefix': '62'},
            'US': {'name': 'United States', 'whatsapp_prefix': '1', 'telegram_prefix': '1'},
            'GB': {'name': 'United Kingdom', 'whatsapp_prefix': '44', 'telegram_prefix': '44'},
            'MY': {'name': 'Malaysia', 'whatsapp_prefix': '60', 'telegram_prefix': '60'},
            'IN': {'name': 'India', 'whatsapp_prefix': '91', 'telegram_prefix': '91'},
            'AU': {'name': 'Australia', 'whatsapp_prefix': '61', 'telegram_prefix': '61'},
            'SG': {'name': 'Singapore', 'whatsapp_prefix': '65', 'telegram_prefix': '65'},
            'PH': {'name': 'Philippines', 'whatsapp_prefix': '63', 'telegram_prefix': '63'},
            'TH': {'name': 'Thailand', 'whatsapp_prefix': '66', 'telegram_prefix': '66'},
            'VN': {'name': 'Vietnam', 'whatsapp_prefix': '84', 'telegram_prefix': '84'},
        }
        return country_info.get(country_iso, {})