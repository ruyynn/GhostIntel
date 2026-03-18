#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Phone Provider Database
Multi-country mobile provider information
"""

from typing import Dict, Optional


class PhoneProviderDB:
    """Database of phone providers by country"""
    
    def __init__(self):
        self.providers = self._load_providers()
    
    def _load_providers(self) -> Dict:
        """Load provider database"""
        return {
            # Indonesia (62)
            'ID': {
                '0811': 'Telkomsel', '0812': 'Telkomsel', '0813': 'Telkomsel',
                '0821': 'Telkomsel', '0822': 'Telkomsel', '0823': 'Telkomsel',
                '0851': 'Telkomsel', '0852': 'Telkomsel', '0853': 'Telkomsel',
                '0814': 'Indosat', '0815': 'Indosat', '0816': 'Indosat',
                '0855': 'Indosat', '0856': 'Indosat', '0857': 'Indosat',
                '0858': 'Indosat', '0859': 'Indosat',
                '0817': 'XL', '0818': 'XL', '0819': 'XL',
                '0877': 'XL', '0878': 'XL', '0879': 'XL',
                '0895': 'Three', '0896': 'Three', '0897': 'Three',
                '0898': 'Three', '0899': 'Three',
                '0881': 'Smartfren', '0882': 'Smartfren', '0883': 'Smartfren',
                '0884': 'Smartfren', '0885': 'Smartfren', '0886': 'Smartfren',
                '0887': 'Smartfren', '0888': 'Smartfren', '0889': 'Smartfren',
            },
            
            # USA (1)
            'US': {
                '212': 'AT&T', '213': 'AT&T', '310': 'T-Mobile',
                '404': 'AT&T', '415': 'AT&T', '510': 'AT&T',
                '617': 'Verizon', '626': 'AT&T', '646': 'Verizon',
                '702': 'T-Mobile', '718': 'Verizon', '818': 'AT&T',
                '832': 'T-Mobile', '847': 'Verizon', '858': 'AT&T',
                '909': 'AT&T', '914': 'Verizon', '917': 'AT&T',
                '929': 'T-Mobile',
            },
            
            # UK (44)
            'GB': {
                '7700': 'EE', '7701': 'EE', '7702': 'EE', '7703': 'EE',
                '7704': 'EE', '7705': 'EE', '7706': 'EE', '7707': 'EE',
                '7708': 'EE', '7709': 'EE',
                '7710': 'O2', '7711': 'O2', '7712': 'O2', '7713': 'O2',
                '7714': 'O2', '7715': 'O2', '7716': 'O2', '7717': 'O2',
                '7718': 'O2', '7719': 'O2',
                '7720': 'Vodafone', '7721': 'Vodafone', '7722': 'Vodafone',
                '7723': 'Vodafone', '7724': 'Vodafone', '7725': 'Vodafone',
                '7730': 'Three', '7731': 'Three', '7732': 'Three',
                '7733': 'Three', '7734': 'Three', '7735': 'Three',
                '7740': 'O2', '7741': 'O2', '7742': 'O2',
                '7750': 'EE', '7751': 'EE', '7752': 'EE',
            },
            
            # Malaysia (60)
            'MY': {
                '010': 'DiGi', '011': 'U Mobile', '012': 'Maxis',
                '013': 'Celcom', '014': 'Maxis/Celcom', '015': 'Tune Talk',
                '016': 'DiGi', '017': 'Maxis', '018': 'U Mobile',
                '019': 'Celcom',
            },
            
            # India (91)
            'IN': {
                '9810': 'Airtel', '9811': 'Airtel', '9812': 'Airtel',
                '9818': 'Airtel', '9819': 'Airtel',
                '9820': 'Vodafone', '9821': 'Vodafone', '9822': 'Vodafone',
                '9824': 'Vodafone', '9825': 'Vodafone',
                '9830': 'Idea', '9831': 'Idea', '9832': 'Idea',
                '9833': 'Idea', '9834': 'Idea',
                '9870': 'Jio', '9871': 'Jio', '9872': 'Jio',
                '9873': 'Jio', '9874': 'Jio',
                '8888': 'BSNL', '8889': 'BSNL', '8890': 'BSNL',
            }
        }
    
    def get_provider(self, phone: str, country: str) -> Optional[str]:
        """
        Get provider for phone number
        phone: E.164 format (e.g., 62812345678)
        country: ISO country code (ID, US, GB, MY, IN)
        """
        if country not in self.providers:
            return None
        
        # Remove country code for matching
        if country == 'ID' and phone.startswith('62'):
            local = '0' + phone[2:]
        elif country == 'US' and phone.startswith('1'):
            local = phone[1:]
        elif country == 'GB' and phone.startswith('44'):
            local = '0' + phone[2:]
        elif country == 'MY' and phone.startswith('60'):
            local = '0' + phone[2:]
        elif country == 'IN' and phone.startswith('91'):
            local = phone[2:]
        else:
            local = phone
        
        # Try matching prefixes (longest first)
        country_providers = self.providers[country]
        
        # Sort prefixes by length (longest first)
        prefixes = sorted(country_providers.keys(), key=len, reverse=True)
        
        for prefix in prefixes:
            if local.startswith(prefix):
                return country_providers[prefix]
        
        return None