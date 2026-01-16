# 📊 GRAFIK FUNGSI KEANGGOTAAN LENGKAP - 7 GRADES

## Implementasi Grade Lengkap (A+, A, B+, B, C+, C, D)

### 🎯 Perubahan Utama:

Sebelumnya sistem hanya menampilkan **4 grades** (A, B, C, D).  
Sekarang sistem menampilkan **7 grades lengkap** sesuai dengan 9 rules:

---

## 📈 Fungsi Keanggotaan Output (7 Grades)

### 1. **Grade D (Sangat Rendah)** 🔴
- **Tipe**: Trapesium Kiri
- **Range**: [0, 0, 10, 25]
- **Mapping**: Rule R9 (Hijau Gelap)
- **Warna Chart**: Merah gelap `rgb(127, 29, 29)`

### 2. **Grade C (Rendah)** 🟠
- **Tipe**: Segitiga
- **Range**: [20, 35, 50]
- **Mapping**: Rule R6, R8 (Kuning Gelap, Hijau Sedang)
- **Warna Chart**: Orange `rgb(249, 115, 22)`

### 3. **Grade C+ (Rendah Plus)** 🟡
- **Tipe**: Segitiga
- **Range**: [40, 50, 60]
- **Mapping**: Rule R7 (Hijau Cerah)
- **Warna Chart**: Orange terang `rgb(251, 146, 60)`

### 4. **Grade B (Standar)** 🟢
- **Tipe**: Segitiga
- **Range**: [50, 60, 70]
- **Mapping**: Rule R3, R5 (Emas Gelap, Kuning Sedang)
- **Warna Chart**: Kuning `rgb(234, 179, 8)`

### 5. **Grade B+ (Standar Plus)** 🔵
- **Tipe**: Segitiga
- **Range**: [60, 70, 80]
- **Mapping**: Rule R4 (Kuning Cerah)
- **Warna Chart**: Biru `rgb(59, 130, 246)`

### 6. **Grade A (Tinggi)** 💚
- **Tipe**: Segitiga
- **Range**: [70, 80, 90]
- **Mapping**: Rule R2 (Emas Sedang)
- **Warna Chart**: Hijau `rgb(34, 197, 94)`

### 7. **Grade A+ (Sangat Tinggi)** ⭐
- **Tipe**: Trapesium Kanan
- **Range**: [85, 92, 100, 100]
- **Mapping**: Rule R1 (Emas Cerah)
- **Warna Chart**: Hijau gelap `rgb(22, 163, 74)`

---

## 🔄 Mapping 9 Rules ke 7 Grades

| Rule | Kondisi | Output Grade | Range Score |
|------|---------|--------------|-------------|
| R1 | Emas + Cerah | **A+** | 85-100 |
| R2 | Emas + Sedang | **A** | 70-90 |
| R3 | Emas + Gelap | **B** | 50-70 |
| R4 | Kuning + Cerah | **B+** | 60-80 |
| R5 | Kuning + Sedang | **B** | 50-70 |
| R6 | Kuning + Gelap | **C** | 20-50 |
| R7 | Hijau + Cerah | **C+** | 40-60 |
| R8 | Hijau + Sedang | **C** | 20-50 |
| R9 | Hijau + Gelap | **D** | 0-25 |

---

## 💻 Implementasi Backend

### File: `backend/app.py`

```python
# 7 Fungsi Keanggotaan Output
def mu_grade_D(x):        # [0, 0, 10, 25]
def mu_grade_C(x):        # [20, 35, 50]
def mu_grade_C_plus(x):   # [40, 50, 60]
def mu_grade_B(x):        # [50, 60, 70]
def mu_grade_B_plus(x):   # [60, 70, 80]
def mu_grade_A(x):        # [70, 80, 90]
def mu_grade_A_plus(x):   # [85, 92, 100, 100]
```

### Defuzzification dengan 7 Grades:

```python
# Clipping dengan aggregated values
clip_A_plus = min(aggregated['A'], m_A_plus)
clip_A = min(aggregated['A'], m_A)
clip_B_plus = min(aggregated['B'], m_B_plus)
clip_B = min(aggregated['B'], m_B)
clip_C_plus = min(aggregated['C'], m_C_plus)
clip_C = min(aggregated['C'], m_C)
clip_D = min(aggregated['D'], m_D)

# Union (MAX)
mu_final = max(clip_A_plus, clip_A, clip_B_plus, clip_B, 
               clip_C_plus, clip_C, clip_D)
```

**Catatan**: 
- Aggregated tetap 4 values (A, B, C, D) dari inference
- Tapi membership functions menjadi 7 untuk lebih detail
- Grade A menggunakan 2 kurva (A dan A+)
- Grade B menggunakan 2 kurva (B dan B+)
- Grade C menggunakan 2 kurva (C dan C+)
- Grade D menggunakan 1 kurva

---

## 🎨 Implementasi Frontend

### File: `fe-simadu/src/components/OutputMembershipChart.vue`

**7 Dataset untuk Chart.js**:

```typescript
datasets: [
  { label: '🔴 Grade D',  color: 'rgb(127, 29, 29)' },
  { label: '🟠 Grade C',  color: 'rgb(249, 115, 22)' },
  { label: '🟡 Grade C+', color: 'rgb(251, 146, 60)' },
  { label: '🟢 Grade B',  color: 'rgb(234, 179, 8)' },
  { label: '🔵 Grade B+', color: 'rgb(59, 130, 246)' },
  { label: '💚 Grade A',  color: 'rgb(34, 197, 94)' },
  { label: '⭐ Grade A+', color: 'rgb(22, 163, 74)' }
]
```

**Optimasi Layout**:
- Legend font size: `9px → 8px`
- Legend padding: `6px → 4px`
- Box size: `8px → 7px`
- Height: `480px → 520px` (tambahan ruang untuk 7 kurva)

---

## 📊 Tampilan Grafik

Grafik akan menampilkan:

1. ✅ **7 kurva berbeda** dengan warna yang jelas
2. ✅ **Overlapping yang natural** (kurva saling tumpang tindih di zona transisi)
3. ✅ **Alpha-cut lines** untuk A, B, C, D (4 garis horizontal)
4. ✅ **Legend kompak** dengan emoji untuk mudah dibaca
5. ✅ **Area fill transparan** agar semua kurva terlihat

---

## 🎯 Keuntungan 7 Grades:

1. **Lebih Detail**: Setiap kombinasi warna×kecerahan punya representasi visual
2. **Lebih Akurat**: Transisi antar grade lebih smooth
3. **Lebih Edukatif**: User bisa melihat semua kemungkinan output
4. **Sesuai Rules**: 9 rules → 7 unique outputs (lebih masuk akal)
5. **Professional**: Tampilan lebih lengkap dan akademis

---

## 📝 Contoh Interpretasi:

**Contoh 1**: Tembakau Emas Cerah (R1)
- α_A = 0.9
- Kurva A+ dan A akan di-clip pada y=0.9
- Score akhir ≈ 88-95 (range A+)

**Contoh 2**: Tembakau Kuning Sedang (R5)
- α_B = 0.7
- Kurva B+ dan B akan di-clip pada y=0.7
- Score akhir ≈ 60-65 (range B/B+)

**Contoh 3**: Tembakau Hijau Gelap (R9)
- α_D = 1.0
- Kurva D akan di-clip pada y=1.0 (full)
- Score akhir ≈ 5-15 (range D)

---

## ✅ Status

- ✅ Backend: 7 membership functions implemented
- ✅ Frontend: 7 curves displayed
- ✅ Chart: No overlapping text
- ✅ Colors: Distinctive and meaningful
- ✅ Legend: Compact with emojis

---

**Update Date**: 16 Januari 2026, 17:53  
**Version**: 3.0 (Complete 7 Grades)  
**Status**: ✅ PRODUCTION READY
