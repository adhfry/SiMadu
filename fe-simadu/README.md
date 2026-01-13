# SiMadu - Sistem Klasifikasi Mutu Tembakau

Sistem klasifikasi mutu tembakau berbasis Fuzzy Logic Mamdani dengan Vue.js dan Flask.

## 🚀 Fitur

- ✅ Upload dan analisis gambar tembakau
- ✅ Klasifikasi otomatis Grade A/B/C
- ✅ Visualisasi lengkap setiap tahapan fuzzy (Fuzzification → Inference → Defuzzification)
- ✅ Responsive design dengan TailwindCSS
- ✅ Glassmorphism UI dengan tema tembakau

## 📋 Prasyarat

- Node.js v20.19.0 atau v22.12.0+
- Python 3.10+
- npm atau yarn

## 🛠️ Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd simadu-project/fe-simadu
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Setup Environment Variables
Buat file `.env` di root folder `fe-simadu`:
```env
VITE_API_BASE_URL=http://localhost:5000
```

Untuk production/hosting, ubah sesuai URL backend Anda:
```env
VITE_API_BASE_URL=https://your-backend-url.com
```

### 4. Jalankan Backend Flask
```bash
cd ../backend
python -m venv venv
venv\Scripts\activate  # Windows
# atau: source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python app.py
```

### 5. Jalankan Frontend Vue
```bash
cd ../fe-simadu
npm run dev
```

Aplikasi akan berjalan di `http://localhost:5173`

## 📁 Struktur Folder

```
fe-simadu/
├── src/
│   ├── views/
│   │   ├── HomePage.vue       # Landing page
│   │   ├── AnalyzePage.vue    # Halaman analisis
│   │   └── AboutPage.vue      # Halaman tentang kelompok
│   ├── services/
│   │   └── api.ts             # API service untuk connect ke Flask
│   ├── router/
│   │   └── index.ts           # Vue Router config
│   ├── App.vue                # Root component
│   ├── main.ts                # Entry point
│   └── main.css               # TailwindCSS import
├── .env                       # Environment variables (jangan commit!)
├── .env.example               # Template env file
└── package.json
```

## 🎨 Halaman

### 1. Home Page (`/`)
Landing page informatif dengan:
- Hero section
- Keunggulan sistem
- Cara kerja sistem (Crisp Input → Fuzzification → Inference → Defuzzification)
- Call-to-action

### 2. Analyze Page (`/analyze`)
Halaman analisis dengan:
- Upload gambar (drag & drop atau click)
- Preview gambar
- Hasil analisis lengkap:
  - **Crisp Input**: Hue & Value dari gambar
  - **Fuzzification**: Derajat keanggotaan semua himpunan fuzzy
  - **Inference**: Aturan fuzzy dan agregasi
  - **Defuzzification**: Hasil akhir Grade A/B/C dengan skor 0-100

### 3. About Page (`/about`)
Informasi tentang:
- Deskripsi proyek
- Teknologi yang digunakan
- Anggota Kelompok 3 (NIM & Kelas)
- Metodologi Fuzzy Mamdani

## 🔧 Teknologi

**Frontend:**
- Vue.js 3 (Composition API)
- TypeScript
- TailwindCSS v4
- Vue Router
- Axios

**Backend:**
- Python Flask
- OpenCV (cv2)
- NumPy

**Algoritma:**
- Fuzzy Logic Mamdani
- Discretized Centroid Defuzzification

## 🌐 Deployment

### Frontend (Vercel/Netlify)
1. Build project:
   ```bash
   npm run build
   ```
2. Deploy folder `dist/`
3. Set environment variable `VITE_API_BASE_URL` ke URL backend production

### Backend (Heroku/Railway/PythonAnywhere)
1. Deploy Flask app
2. Pastikan CORS enabled untuk frontend domain
3. Update `.env` di frontend dengan URL backend

## 📝 Cara Update Anggota Kelompok

Edit file `src/views/AboutPage.vue`:

```typescript
const members = [
  {
    name: 'Nama Lengkap',
    nim: 'NIM Mahasiswa',
    role: 'Ketua Kelompok'  // atau 'Anggota'
  },
  // tambahkan member lain...
]
```

## 🧪 Testing API

Bisa test endpoint backend dengan curl:
```bash
curl -X POST http://localhost:5000/api/classify \
  -F "image=@path/to/tobacco.jpg"
```

## 📖 Referensi

- Modul Defuzzification Hal 19 (Metode Diskrit)
- UAS Artificial Intelligence - Fuzzy Logic Mamdani

## 👥 Kelompok 3

*(Update dengan data kelompok Anda di AboutPage.vue)*

---

**© 2026 SiMadu - Sistem Klasifikasi Mutu Tembakau | Kelompok 3**

