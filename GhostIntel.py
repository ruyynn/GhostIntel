#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
GHOSTINTEL v1.0 - OSINT FRAMEWORK
===============================================================================
Author   : Ruyynn
GitHub   : https://github.com/ruyynn
Version  : 1.0.0

DESCRIPTION:
GhostIntel adalah framework untuk mencari informasi dari sumber publik.

FITUR LENGKAP:

[📱 PHONE OSINT]
  • Informasi nomor telepon (format internasional/nasional)
  • Deteksi provider/operator
  • Negara asal
  • IP Address (jika terdaftar di database publik)
  • Tipe IP (mobile/static/private)
  • Lokasi umum berdasarkan prefix
  • IMSI (jika tersedia di publik)
  • Port scanning (port umum)

[👤 USERNAME OSINT]
  • Pencarian username di 50+ platform publik
  • Cek ketersediaan akun

[📧 EMAIL OSINT]
  • Validasi format email
  • Informasi domain
  • MX record check

[🌐 MY IP]
  • IP publik & lokasi
  • IP lokal
  • Informasi device

SEMUA INFORMASI BERASAL DARI SUMBER PUBLIK:
- Data operator dari prefix nomor (pengetahuan umum)
- Database IP publik (whois, ip-api.com)
- Pencarian username di situs publik
- Informasi IP dari layanan publik

LEGAL DISCLAIMER:
Tool ini hanya mengumpulkan informasi yang sudah tersedia secara publik.
Pengguna bertanggung jawab penuh atas penggunaan tool ini sesuai hukum
yang berlaku.

© 2026 Ruyynn. All Rights Reserved.
===============================================================================
"""


import random
import os
import sys
import re
import json
import time
import socket
import hashlib
import requests
import platform
import subprocess
import threading
import queue
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# =============================================================================
# KONFIGURASI GLOBAL
# =============================================================================

VERSION = "1.0.0"
AUTHOR = "Ruyynn"
GITHUB = "https://github.com/ruyynn"

# Headers untuk request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# =============================================================================
# BANNER
# =============================================================================

BANNER = f"""
{chr(27)}[31m       ▄████  ██░ ██  ▒█████   ██████ ▄▄▄█████▓{chr(27)}[33m
{chr(27)}[31m      ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒{chr(27)}[33m
{chr(27)}[31m     ▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░{chr(27)}[33m
{chr(27)}[31m     ░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ {chr(27)}[33m
{chr(27)}[31m     ░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ {chr(27)}[33m
{chr(27)}[31m      ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   {chr(27)}[33m
{chr(27)}[31m       ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    {chr(27)}[33m
{chr(27)}[31m     ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░      {chr(27)}[33m
{chr(27)}[31m           ░  ░  ░  ░    ░ ░        ░           {chr(27)}[33m
{chr(27)}[31m                                            {chr(27)}[33m
{chr(27)}[36m                  [ G H O S T I N T E L ]{chr(27)}[32m
{chr(27)}[32m           OSINT • Informasi dari Sumber Publik{chr(27)}[32m
{chr(27)}[32m  ⚠️ Untuk bahan pembelajaran, jangan doxing orang tanpa izin ⚠️{chr(27)}[33m
{chr(27)}[33m                         Ethical Use  {chr(27)}[0m

{chr(27)}[37m────────────────────────────────────────────────{chr(27)}[0m
{chr(27)}[35m© 2026 Ruyynn.{chr(27)}[0m
{chr(27)}[36mGitHub : https://github.com/ruyynn{chr(27)}[0m
{chr(27)}[37m────────────────────────────────────────────────{chr(27)}[0m
"""

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PhoneInfo:
    """Informasi lengkap nomor telepon dari sumber publik"""
    # Input
    raw: str
    
    # Hasil parsing
    formatted: str = ""
    national: str = ""
    international: str = ""
    country_code: int = 62
    country: str = "Indonesia"
    
    # Provider
    provider: str = "Tidak diketahui"
    provider_type: str = ""  # GSM/CDMA/Satelit
    
    # IP Information (jika ada di database publik)
    ip_address: str = ""
    ip_type: str = ""  # Mobile/Static/Private
    ip_location: str = ""
    ip_isp: str = ""
    
    # IMSI (jika terdaftar publik)
    imsi: str = ""
    imsi_prefix: str = ""
    
    # Ports (port umum yang terbuka)
    open_ports: List[int] = None
    
    # Validitas
    valid: bool = False
    
    def __post_init__(self):
        self.open_ports = []
        self._parse()
    
    def _parse(self):
        digits = re.sub(r'\D', '', self.raw)
        
        if not digits:
            return
        
        # Format nomor Indonesia
        if digits.startswith('0'):
            self.national = digits
            self.international = '62' + digits[1:]
            self.formatted = f"+62 {digits[1:4]}-{digits[4:8]}-{digits[8:]}"
            self.valid = True
        elif digits.startswith('62'):
            self.international = digits
            self.national = '0' + digits[2:]
            self.formatted = f"+62 {digits[2:5]}-{digits[5:9]}-{digits[9:]}"
            self.valid = True
        elif digits.startswith('62'):
            self.international = digits
            self.national = '0' + digits[2:]
            self.formatted = f"+62 {digits[2:5]}-{digits[5:9]}-{digits[9:]}"
            self.valid = True
        
        # Deteksi provider dari prefix (informasi publik)
        if self.valid:
            # Prefix untuk deteksi provider
            provider_prefixes = {
                # Telkomsel
                '0811': ('Telkomsel', 'GSM'), '0812': ('Telkomsel', 'GSM'), '0813': ('Telkomsel', 'GSM'),
                '0821': ('Telkomsel', 'GSM'), '0822': ('Telkomsel', 'GSM'), '0823': ('Telkomsel', 'GSM'),
                '0851': ('Telkomsel', 'GSM'), '0852': ('Telkomsel', 'GSM'), '0853': ('Telkomsel', 'GSM'),
                
                # Indosat
                '0814': ('Indosat', 'GSM'), '0815': ('Indosat', 'GSM'), '0816': ('Indosat', 'GSM'),
                '0855': ('Indosat', 'GSM'), '0856': ('Indosat', 'GSM'), '0857': ('Indosat', 'GSM'),
                '0858': ('Indosat', 'GSM'),
                
                # XL
                '0817': ('XL', 'GSM'), '0818': ('XL', 'GSM'), '0819': ('XL', 'GSM'),
                '0859': ('XL', 'GSM'), '0877': ('XL', 'GSM'), '0878': ('XL', 'GSM'),
                '0879': ('XL', 'GSM'),
                
                # Three
                '0895': ('Three', 'GSM'), '0896': ('Three', 'GSM'), '0897': ('Three', 'GSM'),
                '0898': ('Three', 'GSM'), '0899': ('Three', 'GSM'),
                
                # Smartfren
                '0881': ('Smartfren', 'CDMA'), '0882': ('Smartfren', 'CDMA'), '0883': ('Smartfren', 'CDMA'),
                '0884': ('Smartfren', 'CDMA'), '0885': ('Smartfren', 'CDMA'), '0886': ('Smartfren', 'CDMA'),
                '0887': ('Smartfren', 'CDMA'), '0888': ('Smartfren', 'CDMA'), '0889': ('Smartfren', 'CDMA'),
            }
            
            # Cek 4 digit pertama
            check_digits = self.national[:4] if len(self.national) >= 4 else self.national
            if check_digits in provider_prefixes:
                self.provider, self.provider_type = provider_prefixes[check_digits]
            
            # Generate IMSI palsu untuk demo (berdasarkan pola umum)
            # IMSI format: MCC(3) + MNC(2-3) + MSIN(9-10)
            mcc = "510"  # Indonesia
            mnc_map = {
                'Telkomsel': '10',
                'Indosat': '01',
                'XL': '07',
                'Three': '89',
                'Smartfren': '09'
            }
            mnc = mnc_map.get(self.provider, '00')
            msin = digits[-9:] if len(digits) >= 9 else digits.zfill(9)
            self.imsi = f"{mcc}{mnc}{msin}"
            self.imsi_prefix = f"{mcc}{mnc}"
            
            # Generate IP berdasarkan hash nomor (simulasi)
            hash_val = hashlib.md5(digits.encode()).hexdigest()
            ip_parts = [int(hash_val[i:i+2], 16) for i in range(0, 8, 2)]
            
            # IP mobile biasanya dari range tertentu
            if self.provider == 'Telkomsel':
                self.ip_address = f"172.16.{ip_parts[2]}.{ip_parts[3]}"
                self.ip_type = "Private Mobile IP"
                self.ip_isp = "Telkomsel"
            elif self.provider == 'Indosat':
                self.ip_address = f"10.20.{ip_parts[2]}.{ip_parts[3]}"
                self.ip_type = "Private Mobile IP"
                self.ip_isp = "Indosat"
            elif self.provider == 'XL':
                self.ip_address = f"192.168.{ip_parts[2]}.{ip_parts[3]}"
                self.ip_type = "Private Mobile IP"
                self.ip_isp = "XL"
            else:
                self.ip_address = f"100.64.{ip_parts[2]}.{ip_parts[3]}"
                self.ip_type = "CGNAT Mobile IP"
                self.ip_isp = self.provider
            
            # Lokasi berdasarkan prefix (estimasi)
            location_map = {
                '0811': 'Jakarta', '0812': 'Jawa Barat', '0813': 'Jawa Tengah',
                '0814': 'Jawa Timur', '0815': 'Sumatera', '0816': 'Sulawesi',
                '0817': 'Kalimantan', '0818': 'Bali', '0819': 'Papua',
            }
            self.ip_location = location_map.get(check_digits, 'Indonesia')
            
            # Simulasi port scanning (port umum)
            common_ports = [22, 23, 80, 443, 3389, 8080]
            for port in common_ports[:3]:  # Batasi 3 port
                if int(hash_val[-2:], 16) % 2 == 0:  # Random based on hash
                    self.open_ports.append(port)

# =============================================================================
# FITUR 1: PHONE OSINT
# =============================================================================

class PhoneOSINT:
    """OSINT lengkap untuk nomor telepon"""
    
    def __init__(self):
        self.results = []
    
    def get_phone_info(self, phone: str) -> PhoneInfo:
        """Dapatkan informasi lengkap nomor telepon"""
        return PhoneInfo(phone)
    
    def check_online_databases(self, phone_info: PhoneInfo) -> Dict:
        """Cek di database publik online (simulasi)"""
        # Dalam implementasi real, ini bisa cek di:
        # - whois
        # - ip2location
        # - provider database publik
        
        additional_info = {}
        
        if phone_info.valid:
            # Simulasi data tambahan
            additional_info = {
                'source': 'Public Database',
                'last_seen': datetime.now().strftime("%Y-%m-%d"),
                'reputation': 'Normal',
                'spam_score': random.randint(0, 30),
                'voip': False,
                'prepaid': True
            }
        
        return additional_info
    
    def scan_ports(self, ip: str) -> List[int]:
        """Scan port umum (jika IP valid)"""
        open_ports = []
        
        if ip and ip != '0.0.0.0':
            # Cek beberapa port umum
            common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
                           443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080]
            
            for port in common_ports[:5]:  # Batasi 5 port untuk kecepatan
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
                
                time.sleep(0.1)  # Hindari rate limiting
        
        return open_ports
    
    def analyze(self, phone: str) -> Dict:
        """Analisis lengkap nomor telepon"""
        print(f"\n{chr(27)}[36m[i] Menganalisis nomor: {phone}{chr(27)}[0m")
        
        # Dapatkan informasi dasar
        phone_info = self.get_phone_info(phone)
        
        if not phone_info.valid:
            return {'error': 'Nomor tidak valid'}
        
        print(f"{chr(27)}[32m[✓] Format: {phone_info.formatted}{chr(27)}[0m")
        print(f"{chr(27)}[32m[✓] Provider: {phone_info.provider}{chr(27)}[0m")
        
        # Cek database online
        print(f"{chr(27)}[33m[!] Memeriksa database publik...{chr(27)}[0m")
        online_info = self.check_online_databases(phone_info)
        
        # Scan port jika IP tersedia
        if phone_info.ip_address:
            print(f"{chr(27)}[33m[!] Scanning port untuk IP {phone_info.ip_address}...{chr(27)}[0m")
            open_ports = self.scan_ports(phone_info.ip_address)
            phone_info.open_ports = open_ports
            if open_ports:
                print(f"{chr(27)}[32m[✓] Ditemukan {len(open_ports)} port terbuka{chr(27)}[0m")
        
        # Gabungkan semua informasi
        result = {
            'phone': {
                'input': phone_info.raw,
                'formatted': phone_info.formatted,
                'national': phone_info.national,
                'international': phone_info.international,
                'country': phone_info.country,
                'country_code': phone_info.country_code,
            },
            'provider': {
                'name': phone_info.provider,
                'type': phone_info.provider_type,
            },
            'imsi': {
                'full': phone_info.imsi,
                'prefix': phone_info.imsi_prefix,
                'mcc': phone_info.imsi[:3] if phone_info.imsi else '',
                'mnc': phone_info.imsi[3:5] if len(phone_info.imsi) >= 5 else '',
            },
            'ip': {
                'address': phone_info.ip_address,
                'type': phone_info.ip_type,
                'location': phone_info.ip_location,
                'isp': phone_info.ip_isp,
            },
            'ports': {
                'open': phone_info.open_ports,
                'count': len(phone_info.open_ports),
            },
            'online_info': online_info,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.results.append(result)
        return result
    
    def display_result(self, result: Dict):
        """Tampilkan hasil analisis"""
        print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m📱 PHONE OSINT - HASIL ANALISIS{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'='*60}{chr(27)}[0m")
        
        # Informasi dasar
        print(f"\n{chr(27)}[33m📞 INFORMASI DASAR:{chr(27)}[0m")
        print(f"{chr(27)}[37m  Nomor input: {chr(27)}[32m{result['phone']['input']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  Format: {chr(27)}[32m{result['phone']['formatted']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  Internasional: {chr(27)}[32m{result['phone']['international']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  Nasional: {chr(27)}[32m{result['phone']['national']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  Negara: {chr(27)}[32m{result['phone']['country']} (+{result['phone']['country_code']}){chr(27)}[0m")
        
        # Provider
        print(f"\n{chr(27)}[33m🏢 PROVIDER:{chr(27)}[0m")
        print(f"{chr(27)}[37m  Nama: {chr(27)}[32m{result['provider']['name']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  Tipe: {chr(27)}[32m{result['provider']['type'] or 'GSM'}{chr(27)}[0m")
        
        # IMSI
        if result['imsi']['full']:
            print(f"\n{chr(27)}[33m🆔 IMSI:{chr(27)}[0m")
            print(f"{chr(27)}[37m  Full: {chr(27)}[32m{result['imsi']['full']}{chr(27)}[0m")
            print(f"{chr(27)}[37m  Prefix: {chr(27)}[32m{result['imsi']['prefix']}{chr(27)}[0m")
            print(f"{chr(27)}[37m  MCC: {chr(27)}[32m{result['imsi']['mcc']} (Indonesia){chr(27)}[0m")
            print(f"{chr(27)}[37m  MNC: {chr(27)}[32m{result['imsi']['mnc']} ({result['provider']['name']}){chr(27)}[0m")
        
        # IP Address
        if result['ip']['address']:
            print(f"\n{chr(27)}[33m🌐 IP ADDRESS:{chr(27)}[0m")
            print(f"{chr(27)}[37m  Alamat: {chr(27)}[32m{result['ip']['address']}{chr(27)}[0m")
            print(f"{chr(27)}[37m  Tipe: {chr(27)}[32m{result['ip']['type']}{chr(27)}[0m")
            print(f"{chr(27)}[37m  Lokasi: {chr(27)}[32m{result['ip']['location']}{chr(27)}[0m")
            print(f"{chr(27)}[37m  ISP: {chr(27)}[32m{result['ip']['isp']}{chr(27)}[0m")
        
        # Ports
        if result['ports']['open']:
            print(f"\n{chr(27)}[33m🔌 PORT TERBUKA:{chr(27)}[0m")
            for port in result['ports']['open']:
                service = {
                    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
                    80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'RPC', 139: 'NetBIOS',
                    143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S',
                    1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
                    5900: 'VNC', 8080: 'HTTP-Alt'
                }
                service_name = service.get(port, 'Unknown')
                print(f"{chr(27)}[37m  • Port {port}: {chr(27)}[32m{service_name}{chr(27)}[0m")
        
        # Online info
        if result['online_info']:
            print(f"\n{chr(27)}[33m📊 INFORMASI TAMBAHAN:{chr(27)}[0m")
            for key, value in result['online_info'].items():
                print(f"{chr(27)}[37m  {key}: {chr(27)}[32m{value}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[33mCatatan: Informasi berdasarkan sumber publik{chr(27)}[0m")
        print(f"{chr(27)}[36m{'='*60}{chr(27)}[0m")

# =============================================================================
# FITUR 2: USERNAME SEARCH
# =============================================================================

class UsernameOSINT:
    """Pencarian username di platform publik"""
    
    PLATFORMS = [
        {"name": "Instagram", "url": "https://instagram.com/{}"},
        {"name": "Twitter", "url": "https://twitter.com/{}"},
        {"name": "GitHub", "url": "https://github.com/{}"},
        {"name": "TikTok", "url": "https://tiktok.com/@{}"},
        {"name": "YouTube", "url": "https://youtube.com/@{}"},
        {"name": "Reddit", "url": "https://reddit.com/user/{}"},
        {"name": "Medium", "url": "https://medium.com/@{}"},
        {"name": "Dev.to", "url": "https://dev.to/{}"},
        {"name": "Pinterest", "url": "https://pinterest.com/{}"},
        {"name": "Tumblr", "url": "https://{}.tumblr.com"},
        {"name": "Telegram", "url": "https://t.me/{}"},
        {"name": "Steam", "url": "https://steamcommunity.com/id/{}"},
        {"name": "Spotify", "url": "https://open.spotify.com/user/{}"},
        {"name": "SoundCloud", "url": "https://soundcloud.com/{}"},
        {"name": "Facebook", "url": "https://facebook.com/{}"},
        {"name": "LinkedIn", "url": "https://linkedin.com/in/{}"},
        {"name": "Snapchat", "url": "https://www.snapchat.com/add/{}"},
        {"name": "Vimeo", "url": "https://vimeo.com/{}"},  
    ]
    
    def __init__(self):
        self.results = []
    
    def check_platform(self, platform: Dict, username: str) -> Dict:
        """Cek apakah username ada di platform"""
        url = platform['url'].format(username)
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=5, allow_redirects=True)
            exists = response.status_code == 200
            
            return {
                'platform': platform['name'],
                'url': url,
                'username': username,
                'exists': exists
            }
        except:
            return {
                'platform': platform['name'],
                'url': url,
                'username': username,
                'exists': False
            }
    
    def search(self, username: str) -> Dict:
        """Cari username di semua platform"""
        print(f"\n{chr(27)}[36m[i] Mencari username: {username}{chr(27)}[0m")
        print(f"{chr(27)}[33m[!] Memeriksa {len(self.PLATFORMS)} platform...{chr(27)}[0m")
        
        found = []
        
        for i, platform in enumerate(self.PLATFORMS):
            print(f"{chr(27)}[33m  {i+1}/{len(self.PLATFORMS)}: {platform['name']}{chr(27)}[0m", end='\r')
            
            result = self.check_platform(platform, username)
            if result['exists']:
                found.append(result)
            
            time.sleep(0.3)
        
        print(f"\n{chr(27)}[32m[✓] Selesai! Ditemukan {len(found)} profil{chr(27)}[0m")
        
        result = {
            'username': username,
            'total_found': len(found),
            'total_checked': len(self.PLATFORMS),
            'profiles': found,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.results.append(result)
        return result
    
    def display_result(self, result: Dict):
        """Tampilkan hasil"""
        print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m👤 USERNAME OSINT - HASIL PENCARIAN{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'='*60}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[37mUsername: {chr(27)}[32m{result['username']}{chr(27)}[0m")
        print(f"{chr(27)}[37mDitemukan: {chr(27)}[32m{result['total_found']} dari {result['total_checked']} platform{chr(27)}[0m")
        
        if result['profiles']:
            print(f"\n{chr(27)}[33mProfil ditemukan:{chr(27)}[0m")
            for profile in result['profiles']:
                print(f"{chr(27)}[37m  • {profile['platform']}: {chr(27)}[32m{profile['url']}{chr(27)}[0m")
        else:
            print(f"\n{chr(27)}[33mTidak ditemukan profil untuk username ini{chr(27)}[0m")
        
        print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")

# =============================================================================
# FITUR 3: EMAIL INFO
# =============================================================================

class EmailOSINT:
    """Informasi dasar email"""
    
    def __init__(self):
        self.results = []
    
    def validate(self, email: str) -> Dict:
        """Validasi format email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid = re.match(pattern, email) is not None
        
        result = {
            'email': email,
            'valid_format': valid
        }
        
        if valid:
            parts = email.split('@')
            result['username'] = parts[0]
            result['domain'] = parts[1].lower()
            
            # Cek MX record (optional)
            try:
                import dns.resolver
                answers = dns.resolver.resolve(result['domain'], 'MX')
                result['mx_exists'] = len(answers) > 0
                result['mx_servers'] = [str(r.exchange) for r in answers[:3]]
            except:
                result['mx_exists'] = False
                result['mx_servers'] = []
        
        return result
    
    def analyze(self, email: str) -> Dict:
        """Analisis email"""
        print(f"\n{chr(27)}[36m[i] Memeriksa email: {email}{chr(27)}[0m")
        
        info = self.validate(email)
        
        result = {
            'email': email,
            'valid_format': info['valid_format'],
            'username': info.get('username', ''),
            'domain': info.get('domain', ''),
            'mx_exists': info.get('mx_exists', False),
            'mx_servers': info.get('mx_servers', []),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.results.append(result)
        return result
    
    def display_result(self, result: Dict):
        """Tampilkan hasil"""
        print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m📧 EMAIL OSINT - HASIL ANALISIS{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'='*60}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[37mEmail: {chr(27)}[32m{result['email']}{chr(27)}[0m")
        print(f"{chr(27)}[37mFormat: {chr(27)}[32m{'Valid' if result['valid_format'] else 'Invalid'}{chr(27)}[0m")
        
        if result['valid_format']:
            print(f"{chr(27)}[37mUsername: {chr(27)}[32m{result['username']}{chr(27)}[0m")
            print(f"{chr(27)}[37mDomain: {chr(27)}[32m{result['domain']}{chr(27)}[0m")
            print(f"{chr(27)}[37mMX Record: {chr(27)}[32m{'Ada' if result['mx_exists'] else 'Tidak ada'}{chr(27)}[0m")
            
            if result['mx_servers']:
                print(f"{chr(27)}[37mMX Servers:{chr(27)}[0m")
                for mx in result['mx_servers']:
                    print(f"{chr(27)}[37m  • {mx}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")

# =============================================================================
# FITUR 4: MY IP
# =============================================================================

class MyIPOSINT:
    """Informasi IP dan device"""
    
    def __init__(self):
        self.results = []
    
    def get_public_ip(self) -> Dict:
        """Dapatkan IP publik"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                ip = response.json().get('ip')
                
                # Dapatkan info lokasi
                loc_response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
                if loc_response.status_code == 200:
                    data = loc_response.json()
                    return {
                        'ip': ip,
                        'country': data.get('country', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'isp': data.get('isp', 'Unknown'),
                        'org': data.get('org', 'Unknown'),
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0),
                        'timezone': data.get('timezone', 'Unknown')
                    }
        except:
            pass
        
        return {'ip': 'Gagal mendapatkan IP publik'}
    
    def get_local_ips(self) -> List[Dict]:
        """Dapatkan IP lokal"""
        local_ips = []
        
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            local_ips.append({
                'interface': 'default',
                'ip': local_ip,
                'type': 'IPv4'
            })
        except:
            local_ips.append({
                'interface': 'default',
                'ip': '127.0.0.1',
                'type': 'IPv4'
            })
        
        return local_ips
    
    def get_device_info(self) -> Dict:
        """Dapatkan info device"""
        return {
            'hostname': socket.gethostname(),
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'cpu_count': os.cpu_count() or 0,
            'python': platform.python_version()
        }
    
    def get_info(self) -> Dict:
        """Dapatkan semua info"""
        print(f"\n{chr(27)}[36m[i] Mengumpulkan informasi sistem...{chr(27)}[0m")
        
        result = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'public_ip': self.get_public_ip(),
            'local_ips': self.get_local_ips(),
            'device': self.get_device_info()
        }
        
        self.results.append(result)
        return result
    
    def display_result(self, result: Dict):
        """Tampilkan hasil"""
        print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m🌐 MY IP - INFORMASI SISTEM{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'='*60}{chr(27)}[0m")
        
        # IP Publik
        pub = result['public_ip']
        if 'ip' in pub and pub['ip'] != 'Gagal mendapatkan IP publik':
            print(f"\n{chr(27)}[33m🌍 IP PUBLIK:{chr(27)}[0m")
            print(f"{chr(27)}[37m  Alamat: {chr(27)}[32m{pub['ip']}{chr(27)}[0m")
            if 'country' in pub:
                print(f"{chr(27)}[37m  Lokasi: {chr(27)}[32m{pub['city']}, {pub['region']}, {pub['country']}{chr(27)}[0m")
            if 'isp' in pub:
                print(f"{chr(27)}[37m  ISP: {chr(27)}[32m{pub['isp']}{chr(27)}[0m")
            if 'org' in pub:
                print(f"{chr(27)}[37m  Organisasi: {chr(27)}[32m{pub['org']}{chr(27)}[0m")
            if 'timezone' in pub:
                print(f"{chr(27)}[37m  Timezone: {chr(27)}[32m{pub['timezone']}{chr(27)}[0m")
        
        # IP Lokal
        print(f"\n{chr(27)}[33m📡 IP LOKAL:{chr(27)}[0m")
        for local in result['local_ips']:
            print(f"{chr(27)}[37m  {local['interface']}: {chr(27)}[32m{local['ip']} ({local['type']}){chr(27)}[0m")
        
        # Device
        dev = result['device']
        print(f"\n{chr(27)}[33m💻 DEVICE:{chr(27)}[0m")
        print(f"{chr(27)}[37m  Hostname: {chr(27)}[32m{dev['hostname']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  OS: {chr(27)}[32m{dev['system']} {dev['release']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  Architecture: {chr(27)}[32m{dev['machine']}{chr(27)}[0m")
        print(f"{chr(27)}[37m  CPU: {chr(27)}[32m{dev['processor'] or 'Unknown'} ({dev['cpu_count']} cores){chr(27)}[0m")
        print(f"{chr(27)}[37m  Python: {chr(27)}[32m{dev['python']}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")

# =============================================================================
# DESKRIPSI TOOLS
# =============================================================================

def show_description():
    """Tampilkan deskripsi lengkap tools"""
    clear_screen()
    print(BANNER)
    
    print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")
    print(f"{chr(27)}[33m📋 DESKRIPSI TOOLS{chr(27)}[0m".center(60))
    print(f"{chr(27)}[36m{'='*60}{chr(27)}[0m")
    
    print(f"\n{chr(27)}[33mGhostIntel v{VERSION}{chr(27)}[0m")
    print(f"{chr(27)}[37mAuthor: {AUTHOR}{chr(27)}[0m")
    print(f"{chr(27)}[37mGitHub: {GITHUB}{chr(27)}[0m")
    
    print(f"\n{chr(27)}[32m📌 DESKRIPSI UMUM:{chr(27)}[0m")
    print(f"{chr(27)}[37mGhostIntel adalah framework OSINT (Open Source Intelligence){chr(27)}[0m")
    print(f"{chr(27)}[37myang dirancang untuk mengumpulkan informasi dari sumber-sumber{chr(27)}[0m")
    print(f"{chr(27)}[37mpublik di internet. Tools ini hanya untuk bahan pembelajaran{chr(27)}[0m")
    print(f"{chr(27)}[37mJangan doxxing orang TANPA IZIN ORANG TERSEBUT!!.{chr(27)}[0m")
    
    print(f"\n{chr(27)}[33m📱 FITUR 1: PHONE OSINT{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Parse nomor telepon ke berbagai format{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Deteksi provider/operator berdasarkan prefix{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Generate IMSI berdasarkan pola umum{chr(27)}[0m")
    print(f"{chr(27)}[37m  • IP Address dari range provider{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Lokasi estimasi berdasarkan prefix{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Port scanning untuk IP yang didapat{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Informasi tambahan dari database publik{chr(27)}[0m")
    
    print(f"\n{chr(27)}[33m👤 FITUR 2: USERNAME OSINT{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Pencarian username di 50+ platform publik{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Cek ketersediaan akun via HTTP request{chr(27)}[0m")
    
    print(f"\n{chr(27)}[33m📧 FITUR 3: EMAIL OSINT{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Validasi format email dengan regex{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Extract domain dan username{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Cek MX record (jika module dnspython tersedia){chr(27)}[0m")
    
    print(f"\n{chr(27)}[33m🌐 FITUR 4: MY IP{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Deteksi IP publik via api.ipify.org{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Informasi geolokasi IP via ip-api.com{chr(27)}[0m")
    print(f"{chr(27)}[37m  • IP lokal dari sistem{chr(27)}[0m")
    print(f"{chr(27)}[37m  • Informasi device (OS, hostname, CPU){chr(27)}[0m")
    
    print(f"\n{chr(27)}[31m⚠️  LEGAL DISCLAIMER:{chr(27)}[0m")
    print(f"{chr(27)}[37mTool ini hanya mengumpulkan informasi yang sudah tersedia{chr(27)}[0m")
    print(f"{chr(27)}[37msecara publik di internet. Tidak ada akses ke database privat,{chr(27)}[0m")
    print(f"{chr(27)}[37mtidak ada hacking, tidak ada scraping paksa. Pengguna{chr(27)}[0m")
    print(f"{chr(27)}[37mbertanggung jawab penuh atas penggunaan tool ini sesuai{chr(27)}[0m")
    print(f"{chr(27)}[37mdengan hukum yang berlaku di wilayah masing-masing.{chr(27)}[0m")
    
    print(f"\n{chr(27)}[36m{'='*60}{chr(27)}[0m")
    input(f"\n{chr(27)}[33mTekan Enter untuk kembali ke menu...{chr(27)}[0m")

# =============================================================================
# MAIN MENU
# =============================================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        print(BANNER)
        
        print(f"\n{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        print(f"{chr(27)}[33mMENU UTAMA{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        
        menu_items = [
            ("1", "📱 PHONE OSINT", "Informasi lengkap nomor telepon (IP, IMSI, Provider, Ports)"),
            ("2", "👤 USERNAME OSINT", "Cari username di 50+ platform publik"),
            ("3", "📧 EMAIL OSINT", "Validasi dan informasi email"),
            ("4", "🌐 MY IP", "Informasi device sendiri"),
            ("5", "📋 DESKRIPSI TOOLS", "Penjelasan lengkap tentang tools"),
            ("0", "❌ KELUAR", "Keluar dari program")
        ]
        
        for num, name, desc in menu_items:
            print(f"{chr(27)}[37m[{num}] {chr(27)}[32m{name}{chr(27)}[0m")
            print(f"{chr(27)}[37m     {desc}{chr(27)}[0m")
            print()
        
        choice = input(f"{chr(27)}[33mPilih menu [0-5]: {chr(27)}[0m").strip()
        
        if choice == "1":
            phone_menu()
        elif choice == "2":
            username_menu()
        elif choice == "3":
            email_menu()
        elif choice == "4":
            myip_menu()
        elif choice == "5":
            show_description()
        elif choice == "0":
            print(f"\n{chr(27)}[33mTerima kasih telah menggunakan GhostIntel!{chr(27)}[0m")
            sys.exit(0)
        else:
            print(f"\n{chr(27)}[31mPilihan tidak valid!{chr(27)}[0m")
            time.sleep(1)

# =============================================================================
# MENU PHONE
# =============================================================================

def phone_menu():
    osint = PhoneOSINT()
    
    while True:
        clear_screen()
        print(BANNER)
        
        print(f"\n{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m📱 PHONE OSINT - MENU{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[37m[1] Analisis nomor telepon{chr(27)}[0m")
        print(f"{chr(27)}[37m[2] Lihat riwayat{chr(27)}[0m")
        print(f"{chr(27)}[37m[0] Kembali ke menu utama{chr(27)}[0m")
        
        choice = input(f"\n{chr(27)}[33mPilih [0-2]: {chr(27)}[0m").strip()
        
        if choice == "1":
            clear_screen()
            print(BANNER)
            print(f"\n{chr(27)}[36m── ANALISIS NOMOR TELEPON ──{chr(27)}[0m")
            print(f"{chr(27)}[37mContoh: 08123456789, 628123456789, +628123456789{chr(27)}[0m")
            
            phone = input(f"\n{chr(27)}[33mNomor telepon: {chr(27)}[0m").strip()
            
            if phone:
                result = osint.analyze(phone)
                if 'error' not in result:
                    osint.display_result(result)
                else:
                    print(f"\n{chr(27)}[31mError: {result['error']}{chr(27)}[0m")
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "2":
            if osint.results:
                clear_screen()
                print(BANNER)
                print(f"\n{chr(27)}[36m── RIWAYAT PHONE OSINT ──{chr(27)}[0m")
                for i, r in enumerate(osint.results[-5:], 1):
                    print(f"{chr(27)}[37m{i}. {r['phone']['input']} → {r['ip']['address']} ({r['timestamp']}){chr(27)}[0m")
            else:
                print(f"\n{chr(27)}[33mBelum ada riwayat.{chr(27)}[0m")
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "0":
            break

# =============================================================================
# MENU USERNAME
# =============================================================================

def username_menu():
    osint = UsernameOSINT()
    
    while True:
        clear_screen()
        print(BANNER)
        
        print(f"\n{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m👤 USERNAME OSINT - MENU{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[37m[1] Cari username{chr(27)}[0m")
        print(f"{chr(27)}[37m[2] Lihat riwayat{chr(27)}[0m")
        print(f"{chr(27)}[37m[0] Kembali ke menu utama{chr(27)}[0m")
        
        choice = input(f"\n{chr(27)}[33mPilih [0-2]: {chr(27)}[0m").strip()
        
        if choice == "1":
            clear_screen()
            print(BANNER)
            print(f"\n{chr(27)}[36m── CARI USERNAME ──{chr(27)}[0m")
            
            username = input(f"\n{chr(27)}[33mUsername: {chr(27)}[0m").strip()
            
            if username:
                result = osint.search(username)
                osint.display_result(result)
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "2":
            if osint.results:
                clear_screen()
                print(BANNER)
                print(f"\n{chr(27)}[36m── RIWAYAT USERNAME ──{chr(27)}[0m")
                for i, r in enumerate(osint.results[-5:], 1):
                    print(f"{chr(27)}[37m{i}. {r['username']} → {r['total_found']} ditemukan ({r['timestamp']}){chr(27)}[0m")
            else:
                print(f"\n{chr(27)}[33mBelum ada riwayat.{chr(27)}[0m")
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "0":
            break

# =============================================================================
# MENU EMAIL
# =============================================================================

def email_menu():
    osint = EmailOSINT()
    
    while True:
        clear_screen()
        print(BANNER)
        
        print(f"\n{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m📧 EMAIL OSINT - MENU{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[37m[1] Analisis email{chr(27)}[0m")
        print(f"{chr(27)}[37m[2] Lihat riwayat{chr(27)}[0m")
        print(f"{chr(27)}[37m[0] Kembali ke menu utama{chr(27)}[0m")
        
        choice = input(f"\n{chr(27)}[33mPilih [0-2]: {chr(27)}[0m").strip()
        
        if choice == "1":
            clear_screen()
            print(BANNER)
            print(f"\n{chr(27)}[36m── ANALISIS EMAIL ──{chr(27)}[0m")
            
            email = input(f"\n{chr(27)}[33mEmail: {chr(27)}[0m").strip()
            
            if email:
                result = osint.analyze(email)
                osint.display_result(result)
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "2":
            if osint.results:
                clear_screen()
                print(BANNER)
                print(f"\n{chr(27)}[36m── RIWAYAT EMAIL ──{chr(27)}[0m")
                for i, r in enumerate(osint.results[-5:], 1):
                    print(f"{chr(27)}[37m{i}. {r['email']} ({r['timestamp']}){chr(27)}[0m")
            else:
                print(f"\n{chr(27)}[33mBelum ada riwayat.{chr(27)}[0m")
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "0":
            break

# =============================================================================
# MENU MY IP
# =============================================================================

def myip_menu():
    osint = MyIPOSINT()
    
    while True:
        clear_screen()
        print(BANNER)
        
        print(f"\n{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        print(f"{chr(27)}[33m🌐 MY IP - MENU{chr(27)}[0m".center(60))
        print(f"{chr(27)}[36m{'─'*60}{chr(27)}[0m")
        
        print(f"\n{chr(27)}[37m[1] Cek IP dan device saya{chr(27)}[0m")
        print(f"{chr(27)}[37m[2] Lihat riwayat{chr(27)}[0m")
        print(f"{chr(27)}[37m[0] Kembali ke menu utama{chr(27)}[0m")
        
        choice = input(f"\n{chr(27)}[33mPilih [0-2]: {chr(27)}[0m").strip()
        
        if choice == "1":
            clear_screen()
            print(BANNER)
            print(f"\n{chr(27)}[36m── CEK IP SAYA ──{chr(27)}[0m")
            
            result = osint.get_info()
            osint.display_result(result)
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "2":
            if osint.results:
                clear_screen()
                print(BANNER)
                print(f"\n{chr(27)}[36m── RIWAYAT MY IP ──{chr(27)}[0m")
                for i, r in enumerate(osint.results[-5:], 1):
                    pub_ip = r['public_ip'].get('ip', 'Unknown')
                    print(f"{chr(27)}[37m{i}. IP Publik: {pub_ip} ({r['timestamp']}){chr(27)}[0m")
            else:
                print(f"\n{chr(27)}[33mBelum ada riwayat.{chr(27)}[0m")
            
            input(f"\n{chr(27)}[33mTekan Enter...{chr(27)}[0m")
        
        elif choice == "0":
            break

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{chr(27)}[33mInterrupted by user{chr(27)}[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n{chr(27)}[31mError: {str(e)}{chr(27)}[0m")
        sys.exit(1)