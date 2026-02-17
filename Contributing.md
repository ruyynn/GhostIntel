KONTRIBUSI GHOSTINTEL
<p align="center"> <b>Halo! 👋 Makasih udah mau berkontribusi di GhostIntel!</b> <br> <i>Panduan ini dibuat khusus biar gampang dipahami. Gak usah bingung!</i> </p>


# 📌 PENTING!
GhostIntel ini punya Ruyynn. Kamu boleh bantu ngembangin, tapi jangan dihapus ini:

```text
© 2026 Ruyynn. All Rights Reserved.
```
Dilarang mengedit, mengubah, atau menyebarluaskan tanpa izin.

## ❓ KONTRIBUSI ITU APA?
Kontribusi itu semua bentuk bantuan yang bikin GhostIntel jadi lebih baik. Gak harus jago coding!

✅ Kontribusi Tanpa Coding

| Jenis Bantuan          | Contoh                                 | Cara Berkontribusi              |
| ---------------------- | -------------------------------------- | ------------------------------- |
| Melaporkan error       | “Saat mencari username terjadi error”  | Buat laporan di **Issues**      |
| Memberi saran fitur    | “Menambahkan fitur pengecekan email”   | Tulis ide di **Discussions**    |
| Memperbaiki typo       | “Terdapat kesalahan penulisan di menu” | Edit **README.md**              |
| Menambahkan screenshot | “Screenshot hasil pemindaian”          | Unggah ke folder `screenshots/` |
| Memberi bintang ⭐      | Star repository                        | Klik tombol **Star**            |

✅ Yang Butuh Coding Sedikit

| Jenis Bantuan         | Contoh                                        | Tingkat Kesulitan |
| --------------------- | --------------------------------------------- | ----------------- |
| Menambah provider     | Menambahkan provider baru untuk nomor HP      | ⭐ Mudah           |
| Menambah platform     | Menambahkan platform (Instagram, TikTok, dll) | ⭐ Mudah           |
| Memperbaiki bug kecil | Memperbaiki error format nomor                | ⭐⭐ Menengah       |

## 🚀 CARA KONTRIBUSI LENGKAP
Cara 1: Paling Gampang (TANPA CODING)

## 📝 Lapor Error / Kasih Saran
Buka halaman Issues

Klik tombol "New Issue" (warna hijau)

Tulis judul (contoh: "Error pas cari username")

Tulis penjelasan:

Kejadian apa?

Gimana caranya biar error muncul?

Screenshot (kalo bisa)

Klik "Submit new issue"

Contoh laporan yang bagus:

```text
Judul: Error pas cari username "testing123"

Aku coba cari username "testing123", muncul error:
"ConnectionError: Gagal konek"

Langkah-langkah:
1. Buka program
2. Pilih menu 2 (Username OSINT)
3. Masukkan username "testing123"
4. Langsung error

Screenshot: [tempelin screenshot]
OS: Windows 11
Python: 3.9.7
```
⭐ Kasih Bintang
Klik tombol ⭐ Star di pojok kanan atas halaman ini. Semudah itu!

## Cara 2: Lewat GitHub (Pemula)

### 📝 Perbaiki Typo di README
Buat akun GitHub (kalo belum punya)

Buka file README.md di repository ini

Klik icon pensil (✏️) di pojok kanan atas file

Edit teks yang mau diperbaiki

Scroll ke bawah, isi deskripsi perubahan:

```text
Contoh: "Fix typo di kata 'pencarian'"
```
Klik "Propose changes"

Klik "Create pull request"

Klik "Create pull request" lagi

Selesai! Tinggal tunggu review.

## Cara 3: Kontribusi Coding (Pemula)

## 📥 Langkah 1: Fork Repository
```bash
Buka https://github.com/ruyynn/GhostIntel
```
Klik tombol Fork (di pojok kanan atas)

Ini bakal bikin salinan GhostIntel di akun kamu

## 💻 Langkah 2: Clone ke Komputer
Buka Terminal/CMD/Powershell, ketik:

```bash
git clone https://github.com/ruyynn/GhostIntel.git
cd GhostIntel
```
## 🌿 Langkah 3: Buat Branch Baru
```bash
git checkout -b nama-branch-kamu
```
Contoh:

git checkout -b tambah-provider

git checkout -b fix-typo

git checkout -b tambah-platform

## ✏️ Langkah 4: Edit File
Buka file ghostintel.py pake Notepad, VS Code, atau editor apapun.

Contoh buat pemula:

Mau nambah platform buat username search?

Buka file ghostintel.py

Cari bagian PLATFORMS = [ (sekitar baris 200an)

Tambahin baris baru:

```python
{"name": "Instagram", "url": "https://instagram.com/{}"},
{"name": "TikTok", "url": "https://tiktok.com/@{}"},
{"name": "Telegram", "url": "https://t.me/{}"},
```
Simpan file

## 🧪 Langkah 5: Test Dulu
Jalankan program buat mastiin gak error:

```bash
python ghostintel.py
```
Coba fitur yang baru kamu tambahin.

## 📤 Langkah 6: Upload ke GitHub
```bash
git add .
git commit -m "Tambah platform Instagram, TikTok, Telegram"
git push origin nama-branch-kamu
```
## 🔄 Langkah 7: Bikin Pull Request
Buka GitHub, nanti muncul notifikasi kuning

Klik "Compare & pull request"

Isi judul (contoh: "Tambah 3 platform baru")

Isi deskripsi:

```text
Yang diubah:
- Nambah Instagram
- Nambah TikTok
- Nambah Telegram
```
Cara test:
- Pilih menu Username OSINT
- Masukkan username
- Cek hasilnya
Klik "Create pull request"

## ✅ Langkah 8: Tunggu
Tunggu review dari Ruyynn. Mungkin diminta revisi, mungkin langsung diterima.

## 🎯 IDE KONTRIBUSI BUAT PEMULA

Kontribusi Paling Mudah (Tanpa Coding)

| No | Ide Kontribusi        | Cara Melakukannya                                       |
| -- | --------------------- | ------------------------------------------------------- |
| 1  | Beri bintang ⭐        | Klik tombol **Star** pada repository                    |
| 2  | Melaporkan bug/error  | Buka tab **Issues**, lalu jelaskan error yang ditemukan |
| 3  | Memberi saran fitur   | Buka tab **Discussions** dan tuliskan ide kamu          |
| 4  | Memperbaiki typo      | Edit **README.md** dan perbaiki kesalahan penulisan     |
| 5  | Membagikan repository | Bagikan link repository ke teman atau komunitas         |

Yang Butuh Coding Dikit

| No | Ide Kontribusi             | File yang Diedit | Cara                                                 |
| -- | -------------------------- | ---------------- | ---------------------------------------------------- |
| 1  | Menambah provider HP       | `ghostintel.py`  | Cari `provider_prefixes`, lalu tambahkan prefix baru |
| 2  | Menambah platform username | `ghostintel.py`  | Cari `PLATFORMS = [` lalu tambahkan platform baru    |
| 3  | Memperbaiki pesan error    | `ghostintel.py`  | Cari pesan error dan perjelas informasinya           |
| 4  | Menambahkan komentar kode  | `ghostintel.py`  | Tambahkan penjelasan pada bagian kode yang kompleks  |
| 5  | Menambahkan screenshot     | `screenshots/`   | Ambil screenshot hasil scan dan unggah ke folder     |


## 🧠 Catatan

● Kontribusi tidak harus berupa kode

● Semua bentuk bantuan sangat dihargai 🙏

● `Pastikan perubahan yang dibuat tidak melanggar hukum dan etika OSINT

## ❓ TANYA JAWAB
Q: Aku gak bisa coding, bisa bantu?

A: BISA BANGET! Banyak kok yang gak perlu coding:

Lapor error

Kasih saran fitur

Perbaiki typo

Kasih bintang

Share ke temen


Q: Takut salah, gimana?

A: Santai aja! Namanya juga belajar. Kalo salah nanti diarahin. Yang penting udah mau bantu.

Q: PR itu apa?

A: PR = Pull Request. Itu cara ngirim perubahan kamu ke repository asli. Mirip ngajuin usul.

Q: Fork itu apa?

A: Fork = nyalin repository orang ke akun kamu. Biar kamu bisa edit-edit dulu sebelum dikirim balik.

Q: Berapa lama direview?

A: Biasanya 1-7 hari, tergantung sibuk atau enggaknya.

## 📞 HUBUNGI
Ada pertanyaan? Jangan sungkan hubungi:

<p align="center"> <a href="mailto:ruyynn25@gmail.com"> <img src="https://img.shields.io/badge/Email-ruyynn25%40gmail.com-red?style=for-the-badge&logo=gmail" /> </a> <a href="https://www.instagram.com/ellreynn"> <img src="https://img.shields.io/badge/Instagram-@ellreynn-purple?style=for-the-badge&logo=instagram" /> </a> </p>

## ⭐ MAKASIH!
<p align="center"> <b>Makasih banyak udah mau bantu! 🙏</b> <br> <i>Kontribusi kamu berarti banget buat GhostIntel.</i> </p><p align="center"> <a href="https://github.com/ruyynn/GhostIntel"> <img src="https://img.shields.io/github/stars/ruyynn/GhostIntel?style=for-the-badge&logo=github&color=yellow&label=Star%20Repo" /> </a> <a href="https://github.com/ruyynn?tab=followers"> <img src="https://img.shields.io/github/followers/ruyynn?style=for-the-badge&logo=github&color=blue&label=Follow%20Me" /> </a> </p>
<p align="center"> <b>© 2026 Ruyynn. All Rights Reserved.</b> </p>
