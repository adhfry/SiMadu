# REVISI SISTEM - 9 FUZZY RULES

## Perubahan yang Dilakukan (Revisi Dosen)

### 1. **Backend (Flask - app.py)**

#### A. Inference - 9 Fuzzy Rules Baru
Sebelumnya sistem hanya memiliki 6 rules sederhana. Sekarang diperbarui menjadi **9 rules** yang merupakan kombinasi lengkap dari:
- **Warna (Hue)**: Emas, Kuning, Hijau
- **Kecerahan (Value)**: Cerah, Sedang, Gelap

**9 Rules Baru:**
1. **R1**: IF Emas AND Cerah THEN **Emas Cerah** (Grade A+)
2. **R2**: IF Emas AND Sedang THEN **Emas Sedang** (Grade A)
3. **R3**: IF Emas AND Gelap THEN **Emas Gelap** (Grade B)
4. **R4**: IF Kuning AND Cerah THEN **Kuning Cerah** (Grade B+)
5. **R5**: IF Kuning AND Sedang THEN **Kuning Sedang** (Grade B)
6. **R6**: IF Kuning AND Gelap THEN **Kuning Gelap** (Grade C)
7. **R7**: IF Hijau AND Cerah THEN **Hijau Cerah** (Grade C+)
8. **R8**: IF Hijau AND Sedang THEN **Hijau Sedang** (Grade C)
9. **R9**: IF Hijau AND Gelap THEN **Hijau Gelap** (Grade D)

#### B. Defuzzification - 4 Output Grades
Output membership functions diperbarui menjadi 4 grades (D, C, B, A):
- **Grade D**: Trapesium Kiri [0, 0, 15, 35] - Sangat Rendah
- **Grade C**: Segitiga [25, 45, 65] - Rendah
- **Grade B**: Segitiga [55, 70, 85] - Standar
- **Grade A**: Trapesium Kanan [75, 90, 100, 100] - Tinggi/Sangat Tinggi

#### C. Hasil Klasifikasi Spesifik
Sistem sekarang menampilkan **kategori tembakau yang spesifik**:
- Tembakau Emas Cerah
- Tembakau Emas Sedang
- Tembakau Emas Gelap
- Tembakau Kuning Cerah
- Tembakau Kuning Sedang
- Tembakau Kuning Gelap
- Tembakau Hijau Cerah
- Tembakau Hijau Sedang
- Tembakau Hijau Gelap

Kategori ditentukan berdasarkan **rule yang dominan** (nilai alpha tertinggi).

#### D. Response API
Response API sekarang mencakup:
```json
{
  "data": {
    "inference": {
      "rules": {
        "R1": 0.5,
        "R2": 0.3,
        ...
        "R9": 0.0
      },
      "aggregation": {
        "A": 0.5,
        "B": 0.3,
        "C": 0.1,
        "D": 0.0
      },
      "dominant_rule": "R1"
    },
    "result": {
      "tobacco_type": "Tembakau Emas Cerah",
      "grade": "Grade A+ (Sangat Tinggi)",
      "price": 95000
    }
  }
}
```

### 2. **Frontend (Vue/TypeScript)**

#### A. Komponen Baru: MembershipChart.vue
Komponen baru untuk menampilkan **grafik fungsi keanggotaan** input variables:

1. **Grafik Hue (Warna)**:
   - Menampilkan 3 fungsi keanggotaan: Emas, Kuning, Hijau
   - Garis vertikal merah menunjukkan nilai input
   - Menampilkan nilai μ (derajat keanggotaan) untuk setiap himpunan

2. **Grafik Value (Kecerahan)**:
   - Menampilkan 3 fungsi keanggotaan: Gelap, Sedang, Cerah
   - Garis vertikal merah menunjukkan nilai input
   - Menampilkan nilai μ (derajat keanggotaan) untuk setiap himpunan

#### B. Update DefuzzChart.vue
- Diperbarui untuk menampilkan 4 grades (D, C, B, A)
- Zona dibagi menjadi 5 kategori: D (0-20), C (20-45), B (45-70), A (70-85), A+ (85-100)
- Alpha-cut lines untuk semua 4 grades

#### C. Update AnalyzePage.vue
**Perubahan tampilan:**

1. **Hasil Utama**:
   - Menampilkan kategori tembakau spesifik (contoh: "Tembakau Emas Cerah")
   - Tetap menampilkan grade dan harga

2. **Bagian Fuzzification**:
   - Menampilkan 2 grafik membership functions (Hue dan Value)
   - Setiap grafik menunjukkan kurva lengkap dengan nilai input

3. **Bagian Inference**:
   - 9 rules dikelompokkan berdasarkan kategori warna:
     - 🟡 Kategori Emas (R1, R2, R3)
     - 🟠 Kategori Kuning (R4, R5, R6)
     - 🟢 Kategori Hijau (R7, R8, R9)
   - Setiap rule menampilkan perhitungan MIN dengan nilai μ yang jelas

4. **Bagian Agregasi**:
   - 4 kotak untuk Grade A, B, C, D
   - Menampilkan formula MAX yang digunakan

#### D. Update TypeScript Interfaces
File `services/api.ts` diperbarui untuk mendukung:
- 9 rules (R1-R9)
- 4 aggregation outputs (A, B, C, D)
- Field baru: `dominant_rule` dan `tobacco_type`

### 3. **Manfaat Perubahan**

1. ✅ **Lebih Detail**: 9 kombinasi memberikan klasifikasi yang lebih spesifik
2. ✅ **Lebih Informatif**: Grafik membership functions membantu memahami proses fuzzifikasi
3. ✅ **Traceable**: User bisa melihat seluruh proses dari input hingga output
4. ✅ **Edukatif**: Cocok untuk presentasi tugas akhir/UAS karena menampilkan semua tahapan Fuzzy Mamdani
5. ✅ **Sesuai Revisi Dosen**: Implementasi lengkap 9 rules + visualisasi grafik

### 4. **Cara Testing**

1. **Start Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
   Backend akan berjalan di http://localhost:5055

2. **Start Frontend**:
   ```bash
   cd fe-simadu
   npm install
   npm run dev
   ```
   Frontend akan berjalan di http://localhost:5173

3. **Upload Gambar Tembakau**:
   - Gunakan gambar di root folder: `tembakau emas.jpg`, `tembakau hijau.png`, dll
   - Sistem akan menampilkan:
     - Grafik keanggotaan Hue dan Value
     - 9 rules dengan perhitungan detail
     - Kategori tembakau spesifik (misal: "Tembakau Emas Cerah")
     - Grafik defuzzification dengan 4 grades

### 5. **Contoh Hasil**

**Input**: Upload foto tembakau emas yang cerah
- **Hue**: ~25 → μ_Emas = 1.0, μ_Kuning = 0.0, μ_Hijau = 0.0
- **Value**: ~200 → μ_Cerah = 1.0, μ_Sedang = 0.0, μ_Gelap = 0.0

**Rules**:
- R1 (Emas AND Cerah) = MIN(1.0, 1.0) = **1.0** ⭐ DOMINAN
- R2-R9 = 0.0

**Output**:
- **Kategori**: Tembakau Emas Cerah
- **Grade**: Grade A+ (Sangat Tinggi)
- **Skor**: ~90
- **Harga**: Rp 95.000/kg

---

## Files yang Diubah

### Backend
- ✏️ `backend/app.py`
  - Function `inference()` - 9 rules baru
  - Function `defuzzification()` - 4 output grades
  - Endpoint `/api/classify` - response baru dengan tobacco_type

### Frontend
- ✏️ `fe-simadu/src/components/DefuzzChart.vue` - Support 4 grades
- ➕ `fe-simadu/src/components/MembershipChart.vue` - Komponen baru
- ✏️ `fe-simadu/src/views/AnalyzePage.vue` - Tampilan 9 rules + grafik membership
- ✏️ `fe-simadu/src/services/api.ts` - TypeScript interfaces update

---

**Dibuat oleh**: GitHub Copilot CLI  
**Tanggal**: 16 Januari 2026  
**Versi**: 2.0 (9 Rules Implementation)
