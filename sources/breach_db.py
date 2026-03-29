#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GhostIntel v2.0 - Public Breach Database
Information about known data breaches (public information)
"""

from typing import Dict, List, Optional


class BreachDB:
    """Database of publicly known data breaches"""
    
    def __init__(self):
        self.breaches = self._load_breaches()
    
    def _load_breaches(self) -> List[Dict]:
        """Load public breach information"""
        return [
            {
                "name": "Adobe",
                "year": 2013,
                "records": 152000000,
                "description": "Adobe security breach exposed customer IDs, encrypted passwords, and password hints.",
                "data_types": ["emails", "passwords", "password_hints"]
            },
            {
                "name": "LinkedIn",
                "year": 2012,
                "records": 117000000,
                "description": "LinkedIn breach exposed email addresses and hashed passwords.",
                "data_types": ["emails", "passwords"]
            },
            {
                "name": "MySpace",
                "year": 2013,
                "records": 360000000,
                "description": "MySpace breach exposed email addresses, usernames, and SHA1 hashed passwords.",
                "data_types": ["emails", "usernames", "passwords"]
            },
            {
                "name": "Tumblr",
                "year": 2013,
                "records": 65000000,
                "description": "Tumblr breach exposed email addresses and SHA1 hashed passwords.",
                "data_types": ["emails", "passwords"]
            },
            {
                "name": "Dropbox",
                "year": 2012,
                "records": 68000000,
                "description": "Dropbox breach exposed email addresses and hashed passwords.",
                "data_types": ["emails", "passwords"]
            },
            {
                "name": "Yahoo",
                "year": 2013,
                "records": 3000000000,
                "description": "Yahoo breach exposed email addresses, passwords, and security questions.",
                "data_types": ["emails", "passwords", "security_questions"]
            },
            {
                "name": "Facebook",
                "year": 2019,
                "records": 533000000,
                "description": "Facebook breach exposed phone numbers, email addresses, and profile information.",
                "data_types": ["emails", "phone_numbers", "names", "locations"]
            },
            {
                "name": "Twitter",
                "year": 2022,
                "records": 5400000,
                "description": "Twitter breach exposed email addresses and phone numbers.",
                "data_types": ["emails", "phone_numbers"]
            },
            {
                "name": "Canva",
                "year": 2019,
                "records": 139000000,
                "description": "Canva breach exposed email addresses, usernames, and hashed passwords.",
                "data_types": ["emails", "usernames", "passwords"]
            },
            {
                "name": "Tokopedia",
                "year": 2020,
                "records": 91000000,
                "description": "Tokopedia breach exposed email addresses, names, and hashed passwords.",
                "data_types": ["emails", "names", "passwords"],
                "country": "ID"
            },
            {
                "name": "Bhinneka",
                "year": 2020,
                "records": 1200000,
                "description": "Bhinneka breach exposed customer data.",
                "data_types": ["emails", "names", "addresses"],
                "country": "ID"
            },
            {
                "name": "JD.ID",
                "year": 2020,
                "records": 14000000,
                "description": "JD.ID breach exposed customer information.",
                "data_types": ["emails", "names", "phone_numbers"],
                "country": "ID"
            }
        ]
    
    def get_all_breaches(self) -> List[Dict]:
        """Get all breaches"""
        return self.breaches
    
    def search_by_domain(self, domain: str) -> List[Dict]:
        """Search breaches by domain"""
        domain = domain.lower()
        results = []
        
        for breach in self.breaches:
            if domain in breach.get('name', '').lower():
                results.append(breach)
        
        return results
    
    def search_by_country(self, country: str) -> List[Dict]:
        """Search breaches by country"""
        country = country.upper()
        return [b for b in self.breaches if b.get('country') == country]
    
    def get_breach_names(self) -> List[str]:
        """Get list of breach names"""
        return [b['name'] for b in self.breaches]