# SiMadu - Sistem Mutu Tembakau Madura

![SiMadu Logo](https://img.shields.io/badge/SiMadu-Fuzzy%20Mamdani-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-blue)

## 📖 Deskripsi Project

**SiMadu (Sistem Mutu Tembakau Madura)** adalah aplikasi web untuk mengklasifikasikan mutu tembakau menggunakan metode **Fuzzy Logic Mamdani** dengan teknik **Discretized Centroid** untuk defuzzifikasi.

### Kelompok 3
- **Mata Kuliah**: Artificial Intelligence
- **Dosen**: Pyepit Rinekso Andriyanto, S.Kom., M.Kom.
- **Tahun**: 2026

---

## 🎯 Fitur Utama

✅ **Klasifikasi Otomatis** - Input Hue & Value, output Grade A/B/C  
✅ **Tracking Lengkap** - Visualisasi setiap tahap fuzzy (Fuzzifikasi → Inference → Defuzzifikasi)  
✅ **Real-time Processing** - Respon cepat dari backend Flask  
✅ **Modern UI** - Glassmorphism design dengan Tailwind CSS  
✅ **Responsive Mobile** - Optimal untuk desktop dan smartphone  

---

## 🧠 Metode Fuzzy Mamdani

### Flow Sistem:
```
Crisp Input → Fuzzifikasi → Fuzzy Input → Inference → Fuzzy Output → Defuzzifikasi → Crisp Output
```

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
- Sampel diskrit: x = 0, 1, 2, ..., 100
- Agregasi dengan operator MAX
- Potongan kurva dengan operator MIN

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

# Install dependencies
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
│   ├── app.py               # Flask API utama
│   ├── requirements.txt     # Dependencies Python
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── assets/          # CSS & static files
│   │   ├── components/      # Vue components
│   │   ├── views/           # Pages (Home, Classify, About)
│   │   ├── router/          # Vue Router config
│   │   ├── App.vue          # Main App component
│   │   └── main.js          # Entry point
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js   # Tailwind configuration
│   └── vite.config.js
│
└── README.md                # This file
```

---

## 🎨 Technology Stack

### Backend
- **Python 3.x** - Programming language
- **Flask 3.0.0** - Web framework
- **Flask-CORS** - Cross-Origin Resource Sharing
- **NumPy 1.26.2** - Numerical computation

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

### 2. Klasifikasi Tembakau
```http
POST /api/classify
Content-Type: application/json

{
  "hue": 25,
  "value": 180
}
```

**Response:**
```json
{
  "success": true,
  "crisp_input": {
    "hue": 25,
    "value": 180
  },
  "fuzzification": {
    "hue_membership": {
      "emas": 0.6667,
      "kuning": 0.25,
      "hijau": 0.0
    },
    "value_membership": {
      "gelap": 0.0,
      "sedang": 0.0,
      "cerah": 0.6
    }
  },
  "inference": {
    "rules_alpha": { ... },
    "aggregation_max": {
      "grade_A": 0.4,
      "grade_B": 0.0,
      "grade_C": 0.0
    }
  },
  "defuzzification": {
    "method": "Discretized Centroid (Mamdani)",
    "samples": 51
  },
  "crisp_output": {
    "value": 73.45,
    "grade": "Grade A (Premium)"
  }
}
```

---

## 📊 Contoh Penggunaan

### Input:
- **Hue**: 25 (Emas dengan sedikit Kuning)
- **Value**: 180 (Cerah)

### Proses:
1. **Fuzzifikasi**: μ_Emas=0.67, μ_Kuning=0.25, μ_Cerah=0.6
2. **Inference**: α1=min(0.67,0.6)=0.6 → Grade A
3. **Agregasi**: MAX(Grade A)=0.6
4. **Defuzzifikasi**: Centroid = 73.45

### Output:
**Grade A (Premium)** dengan nilai **73.45**

---

## 🎓 Referensi

1. **Modul Defuzzification Hal 19** - Metode Discretized Centroid
2. **UAS-Pyepit Rinekso Andriyanto** - Syarat tahapan fuzzy yang jelas

---

## 👥 Kelompok 3

*Data anggota kelompok akan ditambahkan setelah project selesai*

---

## 📝 License

Educational Project - Kelompok 3 AI Class 2026

---

## 📞 Contact & Support

Untuk pertanyaan atau dukungan, hubungi anggota Kelompok 3.

---

**Dibuat dengan ❤️ oleh Kelompok 3 - Sistem Mutu Tembakau Madura**
