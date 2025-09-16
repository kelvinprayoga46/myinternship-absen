# 🤖 MyInternship Attendance Bot

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

> **Automation bot untuk absensi harian di myinternship.id**

Bot otomatis yang dapat melakukan absensi harian secara terjadwal di platform MyInternship.id. Dibuat untuk memudahkan mahasiswa dalam mengelola absensi magang mereka.

## ⚠️ DISCLAIMER

**PENTING:** Tool ini dibuat untuk tujuan **edukasi dan otomatisasi pribadi**.

- ✅ Gunakan dengan **bijak** dan sesuai ketentuan kampus
- ❌ **Tidak bertanggung jawab** atas pelanggaran aturan akademik
- 🔒 **Jaga kerahasiaan** credential dan data pribadi
- 📖 Pastikan memahami **konsekuensi penggunaan**

## ✨ Features

- 🔐 **Auto Login** - Login otomatis dengan credential tersimpan
- 🛡️ **CSRF Protection** - Handling CSRF token untuk keamanan
- 🍪 **Session Management** - Pengelolaan session yang proper
- 📊 **Smart Token Extraction** - Extract JWT token secara otomatis
- ✅ **Attendance Submission** - Submit absensi dengan validasi tanda tangan
- 🔄 **Error Handling** - Comprehensive error handling dan retry logic
- 📝 **Detailed Logging** - Log proses untuk debugging
- 🔒 **Secure Configuration** - Credential disimpan di environment variables

## 🛠️ Tech Stack

- **Python 3.7+** - Bahasa pemrograman utama
- **Requests** - HTTP client untuk web scraping
- **BeautifulSoup4** - HTML parsing dan manipulation
- **python-dotenv** - Environment variables management
- **Re (Regex)** - Pattern matching untuk token extraction

## 📋 Prerequisites

- Python 3.7 atau lebih tinggi
- Git (untuk clone repository)
- Akun aktif di myinternship.id
- Tanda tangan digital (PNG format)

## 🚀 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/myinternship-absen.git
cd myinternship-absen
```

### 2. Install Dependencies

```bash
# Menggunakan pip
pip install -r requirements.txt

# Atau menggunakan pip3
pip3 install -r requirements.txt

# Untuk virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
# Copy template environment
cp .env.example .env

# Edit file .env dengan text editor favorit
nano .env  # Linux/Mac
# atau
notepad .env  # Windows
```

### 4. Konfigurasi .env File

Edit file `.env` dengan data pribadi Anda:

```bash
# MyInternship.id Credentials
MYINTERNSHIP_NIM=john@students.polibatam.ac.id                  # Ganti dengan NIM Anda
MYINTERNSHIP_PASS=adminheker123                  # Ganti dengan password Anda

# MyInternship IDs - SESUAIKAN DENGAN DATA ANDA
MYINTERNSHIP_ID_INTERNSHIP=OTI0OA==id_encode_base64_here        # ID encoded dari URL
MYINTERNSHIP_ID_INTERNSHIP_NUMERIC=id_decode_base64_here     # ID numeric untuk form

# Digital Signature Base64
MYINTERNSHIP_SIGNATURE_BASE64=data:image/png;base64,iVBORw0KGgoAAAANS...
```

## 🔍 Cara Mendapatkan Configuration Data

### A. Mendapatkan ID Internship

1. **Login** ke myinternship.id
2. **Buka halaman** attendance/absensi
3. **Perhatikan URL** di address bar:
   ```
   https://myinternship.id/index.php?page=attendance_internship&id_internship=OTI0OA==
   ```
4. **Copy nilai** `id_internship=XXXXX` → ini adalah `ID_INTERNSHIP`
5. **Untuk ID numeric**, Convert/Decode base64 to Plaintext `id_internship`

### B. Convert Tanda Tangan ke Base64

1. **Download tanda tangan** dari MyInternship.id:
   - Masuk ke profile/settings
   - Download signature dalam format PNG
2. **Convert ke Base64**:

   - Gunakan online converter: [base64-image.de](https://www.base64-image.de/)
   - Upload file PNG tanda tangan
   - Copy hasil dalam format: `data:image/png;base64,XXXXX`

3. **Paste ke .env**:
   ```bash
   MYINTERNSHIP_SIGNATURE_BASE64=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
   ```

## ▶️ Usage

### Basic Usage

```bash
python main.py
```

### Dengan Virtual Environment

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

python main.py
```

### Expected Output

```
Step 1: Mengambil halaman login...
CSRF Token (Login): abc123def456...
Cookies: {'PHPSESSID': 'xyz789...'}

Step 2: Melakukan login...
Login berhasil!

Step 3: Mengambil halaman index...
CSRF Token (Index): def456ghi789...

Step 4: Mengakses halaman attendance...
JWT Token ditemukan: eyJ0eXAiOiJKV1QiLCJhbGciOi...

Step 5: Mengakses halaman add attendance...
Step 6: Submit data attendance...
Attendance berhasil disubmit!

=== Automasi selesai dengan sukses! ===
Absensi berhasil!
```

## 📅 Automation & Scheduling

### Menggunakan Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Tambahkan line ini untuk running setiap hari jam 8 pagi
0 8 * * * cd /path/to/myinternship-bot && /usr/bin/python3 main.py >> attendance.log 2>&1

# Atau dengan virtual environment
0 8 * * * cd /path/to/myinternship-bot && /path/to/venv/bin/python main.py >> attendance.log 2>&1
```

### Menggunakan Task Scheduler (Windows)

1. Buka **Task Scheduler**
2. **Create Basic Task**
3. **Name**: MyInternship Auto Attendance
4. **Trigger**: Daily pada jam yang diinginkan
5. **Action**: Start a program
6. **Program**: `python.exe`
7. **Arguments**: `main.py`
8. **Start in**: Path ke folder project

### Menggunakan GitHub Actions (Cloud)

Buat file `.github/workflows/attendance.yml`:

```yaml
name: Auto Attendance
on:
  schedule:
    - cron: "0 1 * * *" # Jam 8 pagi WIB (UTC+7)
  workflow_dispatch: # Manual trigger

jobs:
  attendance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run attendance bot
        env:
          MYINTERNSHIP_NIM: ${{ secrets.MYINTERNSHIP_NIM }}
          MYINTERNSHIP_PASS: ${{ secrets.MYINTERNSHIP_PASS }}
          MYINTERNSHIP_ID_INTERNSHIP: ${{ secrets.MYINTERNSHIP_ID_INTERNSHIP }}
          MYINTERNSHIP_ID_INTERNSHIP_NUMERIC: ${{ secrets.MYINTERNSHIP_ID_INTERNSHIP_NUMERIC }}
          MYINTERNSHIP_SIGNATURE_BASE64: ${{ secrets.MYINTERNSHIP_SIGNATURE_BASE64 }}
        run: python main.py
```

## 🔧 Configuration Options

### Default Attendance Settings

Bot menggunakan konfigurasi default berikut (dapat dimodifikasi di `main.py`):

```python
default_data = {
    'attendance_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),  # Kemarin
    'attendance_type': 'Present',        # Status hadir
    'check_in': '00:00',                # Jam masuk
    'check_out': '08:00',               # Jam keluar
    'description': '<p>ABSEN HARIAN</p>', # Deskripsi kegiatan
}
```

### Custom Attendance Data

Anda dapat mengustomisasi data absensi:

```python
# Di main.py, modifikasi bagian ini:
custom_attendance = {
    'check_in': '08:30',
    'check_out': '17:00',
    'description': '<p>Kegiatan: Mengembangkan fitur web dashboard</p>'
}

success = automation.run_automation(nim, password, custom_attendance)
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Login Failed

```
Error: Login gagal!
```

**Solusi:**

- ✅ Pastikan NIM dan password benar di `.env`
- ✅ Coba login manual di browser
- ✅ Periksa koneksi internet
- ✅ Pastikan website MyInternship.id tidak maintenance

#### 2. CSRF Token Error

```
Error: Tidak bisa mengambil CSRF token
```

**Solusi:**

- 🔄 Jalankan ulang bot (token bisa expired)
- 🌐 Periksa koneksi internet
- 🔍 Cek apakah struktur website berubah

#### 3. JWT Token Not Found

```
Error: Tidak bisa menemukan JWT token dari button Add Attendance
```

**Solusi:**

- 🆔 Pastikan `ID_INTERNSHIP` benar
- 📅 Cek apakah sudah absen hari ini
- 🔍 Periksa halaman attendance manual

#### 4. Environment Variables Error

```
Error: NoneType object has no attribute...
```

**Solusi:**

- 📄 Pastikan file `.env` ada dan terisi
- ✏️ Periksa format dan nama variable di `.env`
- 🔄 Restart terminal setelah edit `.env`

#### 5. Signature/Validation Error

```
Error submit attendance. Status code: 400
```

**Solusi:**

- 🖋️ Pastikan signature base64 lengkap dan benar
- 📏 Cek format: `data:image/png;base64,XXXXX`
- 🔄 Download ulang signature dan convert lagi

### Debug Mode

Untuk debugging lebih detail, tambahkan print statements:

```python
# Di main.py, tambahkan:
import logging

logging.basicConfig(level=logging.DEBUG)

# Atau tambahkan print statements untuk debug
print(f"Debug - Response: {response.text[:1000]}")
```

### Log Files

Untuk menyimpan log aktivitas:

```bash
# Jalankan dengan output ke file
python main.py > attendance.log 2>&1

# Atau append ke existing log
python main.py >> attendance.log 2>&1
```

## 📁 Project Structure

```
myinternship-absen/
├── 📄 main.py                 # Main application file
├── 📄 .env                    # Environment variables (DO NOT COMMIT!)
├── 📄 .env.example           # Environment template
├── 📄 .gitignore             # Git ignore rules
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md              # This documentation
├── 📄 LICENSE                # MIT License (optional)
├── 📁 logs/                  # Log files (optional)
│   └── attendance.log
└── 📁 docs/                  # Additional documentation (optional)
    ├── setup-guide.md
    └── troubleshooting.md
```

## 🛡️ Security Best Practices

### Environment Variables

- ❌ **JANGAN** commit file `.env` ke Git
- ✅ **GUNAKAN** `.env.example` sebagai template
- 🔒 **SIMPAN** credential dengan aman
- 🔄 **GANTI** password secara berkala

### Code Security

- ✅ Regular update dependencies
- 🔍 Review code sebelum menjalankan
- 🚫 Tidak share credential di chat/email
- 🔐 Gunakan virtual environment

### Deployment Security

- 🌐 Gunakan HTTPS untuk semua koneksi
- 🔑 Set proper file permissions (600 for .env)
- 📝 Monitor log files untuk aktivitas mencurigakan
- 🚨 Set up alerts untuk failed attempts

## 🧪 Testing

### Manual Testing

```bash
python -c "
from main import MyInternshipAutomation
import os
from dotenv import load_dotenv

load_dotenv()
bot = MyInternshipAutomation()
bot.step1_get_login_page()
result = bot.step2_login(os.getenv('MYINTERNSHIP_NIM'), os.getenv('MYINTERNSHIP_PASS'))
print(f'Login result: {result}')
"
```

### Dry Run Mode

Untuk testing tanpa submit attendance (modifikasi di `main.py`):

```python
def step6_submit_attendance(self, referer_url, attendance_data, dry_run=False):
    if dry_run:
        print("DRY RUN: Attendance data would be submitted:")
        print(default_data)
        return True
    # ... rest of the code
```

## 🤝 Contributing

Kontribusi sangat welcome! Berikut cara berkontribusi:

### Fork & Clone

```bash
# Fork repository di GitHub, lalu:
git clone https://github.com/kelvinprayoga46/myinternship-absen.git
cd myinternship-absen
```

### Development Setup

```bash
# Buat virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies dengan dev requirements
pip install -r requirements.txt
pip install black flake8 pytest  # untuk development
```

### Code Style

```bash
# Format code dengan black
black main.py

# Check linting dengan flake8
flake8 main.py
```

### Submit Pull Request

1. Buat branch baru: `git checkout -b feature/improvement-name`
2. Commit changes: `git commit -m "Add: new feature description"`
3. Push branch: `git push origin feature/improvement-name`
4. Buat Pull Request di GitHub

### Version 2.0 (Planned)

- [ ] 🔔 Multi-platform notifications (Telegram, Discord, Email)
- [ ] 📊 Attendance statistics dashboard
- [ ] 🔄 Auto-retry dengan exponential backoff
- [ ] 📱 Web-based GUI interface
- [ ] 🐳 Docker containerization
- [ ] 🔐 Enhanced security dengan encryption

### Version 2.1 (Future)

- [ ] ⚡ Multi-account support
- [ ] 🤖 AI-powered attendance descriptions
- [ ] 📈 Analytics dan reporting
- [ ] 🔗 API integration untuk third-party apps
- [ ] 📱 Mobile app companion

## 📝 Changelog

### v1.0.0 (Current)

- ✅ Initial release
- ✅ Basic attendance automation
- ✅ CSRF token handling
- ✅ Environment variables support
- ✅ Comprehensive error handling
- ✅ Documentation

## 📄 License

```
MIT License

Copyright (c) 2024 MyInternship Bot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Support & Contact

### Issues & Bugs

- 🐛 [Report Bug](https://github.com/kelvinprayoga46/myinternship/issues/new?template=bug_report.md)
- 💡 [Feature Request](https://github.com/kelvinprayoga46/myinternship/issues/new?template=feature_request.md)
- 📖 [Documentation Issue](https://github.com/kelvinprayoga46/myinternship/issues/new?template=documentation.md)

### Community

- 💬 [Discussions](https://wa.me/082386997269)
- 📧 [Email](kelvinprayoga46@gmail.com

### FAQ

**Q: Apakah bot ini aman digunakan?**
A: Ya, bot menggunakan HTTPS dan menyimpan credential di environment variables. Namun gunakan dengan bijak sesuai aturan kampus.

**Q: Berapa sering bot perlu dijalankan?**
A: Sekali per hari, biasanya dijadwalkan pagi/siang/malam hari untuk absen hari sebelumnya.

**Q: Bagaimana jika website MyInternship.id berubah?**
A: Bot mungkin perlu update. Silakan buat issue di GitHub atau submit pull request.

**Q: Bisa untuk multiple account?**
A: Saat ini hanya support satu account. Multi-account akan ditambahkan di versi mendatang.

---

<div align="center">

**⭐ Jika project ini membantu, jangan lupa berikan star!**

Made with ❤️ by [Kelvin](https://github.com/kelvinprayoga46)

</div>
