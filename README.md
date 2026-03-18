# 👻 GhostIntel v2.0

**OSINT Framework Indonesia • Tools Investigasi Digital • 100% Public Data**

<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-ff6b6b?style=for-the-badge&logo=git&logoColor=white)]()
[![GitHub Stars](https://img.shields.io/github/stars/ruyynn/GhostIntel?style=for-the-badge&logo=github&logoColor=white&color=gold)](https://github.com/ruyynn/GhostIntel/stargazers)
[![Downloads](https://img.shields.io/badge/Downloads-1.2k+-brightgreen?style=for-the-badge&logo=download&logoColor=white)]()
[![Maintained](https://img.shields.io/badge/Maintained-Yes-success?style=for-the-badge&logo=maintenance&logoColor=white)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-9b59b6?style=for-the-badge&logo=githubactions&logoColor=white)](CONTRIBUTING.md)

</div>

---

## 📌 **Tentang GhostIntel**

**GhostIntel** adalah framework OSINT (Open Source Intelligence) pertama dari Indonesia yang dirancang khusus untuk memudahkan investigasi digital melalui sumber-sumber publik. Dikembangkan oleh **Ruyynn**, tools ini menggabungkan berbagai teknik OSINT menjadi satu mesin pencari intelijen yang **cepat**, **modular**, dan **mudah digunakan**.

### 🎯 **Use Case GhostIntel**

| Bidang | Kegunaan |
|--------|----------|
| 🔍 **OSINT Analyst** | Pengumpulan data target dari sumber terbuka |
| 🛡️ **Security Researcher** | Investigasi keamanan dan footprinting |
| 📚 **Mahasiswa/Dosen** | Materi pembelajaran keamanan siber |
| 🕵️ **Bug Bounty Hunter** | Reconnaissance tahap awal |
| 👮 **Penegak Hukum** | Investigasi digital (dengan izin resmi) |

---

## ✨ **Fitur Unggulan**

### 🔍 **Auto Entity Detection**
Tidak perlu pusing menentukan jenis target. GhostIntel otomatis mendeteksi!

```bash
┌──(ghostintel㉿localhost)-[~]
└─$ ghostintel investigate ruyynn        
[+] Detected: USERNAME

┌──(ghostintel㉿localhost)-[~]
└─$ ghostintel investigate mail@test.com
[+] Detected: EMAIL

┌──(ghostintel㉿localhost)-[~]
└─$ ghostintel investigate 08123456789    
[+] Detected: PHONE (Indonesia)

┌──(ghostintel㉿localhost)-[~]
└─$ ghostintel investigate example.com    
[+] Detected: DOMAIN

┌──(ghostintel㉿localhost)-[~]
└─$ ghostintel investigate 8.8.8.8        
[+] Detected: IP ADDRESS
```

## 📱 Phone OSINT - 5 Negara
Satu-satunya tools OSINT Indonesia dengan dukungan multi-country!

<details> <summary><b>🇮🇩 INDONESIA (62)</b></summary> <br>
       
```bash       
ghostintel -p 08123456789
```
```markdown
Informasi	Hasil

Provider	Telkomsel / Indosat / XL / Three / Smartfren

Type	Mobile / Fixed Line

Valid	✅ Ya

Format	+62 812-3456-789

Location	Jakarta / Jawa Barat / dll

Provider yang terdeteksi:

📱 Telkomsel: 0811, 0812, 0813, 0821, 0822, 0823, 0851, 0852, 0853

📱 Indosat: 0814, 0815, 0816, 0855, 0856, 0857, 0858

📱 XL: 0817, 0818, 0819, 0859, 0877, 0878, 0879

📱 Three: 0895, 0896, 0897, 0898, 0899

📱 Smartfren: 0881, 0882, 0883, 0884, 0885, 0886, 0887, 0888, 0889
```

</details><details> <summary><b>🇺🇸 USA (1)</b></summary> <br>

```bash
ghostintel -p +12125551234
```
```markdown
Informasi	Hasil

Provider	AT&T / Verizon / T-Mobile

Area Code	212 (New York)

Type	Mobile

Valid	✅ Ya

Area Codes:

📍 212: New York (AT&T)

📍 310: Los Angeles (T-Mobile)

📍 415: San Francisco (AT&T)

📍 617: Boston (Verizon)

📍 702: Las Vegas (T-Mobile)

📍 718: New York (Verizon)

📍 818: Los Angeles (AT&T)

📍 832: Houston (T-Mobile)
```

</details><details> <summary><b>🇬🇧 UK (44)</b></summary> <br>

```bash
ghostintel -p +447700123456
```
```markdown
Informasi	Hasil

Provider	EE / O2 / Vodafone / Three

Type	Mobile

Valid	✅ Ya

Mobile Prefixes:

📱 7700-7709: EE

📱 7710-7719: O2

📱 7720-7725: Vodafone

📱 7730-7735: Three

📱 7740-7742: O2

📱 7750-7752: EE
```
</details><details> <summary><b>🇲🇾 MALAYSIA (60)</b></summary> <br>
       
```bash
ghostintel -p +60123456789
```
```markdown
Informasi	Hasil

Provider	Maxis / Celcom / DiGi / U Mobile

Type	Mobile

Valid	✅ Ya

Mobile Prefixes:

📱 012, 017: Maxis

📱 013, 019: Celcom

📱 010, 016: DiGi

📱 011, 018: U Mobile

📱 014: Maxis/Celcom

📱 015: Tune Talk
```

</details><details> <summary><b>🇮🇳 INDIA (91)</b></summary> <br>

```bash
ghostintel -p +919876543210
```
```markdown
Informasi	Hasil

Provider	Airtel / Vodafone / Jio / BSNL

Type	Mobile

Valid	✅ Ya

Mobile Prefixes:

📱 9810-9819: Airtel

📱 9820-9825: Vodafone

📱 9870-9874: Jio

📱 8888-8890: BSNL

📱 9830-9834: Idea
```
</details>

## 👤 Username OSINT - 100+ Platform

*Cari username di seluruh platform sekaligus!*

```bash
ghostintel -u ruyynn
```
### Platform Lengkap (100+):

|Kategori	   |     Platform     |
|----------------|------------------|
|🌐 Social Media|	Twitter, Instagram, TikTok, Facebook, Pinterest, Snapchat, Tumblr, Mastodon|
|💻 Developer|   	GitHub, GitLab, Bitbucket, Replit, CodePen, Stack Overflow, HackerOne, Bugcrowd|
|🗣️ Forum|	       Reddit, Quora, HackerNews, Kaskus, Detik Forum, Indowebster|
|📝 Blog|	       Medium, Dev.to, Kompasiana, WordPress, Ghost, Blogger|
|💬 Messaging|	       Telegram, WhatsApp, Discord, Slack, Matrix, Signal|
|🎮 Gaming|	       Steam, Minecraft, Chess.com, Roblox, Epic Games, Xbox, PlayStation|
|💼 Professional|	LinkedIn, Upwork, Fiverr, Freelancer, Toptal, AngelList|
|🎵 Music|	       Spotify, SoundCloud, Last.fm, Bandcamp, ReverbNation, Mixcloud|
|🎬 Video|	       YouTube, Twitch, Vimeo, Dailymotion, Kick, Rumble|
|🇮🇩 Indonesian|  	Kaskus, Kompasiana, Detik Forum, Indowebster, Lintas.me|

---

## 📧 Email OSINT - DNS Investigator

Investigasi email sampai ke akar-akarnya!

```bash
ghostintel -e admin@example.com
```
```text
╔═══════════════════════════════════════╗
║         EMAIL INVESTIGATION           ║
╚═══════════════════════════════════════╝

📧 Email      : admin@example.com
👤 Username   : admin
🌐 Domain     : example.com

📋 DNS RECORDS:
├─ MX Records:
│  ├─ mail.example.com (priority 10)
│  └─ backup.example.com (priority 20)
├─ SPF Record : v=spf1 include:_spf.example.com ~all
├─ DMARC      : v=DMARC1; p=reject; rua=mailto:dmarc@example.com
└─ TXT Records: 3 records found

🖼️ Gravatar   : ✅ Found (admin@example.com)
📦 Disposable : ❌ No
💸 Free Provider : ❌ No (Custom domain)
```

## 🌐 Domain OSINT - DNS Recon

Scan domain secara mendalam!

```bash
ghostintel -d example.com
```
```text
╔═══════════════════════════════════════╗
║         DOMAIN INVESTIGATION          ║
╚═══════════════════════════════════════╝

🌐 Domain     : example.com

📡 DNS RECORDS:
├─ A Records  : 93.184.216.34, 2606:2800:220:1:248:1893:25c8:1946
├─ NS Records :
│  ├─ a.iana-servers.net
│  └─ b.iana-servers.net
├─ MX Records :
│  ├─ mail.example.com (10)
├─ TXT Records: v=spf1 -all
└─ SOA Record : a.iana-servers.net (2024021201)

🌍 WEBSITE INFO:
├─ HTTP Status: 200 OK
├─ Server     : ECS/example
├─ Title      : Example Domain
└─ HTTPS      : ✅ Enabled
```
## 🌍 IP OSINT - Geolocation & RDAP

Lacak IP address dengan akurat!

```bash
ghostintel -i 8.8.8.8
```
```text
╔═══════════════════════════════════════╗
║            IP INVESTIGATION           ║
╚═══════════════════════════════════════╝

🌍 IP Address : 8.8.8.8
📦 Version    : IPv4
🏠 Private    : ❌ No

📍 GEOLOCATION:
├─ Country    : United States
├─ City       : Mountain View
├─ Coordinates: 37.3860, -122.0838
├─ Timezone   : America/Los_Angeles
├─ ISP        : Google LLC
├─ Organization: Google Public DNS
└─ ASN        : AS15169 Google

🔄 Reverse DNS: dns.google

📋 RDAP INFO:
├─ RIR        : ARIN
├─ Handle     : NET-8-8-8-0-1
├─ Registered : 1992-12-01
└─ Organization: Google LLC
```

## 🧠 Correlation Engine - Intel Graph

GhostIntel menghubungkan semua data yang ditemukan!

```bash
ghostintel investigate ruyynn --report
```
```text
🔗 INTELLIGENCE CORRELATION
╔═══════════════════════════════════════╗
║                 ruyynn                ║
╚═══════════════════════════════════════╝
     ├─ 👤 USERNAME: ruyynn
     │    ├─ GitHub: https://github.com/ruyynn
     │    ├─ Twitter: https://twitter.com/ruyynn
     │    └─ Telegram: https://t.me/ruyynn
     │
     ├─ 📧 EMAIL: ruyynn@gmail.com
     │    ├─ Domain: gmail.com
     │    └─ Gravatar: ✅ Found
     │
     ├─ 🌐 DOMAIN: ruyynn.dev
     │    ├─ IP: 104.28.12.34
     │    ├─ Hosting: Cloudflare
     │    └─ Server: nginx
     │
     └─ 🌍 IP: 104.28.12.34
          ├─ Country: USA
          ├─ ISP: Cloudflare
          └─ Organization: Cloudflare Inc.
```

## 📊 Report Generator - Premium Output

Buat laporan profesional dengan 3 format!

```bash
# HTML Report (interaktif, keren!)
ghostintel investigate target --format html -o report.html

# JSON Report (untuk parsing lanjutan)
ghostintel investigate target --format json -o data.json

# TXT Report (simple, cepat)
ghostintel investigate target --format txt -o output.txt
```
### Fitur Report HTML:

🌓 Dark/Light theme toggle - Bisa ganti-ganti tema

🔍 Live search - Cari data dengan highlight

📋 Copy to clipboard - Salin data dengan sekali klik

📱 Fully responsive - Buka di HP juga oke

🖨️ Print-friendly - Siap cetak atau jadi PDF

⚡ Fast loading - Optimized performance

🎨 Modern UI - Tampilan kekinian

---

## 🚀 Cara Install

Metode 1: Clone Repository

```bash
# Clone repo
git clone https://github.com/ruyynn/GhostIntel.git
cd GhostIntel

# Install dependencies
pip install -r requirements.txt

# Jalankan
python ghostintel.py -h
```

Metode 2: Virtual Environment (Rekomendasi)

```bash
# Buat virtual env
python -m venv venv

# Aktifkan (Linux/Mac)
source venv/bin/activate
# Atau (Windows)
venv\Scripts\activate

# Install
pip install -r requirements.txt
python ghostintel.py -h
```

## 📖 Panduan Lengkap

Basic Commands

```bash
# Help
python ghostintel.py -h

# Version
python ghostintel.py -v

# Username
python ghostintel.py -u username

# Email
python ghostintel.py -e email@example.com

# Phone (Indonesia)
python ghostintel.py -p 08123456789

# Phone (USA)
python ghostintel.py -p +12125551234

# Phone (UK)
python ghostintel.py -p +447700123456

# Phone (Malaysia)
python ghostintel.py -p +60123456789

# Phone (India)
python ghostintel.py -p +919876543210

# Domain
python ghostintel.py -d example.com

# IP
python ghostintel.py -i 8.8.8.8

# Auto-detect
python ghostintel.py investigate target
```

Report Generation

```bash
# Comprehensive report (semua module)
python ghostintel.py -u username --report

# HTML report dengan custom filename
python ghostintel.py -d example.com --format html -o example.com.html

# JSON report untuk parsing
python ghostintel.py -e email@example.com --format json -o email.json

# Text report simple
python ghostintel.py -p 08123456789 --format txt -o phone.txt
Advanced Options
bash
# Custom timeout (untuk target lambat)
python ghostintel.py -d example.com --timeout 30

# More threads (lebih cepat)
python ghostintel.py -u username --threads 50

# No colors (untuk output file)
python ghostintel.py -u username --no-color
```

## 📋 Requirements
```txt
Python 3.8+
aiohttp==3.9.0
beautifulsoup4==4.12.0
dnspython==2.6.0
phonenumbers==8.13.0
rich==13.7.0
tldextract==5.1.0
jinja2==3.1.0
aiofiles==23.2.0
colorama==0.4.6
```

## 🏗️ Struktur Project
```text
📁 ghostintel/
├── 📄 ghostintel.py           # Main entry point
├── 📄 requirements.txt        # Dependencies
├── 📄 README.md               # You are here
├── 📄 CONTRIBUTING.md         # Contribution guide
├── 📄 LICENSE                  # MIT License
│
├── 📁 core/                    # Core modules
│   ├── 📄 engine.py            # Main engine
│   ├── 📄 detector.py          # Entity detection
│   ├── 📄 banner.py            # UI banner
│   ├── 📄 utils.py             # Utilities
│   └── 📄 correlation.py       # Intel correlation
│
├── 📁 modules/                 # OSINT modules
│   ├── 📄 username.py          # Username checker (100+ platforms)
│   ├── 📄 email.py             # Email investigator
│   ├── 📄 phone.py             # Phone module (5 negara)
│   ├── 📄 domain.py            # Domain recon
│   └── 📄 ip.py                # IP lookup
│
├── 📁 sources/                  # Data sources
│   ├── 📄 social_media.py       # 100+ platform database
│   ├── 📄 phone_db.py           # Provider database multi-country
│   └── 📄 breach_db.py          # Public breach information
│
├── 📁 reports/                   # Report generator
│   ├── 📄 generator.py           # Report engine
│   ├── 📄 html_template.py       # HTML template with CSS/JS
│   └── 📄 json_formatter.py      # JSON formatter
│
└── 📁 output/                    # Auto-generated reports
```

## ⚠️ Legal Disclaimer

### Purpose
GhostIntel dibuat hanya untuk tujuan berikut:

- Edukasi dan pembelajaran cybersecurity
- Penelitian keamanan yang sah (legitimate security research)
- Pengujian pada sistem milik sendiri atau dengan izin
- Pengembangan kemampuan OSINT dan reconnaissance

### Data Sources
GhostIntel hanya menggunakan sumber data yang **bersifat publik**, seperti:

- Public DNS lookup
- Public RDAP / WHOIS records
- Informasi dari website publik
- API publik yang legal
- Data yang memang tersedia secara terbuka

### Prohibited Use
Penggunaan berikut **dilarang keras**:

- Doxing atau mengekspos data pribadi tanpa izin
- Stalking, harassment, atau intimidasi
- Aktivitas ilegal atau kriminal
- Mengakses sistem atau data tanpa otorisasi

### Responsibility
Dengan menggunakan GhostIntel, Anda setuju bahwa:

- Anda bertanggung jawab penuh atas penggunaan tool ini
- Anda akan mematuhi hukum yang berlaku di wilayah Anda
- Author tidak bertanggung jawab atas penyalahgunaan tool ini
---

## 📝 Lisensi
MIT License - Silakan gunakan, modifikasi, dan distribusikan dengan mencantumkan kredit kepada Ruyynn.

---

## 👨‍💻 Author

### **Ruyynn**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ruyynn)

---

### 📌 **Project Links**

| Link | Tujuan |
|------|--------|
| [![Project](https://img.shields.io/badge/Project-GhostIntel-2dd4bf?style=flat-square&logo=github)](https://github.com/ruyynn/GhostIntel) | Repository utama |
| [![Issues](https://img.shields.io/badge/Issues-Report%20Bug-ff6b6b?style=flat-square&logo=github)](https://github.com/ruyynn/GhostIntel/issues) | Laporkan bug |
| [![Discussions](https://img.shields.io/badge/Discussions-Join%20Diskusi-9b59b6?style=flat-square&logo=github)](https://github.com/ruyynn/GhostIntel/discussions) | Diskusi & saran |

## 🤝 Cara Berkontribusi

Kami sangat terbuka untuk kontribusi!

🍴 Fork repository ini

🌿 Buat branch baru (git checkout -b fitur-keren)

💻 Commit perubahan (git commit -m 'Add fitur keren')

📤 Push ke branch (git push origin fitur-keren)

🔄 Buka Pull Request

Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan lengkap.

## ⭐ **Dukungan & Star**

<div align="center">

### 🌟 **Dukung GhostIntel!** 🌟

[![GitHub stars](https://img.shields.io/github/stars/ruyynn/GhostIntel?style=for-the-badge&logo=github&logoColor=white&color=gold)](https://github.com/ruyynn/GhostIntel/stargazers)

</div>

Cara paling simple buat dukung GhostIntel:

| # | Cara | Emoji |
|---|------|-------|
| 1 | ⭐ **Beri star** di repository ini | `⭐` |
| 2 | 📢 **Share** ke teman-teman | `📢` |
| 3 | 🐛 **Laporkan** issues | `🐛` |
| 4 | 💡 **Saran** fitur baru | `💡` |
| 5 | 🤝 **Kontribusi** kode | `🤝` |

> Setiap star dan kontribusi sangat berarti untuk pengembangan tools ini! 💪

### 💖 **Support via Saweria / Ko-fi**

Support developer biar makin semangat ngoding! 🚀

| Platform | Link | Untuk |
|----------|------|-------|
| **🇮🇩 Saweria** | [<img src="https://user-images.githubusercontent.com/26188697/180601310-e82c63e4-412b-4c36-b7b5-7ba713c80380.png" width="150" alt="Saweria">](https://saweria.co/Ruyynn) | Untuk donor Indonesia |
| **🌍 Ko-fi** | [<img src="https://ko-fi.com/img/githubbutton_sm.svg" width="150" alt="Ko-fi">](https://ko-fi.com/H2H11W13IP) | Untuk donor internasional |

</div>

## 📞 **Contact**

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ruyynn)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://web.facebook.com/profile.php?id=61587795784907)
[![Gmail](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ruyynn25@gmail.com)

</div>

---

### 💬 **Mau Ngobrol Langsung?**

- 🐛 **Report bug** → [GitHub Issues](https://github.com/ruyynn/GhostIntel/issues)
- 💡 **Saran fitur** → [GitHub Discussions](https://github.com/ruyynn/GhostIntel/discussions)
- ❓ **Pertanyaan** → Bisa DM via sosial media di atas
- 🤝 **Kerjasama** → Email ke [Click Me](mailto:ruyynn25@gmail.com)

---

## 🙏 **Terima Kasih**

<div align="center">

**Terima kasih kepada semua kontributor, pengguna, dan donatur yang sudah mendukung GhostIntel!**  

Tools ini dibuat dengan ❤️ untuk kemajuan dunia keamanan siber di Indonesia.

---

![Star History](https://api.star-history.com/svg?repos=ruyynn/GhostIntel&type=Date)

---

**GhostIntel v2.0**  
*OSINT Framework Indonesia • 100% Public Data • Untuk Edukasi Keamanan Siber*

© 2026 Ruyynn. All Rights Reserved.

</div>
