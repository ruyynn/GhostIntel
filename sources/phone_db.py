#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.5 - Phone Provider Database
Multi-country mobile provider information (8 countries)
"""

from typing import Dict, Optional


class PhoneProviderDB:
    """Database of phone providers by country - Enhanced v2.5"""
    
    def __init__(self):
        self.providers = self._load_providers()
    
    def _load_providers(self) -> Dict:
        """Load provider database - 8 countries"""
        return {
            # ==================== INDONESIA (62) ====================
            'ID': {
                # Telkomsel
                '0811': 'Telkomsel', '0812': 'Telkomsel', '0813': 'Telkomsel',
                '0821': 'Telkomsel', '0822': 'Telkomsel', '0823': 'Telkomsel',
                '0851': 'Telkomsel', '0852': 'Telkomsel', '0853': 'Telkomsel',
                # Indosat
                '0814': 'Indosat', '0815': 'Indosat', '0816': 'Indosat',
                '0855': 'Indosat', '0856': 'Indosat', '0857': 'Indosat',
                '0858': 'Indosat', '0859': 'Indosat',
                # XL Axiata
                '0817': 'XL', '0818': 'XL', '0819': 'XL',
                '0877': 'XL', '0878': 'XL', '0879': 'XL',
                # Three (Tri)
                '0895': 'Three', '0896': 'Three', '0897': 'Three',
                '0898': 'Three', '0899': 'Three',
                # Smartfren
                '0881': 'Smartfren', '0882': 'Smartfren', '0883': 'Smartfren',
                '0884': 'Smartfren', '0885': 'Smartfren', '0886': 'Smartfren',
                '0887': 'Smartfren', '0888': 'Smartfren', '0889': 'Smartfren',
                # By.U (Telkomsel)
                '0859': 'By.U',  # Note: 0859 also Indosat, but By.U is Telkomsel sub-brand
            },
            
            # ==================== USA (1) ====================
            'US': {
                # AT&T
                '212': 'AT&T', '213': 'AT&T', '404': 'AT&T', '415': 'AT&T',
                '510': 'AT&T', '626': 'AT&T', '818': 'AT&T', '858': 'AT&T',
                '909': 'AT&T', '917': 'AT&T',
                # Verizon
                '617': 'Verizon', '646': 'Verizon', '718': 'Verizon',
                '847': 'Verizon', '914': 'Verizon',
                # T-Mobile
                '310': 'T-Mobile', '702': 'T-Mobile', '832': 'T-Mobile',
                '929': 'T-Mobile',
                # Sprint (now part of T-Mobile)
                '816': 'T-Mobile/Sprint', '913': 'T-Mobile/Sprint',
            },
            
            # ==================== UK (44) ====================
            'GB': {
                # EE
                '7700': 'EE', '7701': 'EE', '7702': 'EE', '7703': 'EE',
                '7704': 'EE', '7705': 'EE', '7706': 'EE', '7707': 'EE',
                '7708': 'EE', '7709': 'EE',
                '7750': 'EE', '7751': 'EE', '7752': 'EE',
                # O2
                '7710': 'O2', '7711': 'O2', '7712': 'O2', '7713': 'O2',
                '7714': 'O2', '7715': 'O2', '7716': 'O2', '7717': 'O2',
                '7718': 'O2', '7719': 'O2',
                '7740': 'O2', '7741': 'O2', '7742': 'O2',
                # Vodafone
                '7720': 'Vodafone', '7721': 'Vodafone', '7722': 'Vodafone',
                '7723': 'Vodafone', '7724': 'Vodafone', '7725': 'Vodafone',
                # Three
                '7730': 'Three', '7731': 'Three', '7732': 'Three',
                '7733': 'Three', '7734': 'Three', '7735': 'Three',
            },
            
            # ==================== MALAYSIA (60) ====================
            'MY': {
                # Maxis
                '012': 'Maxis', '017': 'Maxis',
                # Celcom
                '013': 'Celcom', '019': 'Celcom',
                # DiGi
                '010': 'DiGi', '016': 'DiGi',
                # U Mobile
                '011': 'U Mobile', '018': 'U Mobile',
                # Others
                '014': 'Maxis/Celcom', '015': 'Tune Talk',
            },
            
            # ==================== INDIA (91) ====================
            'IN': {
                # Airtel
                '9810': 'Airtel', '9811': 'Airtel', '9812': 'Airtel',
                '9818': 'Airtel', '9819': 'Airtel',
                # Vodafone Idea (Vi)
                '9820': 'Vodafone Idea', '9821': 'Vodafone Idea', '9822': 'Vodafone Idea',
                '9824': 'Vodafone Idea', '9825': 'Vodafone Idea',
                # Idea (merged with Vodafone)
                '9830': 'Vodafone Idea', '9831': 'Vodafone Idea', '9832': 'Vodafone Idea',
                '9833': 'Vodafone Idea', '9834': 'Vodafone Idea',
                # Jio
                '9870': 'Jio', '9871': 'Jio', '9872': 'Jio',
                '9873': 'Jio', '9874': 'Jio',
                # BSNL
                '8888': 'BSNL', '8889': 'BSNL', '8890': 'BSNL',
            },
            
            # ==================== AUSTRALIA (61) - NEW ====================
            'AU': {
                # Telstra
                '0410': 'Telstra', '0411': 'Telstra', '0412': 'Telstra',
                '0413': 'Telstra', '0414': 'Telstra', '0415': 'Telstra',
                '0416': 'Telstra', '0417': 'Telstra', '0418': 'Telstra',
                '0419': 'Telstra',
                # Optus
                '0400': 'Optus', '0401': 'Optus', '0402': 'Optus',
                '0403': 'Optus', '0404': 'Optus', '0405': 'Optus',
                '0406': 'Optus', '0407': 'Optus', '0408': 'Optus',
                '0409': 'Optus',
                # Vodafone
                '0420': 'Vodafone', '0421': 'Vodafone', '0422': 'Vodafone',
                '0423': 'Vodafone', '0424': 'Vodafone', '0425': 'Vodafone',
                '0426': 'Vodafone', '0427': 'Vodafone', '0428': 'Vodafone',
                '0429': 'Vodafone',
                # Amaysim (uses Optus network)
                '0470': 'Amaysim', '0471': 'Amaysim', '0472': 'Amaysim',
                '0473': 'Amaysim', '0474': 'Amaysim', '0475': 'Amaysim',
                # Boost (uses Telstra network)
                '0480': 'Boost', '0481': 'Boost', '0482': 'Boost',
                # Others
                '0450': 'Vodafone', '0451': 'Vodafone', '0452': 'Vodafone',
                '0455': 'Optus', '0456': 'Optus', '0457': 'Optus',
                '0466': 'Telstra', '0467': 'Telstra', '0468': 'Telstra',
            },
            
            # ==================== SINGAPORE (65) - NEW ====================
            'SG': {
                # Singtel
                '8111': 'Singtel', '8112': 'Singtel', '8113': 'Singtel',
                '8114': 'Singtel', '8115': 'Singtel', '8116': 'Singtel',
                '8117': 'Singtel', '8118': 'Singtel', '8119': 'Singtel',
                '8120': 'Singtel', '8121': 'Singtel', '8122': 'Singtel',
                '8123': 'Singtel', '8124': 'Singtel', '8125': 'Singtel',
                '8126': 'Singtel', '8127': 'Singtel', '8128': 'Singtel',
                '8129': 'Singtel',
                # StarHub
                '8000': 'StarHub', '8001': 'StarHub', '8002': 'StarHub',
                '8003': 'StarHub', '8004': 'StarHub', '8005': 'StarHub',
                '8006': 'StarHub', '8007': 'StarHub', '8008': 'StarHub',
                '8009': 'StarHub',
                '8130': 'StarHub', '8131': 'StarHub', '8132': 'StarHub',
                '8133': 'StarHub', '8134': 'StarHub', '8135': 'StarHub',
                '8136': 'StarHub', '8137': 'StarHub', '8138': 'StarHub',
                '8139': 'StarHub',
                # M1
                '8100': 'M1', '8101': 'M1', '8102': 'M1', '8103': 'M1',
                '8104': 'M1', '8105': 'M1', '8106': 'M1', '8107': 'M1',
                '8108': 'M1', '8109': 'M1',
                '8140': 'M1', '8141': 'M1', '8142': 'M1', '8143': 'M1',
                '8144': 'M1', '8145': 'M1', '8146': 'M1', '8147': 'M1',
                '8148': 'M1', '8149': 'M1',
                # SIMBA (formerly TPG)
                '8800': 'SIMBA', '8801': 'SIMBA', '8802': 'SIMBA',
                '8803': 'SIMBA', '8804': 'SIMBA', '8805': 'SIMBA',
                '8806': 'SIMBA', '8807': 'SIMBA', '8808': 'SIMBA',
                '8809': 'SIMBA',
                # GOMO (Singtel MVNO)
                '8660': 'GOMO', '8661': 'GOMO', '8662': 'GOMO',
                '8663': 'GOMO', '8664': 'GOMO', '8665': 'GOMO',
                # Circles.Life (M1 MVNO)
                '8600': 'Circles.Life', '8601': 'Circles.Life', '8602': 'Circles.Life',
                '8603': 'Circles.Life', '8604': 'Circles.Life', '8605': 'Circles.Life',
            },
            
            # ==================== PHILIPPINES (63) - NEW ====================
            'PH': {
                # Globe
                '917': 'Globe', '918': 'Globe', '919': 'Globe',
                '920': 'Globe', '921': 'Globe', '922': 'Globe',
                '923': 'Globe', '924': 'Globe', '925': 'Globe',
                '926': 'Globe', '927': 'Globe', '928': 'Globe',
                '929': 'Globe',
                '905': 'Globe', '906': 'Globe', '907': 'Globe',
                '915': 'Globe', '916': 'Globe',
                '956': 'Globe', '957': 'Globe', '958': 'Globe',
                '959': 'Globe',
                # Smart
                '908': 'Smart', '909': 'Smart', '910': 'Smart',
                '911': 'Smart', '912': 'Smart', '913': 'Smart',
                '914': 'Smart',
                '918': 'Smart', '919': 'Smart',
                '920': 'Smart', '921': 'Smart', '922': 'Smart',
                '923': 'Smart', '924': 'Smart', '925': 'Smart',
                '926': 'Smart', '927': 'Smart', '928': 'Smart',
                '929': 'Smart',
                '938': 'Smart', '939': 'Smart', '940': 'Smart',
                '941': 'Smart', '942': 'Smart', '943': 'Smart',
                '944': 'Smart', '945': 'Smart', '946': 'Smart',
                '947': 'Smart', '948': 'Smart', '949': 'Smart',
                # DITO Telecommunity
                '991': 'DITO', '992': 'DITO', '993': 'DITO',
                '994': 'DITO', '995': 'DITO', '996': 'DITO',
                '997': 'DITO', '998': 'DITO', '999': 'DITO',
                # Sun Cellular (now part of Smart)
                '922': 'Smart/Sun', '923': 'Smart/Sun', '924': 'Smart/Sun',
                '925': 'Smart/Sun', '926': 'Smart/Sun', '927': 'Smart/Sun',
                '928': 'Smart/Sun', '929': 'Smart/Sun',
            },
        }
    
    def get_provider(self, phone: str, country: str) -> Optional[str]:
        """
        Get provider for phone number
        phone: E.164 format (e.g., 62812345678)
        country: ISO country code (ID, US, GB, MY, IN, AU, SG, PH)
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
        elif country == 'AU' and phone.startswith('61'):
            local = '0' + phone[2:]
        elif country == 'SG' and phone.startswith('65'):
            local = phone[2:]  # Singapore uses 8-digit without leading 0
        elif country == 'PH' and phone.startswith('63'):
            local = '0' + phone[2:]
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
    
    def get_all_countries(self) -> list:
        """Get list of supported countries"""
        return list(self.providers.keys())
    
    def get_provider_by_prefix(self, country: str, prefix: str) -> Optional[str]:
        """Get provider by specific prefix"""
        if country not in self.providers:
            return None
        return self.providers[country].get(prefix)