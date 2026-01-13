# SiMadu - Sistem Mutu Tembakau Madura

![SiMadu Logo](https://img.shields.io/badge/SiMadu-Fuzzy%20Mamdani-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)

## 📖 Deskripsi Project

**SiMadu (Sistem Mutu Tembakau Madura)** adalah aplikasi web untuk mengklasifikasikan mutu tembakau menggunakan metode **Fuzzy Logic Mamdani** dengan teknik **Discretized Centroid** untuk defuzzifikasi.

### 🎯 Fitur Utama v2.0

✅ **Upload Gambar Tembakau** - Input foto daun tembakau (JPG/PNG)  
✅ **Ekstraksi Otomatis Hue & Value** - Menggunakan OpenCV HSV Color Space  
✅ **Klasifikasi Real-time** - Dari gambar langsung ke Grade A/B/C  
✅ **Tracking Lengkap** - Visualisasi setiap tahap fuzzy  
✅ **Modern UI** - Glassmorphism design dengan Tailwind CSS  
✅ **Responsive Mobile** - Optimal untuk desktop dan smartphone  

### Kelompok 3
- **Mata Kuliah**: Artificial Intelligence
- **Dosen**: Pyepit Rinekso Andriyanto, S.Kom., M.Kom.
- **Tahun**: 2026

---

## 🧠 Metode Fuzzy Mamdani

### Flow Sistem:
```
Image Upload → HSV Extraction → Hue/Value → Fuzzification → Inference → Defuzzification → Grade
```

### 0. **Ekstraksi Gambar (Image Processing)**
- **Input**: Foto tembakau (JPG/PNG)
- **Metode**: HSV Color Space Analysis dengan OpenCV
- **Output**: 
  - Hue (scaled 0-80): Rata-rata warna dominan
  - Value (0-255): Rata-rata kecerahan

### 1. **Variabel Input**
| Variabel | Range | Himpunan Fuzzy |
|----------|-------|----------------|
| **Warna (Hue)** | 0-80 | Emas [0,0,20,35], Kuning [20,40,55], Hijau [45,60,80,80] |
| **Kecerahan (Value)** | 0-255 | Gelap [0,0,60,100], Sedang [80,130,180], Cerah [150,200,255,255] |

### 2. **Variabel Output**
| Grade | Range | Fungsi Keanggotaan |
|-------|-------|-------------------|
| **Grade C** | 0-50 | Trapesium Kiri [0,0,20,50] |
| **Grade B** | 30-70 | Segitiga [30,50,70] |
| **Grade A** | 50-100 | Trapesium Kanan [50,80,100,100] |

### 3. **Aturan Fuzzy (IF-THEN)**
1. IF Emas AND Cerah THEN Grade A
2. IF Emas AND Sedang THEN Grade B
3. IF Kuning AND Cerah THEN Grade B
4. IF Kuning AND Sedang THEN Grade B
5. IF Hijau THEN Grade C
6. IF Gelap THEN Grade C

### 4. **Defuzzifikasi**
Menggunakan **Discretized Centroid** (sesuai PDF Hal 19):
```
Nilai Akhir = Σ(xi × μi) / Σμi
```

---

## 🚀 Cara Menjalankan Project

### Prerequisites
- Python 3.x
- Node.js & npm
- Git

### 1️⃣ Setup Backend (Flask)

```bash
cd backend

# Aktivasi virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Jalankan server
python app.py
```

Server akan berjalan di: `http://localhost:5000`

### 2️⃣ Setup Frontend (Vue.js)

```bash
cd frontend

# Install dependencies (jika belum)
npm install

# Jalankan development server
npm run dev
```

Frontend akan berjalan di: `http://localhost:5173`

---

## 📂 Struktur Project

```
simadu-project/
├── backend/
│   ├── venv/                 # Python virtual environment
│   ├── app.py               # Flask API utama + Image Processing
│   ├── requirements.txt     # Dependencies (Flask, OpenCV, NumPy)
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── assets/          # CSS & static files
│   │   ├── views/           
│   │   │   ├── HomeView.vue        # Landing page
│   │   │   ├── ClassifyView.vue    # Upload & Klasifikasi
│   │   │   └── AboutView.vue       # Info kelompok
│   │   ├── router/          # Vue Router config
│   │   ├── App.vue          # Main App component
│   │   └── main.ts          # Entry point
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── test_input.json          # Sample test data
└── README.md                # This file
```

---

## 🎨 Technology Stack

### Backend
- **Python 3.x** - Programming language
- **Flask 3.0.0** - Web framework
- **Flask-CORS** - Cross-Origin Resource Sharing
- **NumPy 1.26.2** - Numerical computation
- **OpenCV 4.8.1** - Image processing & HSV extraction
- **Pillow 10.1.0** - Image manipulation

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Official routing library
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Vite** - Build tool

---

## 📡 API Endpoints

### 1. Health Check
```http
GET /api/health
```
**Response:**
```json
{
  "status": "Backend Flask berjalan dengan baik!"
}
```

### 2. Klasifikasi Tembakau (Image Upload)
```http
POST /api/classify
Content-Type: multipart/form-data

Form Data:
- image: <file> (JPG/PNG)
```

**Response:**
```json
{
  "success": true,
  "image_analysis": {
    "extracted_hue": 25.43,
    "extracted_value": 182.56,
    "method": "HSV Color Space Analysis"
  },
  "crisp_input": {
    "hue": 25.43,
    "value": 182.56
  },
  "fuzzification": {
    "hue_membership": {
      "emas": 0.6381,
      "kuning": 0.2715,
      "hijau": 0.0
    },
    "value_membership": {
      "gelap": 0.0,
      "sedang": 0.0,
      "cerah": 0.6512
    }
  },
  "inference": {
    "rules_alpha": {...},
    "aggregation_max": {
      "grade_A": 0.6381,
      "grade_B": 0.2715,
      "grade_C": 0.0
    }
  },
  "defuzzification": {
    "method": "Discretized Centroid (Mamdani)",
    "samples": 69
  },
  "crisp_output": {
    "value": 74.23,
    "grade": "Grade A (Premium)"
  }
}
```

---

## 📊 Cara Penggunaan

### Step 1: Buka Aplikasi
Akses `http://localhost:5173` di browser

### Step 2: Upload Foto Tembakau
1. Klik menu "Klasifikasi"
2. Pilih file gambar tembakau (JPG/PNG)
3. Preview gambar akan muncul

### Step 3: Analisis & Klasifikasi
1. Klik tombol "Analisis & Klasifikasi"
2. Sistem akan:
   - Ekstrak Hue & Value dari gambar
   - Proses Fuzzifikasi
   - Evaluasi aturan Inference
   - Hitung Defuzzifikasi
3. Hasil Grade A/B/C ditampilkan

### Step 4: Review Detail
Lihat tracking lengkap:
- Nilai Hue & Value terdeteksi
- Derajat keanggotaan fuzzy
- α-predikat setiap aturan
- Metode defuzzifikasi

---

## 🎓 Referensi

1. **Modul Defuzzification Hal 19** - Metode Discretized Centroid
2. **UAS-Pyepit Rinekso Andriyanto** - Syarat tahapan fuzzy yang jelas
3. **OpenCV HSV Color Space** - Ekstraksi warna dari gambar

---

## 👥 Kelompok 3

*Data anggota kelompok akan ditambahkan di halaman About*

---

## 📝 License

Educational Project - Kelompok 3 AI Class 2026

---

## 📞 Contact & Support

Untuk pertanyaan atau dukungan, hubungi anggota Kelompok 3.

---

**Dibuat dengan ❤️ oleh Kelompok 3 - Sistem Mutu Tembakau Madura**
