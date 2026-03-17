```
       ▄████  ██░ ██  ▒█████   ██████ ▄▄▄█████▓     
      ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒    
     ▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░    
     ░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░     
     ░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░     
      ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░       
       ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░        
     ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░          
           ░  ░  ░  ░    ░ ░        ░               
```

<div align="center">

# GhostIntel v2.0

**API-Less OSINT Mashup Engine**

[![Version](https://img.shields.io/badge/Versi-2.0.0-blue?style=for-the-badge)](https://github.com/ruyynn/GhostIntel)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge)](https://python.org)
[![License](https://img.shields.io/badge/Lisensi-MIT-red?style=for-the-badge)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Ruyynn-purple?style=for-the-badge)](https://github.com/ruyynn)
[![Stars](https://img.shields.io/github/stars/ruyynn/GhostIntel?style=social)](https://github.com/ruyynn/GhostIntel/stargazers)

*Update besar dari [GhostIntel v1.0](https://github.com/ruyynn/GhostIntel) — dibangun ulang dari nol dengan arsitektur async, lebih cepat, lebih lengkap.*

⚠️ **Untuk bahan pembelajaran. Jangan doxing orang tanpa izin.** ⚠️

</div>

---

## 📋 Deskripsi

GhostIntel v2.0 adalah **OSINT Mashup Engine** berbasis Python yang dirancang untuk melakukan pengumpulan informasi dari sumber publik secara cepat, legal, dan etis — **tanpa memerlukan API key apapun**.

Versi ini merupakan **rewrite penuh** dari v1.0 dengan arsitektur async, modul yang diperluas, sistem korelasi data antar modul, dan output report dalam berbagai format.

---

## ✨ Apa yang Baru di v2.0?

| Fitur | v1.0 | v2.0 |
|---|---|---|
| Arsitektur | Sync/Sequential | **Async/Concurrent** |
| Phone OSINT | Indonesia only | **ID, US, UK, MY, IN** |
| Username check | Beberapa platform | **100+ platform** |
| Domain OSINT | ❌ | **✅ DNS + HTTP** |
| IP OSINT | Basic | **✅ RDAP + Geolocation** |
| Auto-detect target | ❌ | **✅ EntityDetector** |
| Korelasi data | ❌ | **✅ CorrelationEngine** |
| Export report | ❌ | **✅ JSON / HTML / TXT** |
| API key required | Beberapa | **❌ Zero API keys** |
| Concurrent threads | 1 | **20 (configurable)** |

---

## 🚀 Fitur Utama

### 👤 Username OSINT
- Cek username di **100+ platform** secara bersamaan
- Kategorisasi: social, dev, gaming, musik, forum, profesional, Indonesia-specific
- Parse judul halaman untuk validasi profil aktif
- Generate variasi username dan possible emails

### 📧 Email OSINT
- Validasi format & cek MX records via DNS live
- Deteksi SPF dan DMARC record
- Cek Gravatar profile
- Identifikasi disposable email & free provider
- Generate variasi username dari email

### 📱 Phone OSINT (Multi-Country)
- Support **5 negara**: 🇮🇩 Indonesia, 🇺🇸 USA, 🇬🇧 UK, 🇲🇾 Malaysia, 🇮🇳 India
- Deteksi provider/operator dari prefix nomor
- Format output: E.164, International, National, RFC3966
- Deteksi jenis line (Mobile, Fixed, VoIP, dll)
- Timezone detection

### 🌐 Domain OSINT
- DNS records lengkap: **A, AAAA, NS, MX, TXT, SOA, CNAME**
- Cek HTTP/HTTPS status & server header
- Ambil title website otomatis
- Semua via live DNS query (bukan cache)

### 🌍 IP OSINT
- Geolocation via **ip-api.com** (gratis, tanpa key)
- Reverse DNS lookup
- **RDAP lookup** ke 5 RIR: ARIN, RIPE, APNIC, LACNIC, AFRINIC
- Deteksi private/loopback/multicast

### 🔗 Correlation Engine
- Menghubungkan data dari semua modul secara otomatis
- Ekstrak entitas: email, domain, IP, username, ASN, ISP
- Visualisasi tree di terminal

### 📊 Report Generator
- Export ke **JSON**, **HTML** (via Jinja2 template), atau **TXT**
- Auto-naming dengan timestamp
- Summary table per modul

---

## 🗂️ Struktur Project

```
GhostIntel/
├── ghostintel.py           # Entry point utama
├── requirements.txt
│
├── core/
│   ├── engine.py           # Orchestrator utama
│   ├── detector.py         # Auto-detect tipe target
│   ├── correlation.py      # Korelasi data antar modul
│   ├── banner.py           # CLI styling (Rich)
│   └── utils.py            # Help menu & utilities
│
├── modules/
│   ├── base.py             # Base class semua modul
│   ├── username.py         # Username checker (100+ platform)
│   ├── email.py            # Email investigator
│   ├── phone.py            # Phone number analyzer
│   ├── domain.py           # Domain DNS scanner
│   └── ip.py               # IP geolocation & RDAP
│
├── sources/
│   ├── social_media.py     # Database 100+ platform URL
│   ├── phone_db.py         # Database prefix → provider
│   └── breach_db.py        # Database breach publik
│
└── reports/
    ├── generator.py         # Report generator (JSON/HTML/TXT)
    ├── html_template.py     # Jinja2 HTML template
    └── json_formatter.py    # JSON serializer
```

---

## 🖥️ Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/ruyynn/GhostIntel.git
cd GhostIntel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan

```bash
python3 ghostintel.py --help
```

### Requirements

- Python 3.8+
- Linux / Windows / macOS

---

## 📌 Cara Penggunaan

### Auto-detect (Recommended)

```bash
python3 ghostintel.py investigate TARGET
```

GhostIntel akan otomatis mendeteksi apakah target adalah email, domain, IP, nomor telepon, atau username.

### Spesifik per Tipe

```bash
python3 ghostintel.py -u USERNAME        # Username
python3 ghostintel.py -e EMAIL           # Email
python3 ghostintel.py -p PHONE           # Phone
python3 ghostintel.py -d DOMAIN          # Domain
python3 ghostintel.py -i IP              # IP Address
```

### Generate Report

```bash
# HTML report
python3 ghostintel.py -u asep --report --format html

# JSON output ke file
python3 ghostintel.py -d example.com --format json -o hasil.json

# Text report
python3 ghostintel.py -p +62812345678 --report --format txt
```

### Contoh Lengkap

```bash
# Cek username
python3 ghostintel.py -u johndoe

# Investigasi nomor Indonesia
python3 ghostintel.py -p 081234567890

# Investigasi nomor US
python3 ghostintel.py -p +12125551234

# Domain recon dengan laporan HTML
python3 ghostintel.py -d example.com --report --format html -o hasil.html

# IP lookup
python3 ghostintel.py -i 8.8.8.8

# Email investigation
python3 ghostintel.py -e user@example.com

# Auto-detect + comprehensive report
python3 ghostintel.py investigate target@example.com --report
```

---

## 📱 Phone OSINT — Format per Negara

| Negara | Format Lokal | Format Internasional |
|--------|-------------|---------------------|
| 🇮🇩 Indonesia | `081234567890` | `+62 812-3456-7890` |
| 🇺🇸 USA | `(212) 555-1234` | `+1 212-555-1234` |
| 🇬🇧 UK | `07700 123456` | `+44 7700 123456` |
| 🇲🇾 Malaysia | `012-3456789` | `+60 12-3456789` |
| 🇮🇳 India | `09876543210` | `+91 98765 43210` |

---

## ⚙️ Opsi Lanjutan

| Opsi | Default | Deskripsi |
|------|---------|-----------|
| `--timeout` | 10 | Request timeout (detik) |
| `--threads` | 20 | Concurrent threads |
| `--format` | json | Format output: json / html / txt |
| `-o, --output` | auto | Nama file output |
| `--report` | false | Generate laporan lengkap |
| `--no-color` | false | Nonaktifkan warna terminal |

---

## 🧠 Kenapa GhostIntel?

- ✅ **Zero API Keys** — tidak perlu daftar ke layanan apapun
- ✅ **Async & Fast** — investigasi concurrent, bukan sequential
- ✅ **Multi-country** — tidak hanya Indonesia
- ✅ **Correlation** — data dari berbagai modul dihubungkan otomatis
- ✅ **Tidak hacking** — hanya menggunakan data publik
- ✅ **Tidak brute-force** — tidak mengakses database privat

---

## 🤝 Contributing

Kontribusi sangat terbuka! 🚀

1. 🍴 Fork repository
2. 🌿 Buat branch baru (`git checkout -b fitur-baru`)
3. 💾 Commit perubahan (`git commit -m 'Tambah fitur X'`)
4. 📤 Push ke branch (`git push origin fitur-baru`)
5. 🔄 Kirim Pull Request

Panduan lengkap: [CONTRIBUTING.md](Contributing.md)

---

## 📫 Author

[![GitHub](https://img.shields.io/badge/GitHub-Ruyynn-black?style=for-the-badge&logo=github)](https://github.com/ruyynn)
[![Instagram](https://img.shields.io/badge/Instagram-@ellreynn-purple?style=for-the-badge&logo=instagram)](https://www.instagram.com/ellreynn)
[![Email](https://img.shields.io/badge/Email-ruyynn25@gmail.com-red?style=for-the-badge&logo=gmail)](mailto:ruyynn25@gmail.com)

---

## ☕ Dukungan

Jika tools ini bermanfaat, boleh banget kasih ⭐ atau donasi:

[![Saweria](https://img.shields.io/badge/Donasi-Saweria-orange?style=for-the-badge)](https://saweria.co/Ruyynn)

---

## ⚠️ Disclaimer & Legal

### Tujuan Pembuatan

GhostIntel dibuat **semata-mata** untuk:
- ✅ Edukasi dan pembelajaran keamanan siber
- ✅ Riset keamanan yang sah
- ✅ Pengujian pada sistem milik sendiri
- ✅ Pengembangan skill OSINT untuk keperluan profesional

### Sumber Data

GhostIntel **HANYA** menggunakan:
- ✅ Sumber publik yang tersedia di internet
- ✅ API publik yang legal
- ✅ Data yang sudah terbuka untuk umum

### Larangan Penggunaan

**DILARANG KERAS** menggunakan GhostIntel untuk:
- ❌ Doxing (mengekspos data pribadi orang tanpa izin)
- ❌ Stalking atau pelecehan
- ❌ Pelanggaran privasi
- ❌ Aktivitas kriminal atau ilegal

> Dengan menggunakan GhostIntel, Anda bertanggung jawab penuh atas segala konsekuensi penggunaan tool ini. Author tidak bertanggung jawab atas penyalahgunaan.

---

## 📜 License

© 2026 Ruyynn. Licensed under the [MIT License](LICENSE).

Dilarang mendistribusikan ulang untuk tujuan komersial tanpa izin tertulis dari pembuat.

---

<div align="center">

**GhostIntel v2.0** — *OSINT Mashup Engine*

*Dibuat untuk pembelajaran • Gunakan dengan bijak • Hormati privasi orang lain*

*"Ilmu yang bermanfaat adalah ilmu yang digunakan untuk kebaikan, bukan untuk menyakiti sesama."*

[![Star Repo](https://img.shields.io/github/stars/ruyynn/GhostIntel?style=for-the-badge&logo=github&color=yellow&label=Star%20Repo)](https://github.com/ruyynn/GhostIntel)

</div>
