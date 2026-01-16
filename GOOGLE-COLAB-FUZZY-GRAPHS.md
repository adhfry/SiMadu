# 📊 Google Colab - Grafik Fungsi Keanggotaan Fuzzy (untuk Dokumentasi Jurnal)

## Kode Python untuk Membuat Grafik Keanggotaan Sistem Mutu Tembakau Madura

Paste kode berikut di Google Colab untuk membuat visualisasi grafik fungsi keanggotaan yang bersih dan profesional untuk dokumentasi jurnal.

---

## 1️⃣ Install & Import Libraries

```python
# Install libraries (jika belum terinstall)
!pip install matplotlib numpy

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
```

---

## 2️⃣ Grafik Fungsi Keanggotaan INPUT - HUE (Warna)

```python
# Fungsi Keanggotaan HUE (0-180)
def mu_emas(x):
    """Trapesium Kiri [0, 0, 15, 35]"""
    if x <= 15:
        return 1.0
    elif 15 < x < 35:
        return (35 - x) / 20
    return 0.0

def mu_kuning(x):
    """Segitiga [25, 45, 60]"""
    if 25 < x <= 45:
        return (x - 25) / 20
    elif 45 < x < 60:
        return (60 - x) / 15
    return 0.0

def mu_hijau(x):
    """Trapesium Kanan [50, 65, 80, 80]"""
    if x < 50:
        return 0.0
    elif 50 <= x < 65:
        return (x - 50) / 15
    return 1.0

# Generate data
hue_values = np.linspace(0, 180, 500)
emas_values = [mu_emas(x) for x in hue_values]
kuning_values = [mu_kuning(x) for x in hue_values]
hijau_values = [mu_hijau(x) for x in hue_values]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(hue_values, emas_values, 'gold', linewidth=3, label='Emas')
plt.plot(hue_values, kuning_values, 'orange', linewidth=3, label='Kuning')
plt.plot(hue_values, hijau_values, 'green', linewidth=3, label='Hijau')

# Styling untuk jurnal
plt.title('Fungsi Keanggotaan Hue (Warna)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Hue (0-180)', fontsize=14, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=14, fontweight='bold')
plt.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
plt.grid(True, alpha=0.3, linestyle='--')
plt.ylim(-0.05, 1.1)
plt.xlim(0, 180)

# Tambahkan tick marks yang lebih rapi
plt.xticks(np.arange(0, 181, 20), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)

plt.tight_layout()
plt.savefig('grafik_hue.png', dpi=300, bbox_inches='tight')  # Simpan dengan resolusi tinggi
plt.show()

print("✅ Grafik Hue berhasil dibuat dan disimpan sebagai 'grafik_hue.png'")
```

---

## 3️⃣ Grafik Fungsi Keanggotaan INPUT - VALUE (Kecerahan)

```python
# Fungsi Keanggotaan VALUE (0-255)
def mu_gelap(x):
    """Trapesium Kiri [0, 0, 80, 140]"""
    if x <= 80:
        return 1.0
    elif 80 < x < 140:
        return (140 - x) / 60
    return 0.0

def mu_sedang(x):
    """Segitiga [120, 160, 200]"""
    if 120 < x <= 160:
        return (x - 120) / 40
    elif 160 < x < 200:
        return (200 - x) / 40
    return 0.0

def mu_cerah(x):
    """Trapesium Kanan [180, 220, 255, 255]"""
    if x < 180:
        return 0.0
    elif 180 <= x < 220:
        return (x - 180) / 40
    return 1.0

# Generate data
value_values = np.linspace(0, 255, 500)
gelap_values = [mu_gelap(x) for x in value_values]
sedang_values = [mu_sedang(x) for x in value_values]
cerah_values = [mu_cerah(x) for x in value_values]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(value_values, gelap_values, color='#1e3a8a', linewidth=3, label='Gelap')
plt.plot(value_values, sedang_values, color='#3b82f6', linewidth=3, label='Sedang')
plt.plot(value_values, cerah_values, color='#93c5fd', linewidth=3, label='Cerah')

# Styling untuk jurnal
plt.title('Fungsi Keanggotaan Value (Kecerahan)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Value (0-255)', fontsize=14, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=14, fontweight='bold')
plt.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
plt.grid(True, alpha=0.3, linestyle='--')
plt.ylim(-0.05, 1.1)
plt.xlim(0, 255)

# Tambahkan tick marks yang lebih rapi
plt.xticks(np.arange(0, 256, 30), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)

plt.tight_layout()
plt.savefig('grafik_value.png', dpi=300, bbox_inches='tight')  # Simpan dengan resolusi tinggi
plt.show()

print("✅ Grafik Value berhasil dibuat dan disimpan sebagai 'grafik_value.png'")
```

---

## 4️⃣ Grafik Fungsi Keanggotaan OUTPUT - 9 GRADES

```python
# Fungsi Keanggotaan OUTPUT (Grade 0-100) - 9 GRADES
def mu_C_minus(x):
    """Trapesium Kiri [0, 0, 5, 15]"""
    if x <= 5:
        return 1.0
    elif 5 < x < 15:
        return (15 - x) / 10
    return 0.0

def mu_C(x):
    """Segitiga [10, 20, 30]"""
    if 10 < x <= 20:
        return (x - 10) / 10
    elif 20 < x < 30:
        return (30 - x) / 10
    return 0.0

def mu_C_plus(x):
    """Segitiga [25, 35, 45]"""
    if 25 < x <= 35:
        return (x - 25) / 10
    elif 35 < x < 45:
        return (45 - x) / 10
    return 0.0

def mu_B_minus(x):
    """Segitiga [40, 48, 56]"""
    if 40 < x <= 48:
        return (x - 40) / 8
    elif 48 < x < 56:
        return (56 - x) / 8
    return 0.0

def mu_B(x):
    """Segitiga [52, 60, 68]"""
    if 52 < x <= 60:
        return (x - 52) / 8
    elif 60 < x < 68:
        return (68 - x) / 8
    return 0.0

def mu_B_plus(x):
    """Segitiga [64, 72, 80]"""
    if 64 < x <= 72:
        return (x - 64) / 8
    elif 72 < x < 80:
        return (80 - x) / 8
    return 0.0

def mu_A_minus(x):
    """Segitiga [75, 82, 89]"""
    if 75 < x <= 82:
        return (x - 75) / 7
    elif 82 < x < 89:
        return (89 - x) / 7
    return 0.0

def mu_A(x):
    """Segitiga [85, 91, 97]"""
    if 85 < x <= 91:
        return (x - 85) / 6
    elif 91 < x < 97:
        return (97 - x) / 6
    return 0.0

def mu_A_plus(x):
    """Trapesium Kanan [92, 96, 100, 100]"""
    if x < 92:
        return 0.0
    elif 92 <= x < 96:
        return (x - 92) / 4
    return 1.0

# Generate data
grade_values = np.linspace(0, 100, 500)
C_minus_values = [mu_C_minus(x) for x in grade_values]
C_values = [mu_C(x) for x in grade_values]
C_plus_values = [mu_C_plus(x) for x in grade_values]
B_minus_values = [mu_B_minus(x) for x in grade_values]
B_values = [mu_B(x) for x in grade_values]
B_plus_values = [mu_B_plus(x) for x in grade_values]
A_minus_values = [mu_A_minus(x) for x in grade_values]
A_values = [mu_A(x) for x in grade_values]
A_plus_values = [mu_A_plus(x) for x in grade_values]

# Plot dengan warna profesional untuk jurnal
plt.figure(figsize=(14, 7))

plt.plot(grade_values, C_minus_values, color='#7F1D1D', linewidth=2.5, label='C-', alpha=0.9)
plt.plot(grade_values, C_values, color='#DC2626', linewidth=2.5, label='C', alpha=0.9)
plt.plot(grade_values, C_plus_values, color='#F97316', linewidth=2.5, label='C+', alpha=0.9)
plt.plot(grade_values, B_minus_values, color='#FBBF24', linewidth=2.5, label='B-', alpha=0.9)
plt.plot(grade_values, B_values, color='#EAB308', linewidth=2.5, label='B', alpha=0.9)
plt.plot(grade_values, B_plus_values, color='#3B82F6', linewidth=2.5, label='B+', alpha=0.9)
plt.plot(grade_values, A_minus_values, color='#0EA5E9', linewidth=2.5, label='A-', alpha=0.9)
plt.plot(grade_values, A_values, color='#22C55E', linewidth=2.5, label='A', alpha=0.9)
plt.plot(grade_values, A_plus_values, color='#16A34A', linewidth=2.5, label='A+', alpha=0.9)

# Styling untuk jurnal
plt.title('Fungsi Keanggotaan Output (Grade Mutu)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Mutu (0-100)', fontsize=14, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=14, fontweight='bold')
plt.legend(loc='upper left', fontsize=11, ncol=3, frameon=True, shadow=True)
plt.grid(True, alpha=0.3, linestyle='--')
plt.ylim(-0.05, 1.1)
plt.xlim(0, 100)

# Tambahkan tick marks yang lebih rapi
plt.xticks(np.arange(0, 101, 10), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)

plt.tight_layout()
plt.savefig('grafik_output_9grades.png', dpi=300, bbox_inches='tight')  # Simpan dengan resolusi tinggi
plt.show()

print("✅ Grafik Output (9 Grades) berhasil dibuat dan disimpan sebagai 'grafik_output_9grades.png'")
print("\n📋 Spesifikasi Fungsi Keanggotaan:")
print("   - C-  : Trapesium Kiri [0, 0, 5, 15]")
print("   - C   : Segitiga [10, 20, 30]")
print("   - C+  : Segitiga [25, 35, 45]")
print("   - B-  : Segitiga [40, 48, 56]")
print("   - B   : Segitiga [52, 60, 68]")
print("   - B+  : Segitiga [64, 72, 80]")
print("   - A-  : Segitiga [75, 82, 89]")
print("   - A   : Segitiga [85, 91, 97]")
print("   - A+  : Trapesium Kanan [92, 96, 100, 100]")
```

---

## 5️⃣ Grafik Defuzzification (Contoh dengan Area Arsiran)

```python
# Contoh Defuzzification untuk dokumentasi
def create_defuzzification_example():
    """
    Membuat contoh grafik defuzzification untuk dokumentasi jurnal
    """
    
    # Contoh nilai agregasi (ubah sesuai kebutuhan)
    alpha_A_plus = 0.6
    alpha_A = 0.4
    alpha_A_minus = 0.3
    alpha_B_plus = 0.0
    alpha_B = 0.0
    alpha_B_minus = 0.0
    alpha_C_plus = 0.0
    alpha_C = 0.0
    alpha_C_minus = 0.0
    
    # Array untuk menyimpan kurva final
    x_values = np.arange(0, 101, 1)
    y_final = []
    numerator = 0
    denominator = 0
    
    for x in x_values:
        # Clipping: MIN(alpha, membership_function)
        clip_A_plus = min(alpha_A_plus, mu_A_plus(x))
        clip_A = min(alpha_A, mu_A(x))
        clip_A_minus = min(alpha_A_minus, mu_A_minus(x))
        clip_B_plus = min(alpha_B_plus, mu_B_plus(x))
        clip_B = min(alpha_B, mu_B(x))
        clip_B_minus = min(alpha_B_minus, mu_B_minus(x))
        clip_C_plus = min(alpha_C_plus, mu_C_plus(x))
        clip_C = min(alpha_C, mu_C(x))
        clip_C_minus = min(alpha_C_minus, mu_C_minus(x))
        
        # Union: MAX dari semua clipped curves
        mu_final = max(clip_A_plus, clip_A, clip_A_minus, 
                       clip_B_plus, clip_B, clip_B_minus,
                       clip_C_plus, clip_C, clip_C_minus)
        
        y_final.append(mu_final)
        
        # Akumulasi untuk centroid
        numerator += x * mu_final
        denominator += mu_final
    
    # Hitung centroid
    centroid = numerator / denominator if denominator > 0 else 0
    
    # Plot
    plt.figure(figsize=(12, 7))
    
    # Area arsiran (filled area)
    plt.fill_between(x_values, 0, y_final, alpha=0.3, color='mediumpurple', label='Area Agregasi (Union)')
    
    # Kurva hasil union
    plt.plot(x_values, y_final, color='purple', linewidth=3, label='Kurva Agregasi')
    
    # Centroid point dan line
    centroid_y = y_final[int(centroid)]
    plt.plot(centroid, centroid_y, 'ro', markersize=12, label=f'Centroid (Crisp Output)', zorder=5)
    plt.axvline(x=centroid, color='red', linestyle='--', linewidth=2.5, alpha=0.7)
    
    # Styling untuk jurnal
    plt.title('Proses Defuzzification - Metode Centroid', fontsize=16, fontweight='bold')
    plt.xlabel('Nilai Mutu (0-100)', fontsize=14, fontweight='bold')
    plt.ylabel('Derajat Keanggotaan (μ)', fontsize=14, fontweight='bold')
    plt.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.ylim(-0.05, 1.1)
    plt.xlim(0, 100)
    
    # Tambahkan tick marks yang lebih rapi
    plt.xticks(np.arange(0, 101, 10), fontsize=12)
    plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)
    
    # Tambahkan teks centroid
    plt.text(centroid, -0.15, f'x* = {centroid:.2f}', 
             ha='center', fontsize=12, fontweight='bold', color='red')
    
    plt.tight_layout()
    plt.savefig('grafik_defuzzification.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Grafik Defuzzification berhasil dibuat dan disimpan sebagai 'grafik_defuzzification.png'")
    print(f"\n📊 Hasil Defuzzification:")
    print(f"   - Crisp Output (Centroid): {centroid:.2f}")
    print(f"   - Numerator: {numerator:.2f}")
    print(f"   - Denominator: {denominator:.2f}")

# Jalankan fungsi
create_defuzzification_example()
```

---

## 6️⃣ Generate Semua Grafik Sekaligus

```python
# Script untuk generate semua grafik sekaligus
print("="*60)
print("📊 GENERATING ALL GRAPHS FOR JOURNAL DOCUMENTATION")
print("="*60)

# 1. Grafik Hue
hue_values = np.linspace(0, 180, 500)
emas_values = [mu_emas(x) for x in hue_values]
kuning_values = [mu_kuning(x) for x in hue_values]
hijau_values = [mu_hijau(x) for x in hue_values]

plt.figure(figsize=(10, 6))
plt.plot(hue_values, emas_values, 'gold', linewidth=3, label='Emas')
plt.plot(hue_values, kuning_values, 'orange', linewidth=3, label='Kuning')
plt.plot(hue_values, hijau_values, 'green', linewidth=3, label='Hijau')
plt.title('Fungsi Keanggotaan Hue (Warna)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Hue (0-180)', fontsize=14, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=14, fontweight='bold')
plt.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
plt.grid(True, alpha=0.3, linestyle='--')
plt.ylim(-0.05, 1.1)
plt.xlim(0, 180)
plt.xticks(np.arange(0, 181, 20), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)
plt.tight_layout()
plt.savefig('grafik_hue.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ 1/4 Grafik Hue selesai")

# 2. Grafik Value
value_values = np.linspace(0, 255, 500)
gelap_values = [mu_gelap(x) for x in value_values]
sedang_values = [mu_sedang(x) for x in value_values]
cerah_values = [mu_cerah(x) for x in value_values]

plt.figure(figsize=(10, 6))
plt.plot(value_values, gelap_values, color='#1e3a8a', linewidth=3, label='Gelap')
plt.plot(value_values, sedang_values, color='#3b82f6', linewidth=3, label='Sedang')
plt.plot(value_values, cerah_values, color='#93c5fd', linewidth=3, label='Cerah')
plt.title('Fungsi Keanggotaan Value (Kecerahan)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Value (0-255)', fontsize=14, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=14, fontweight='bold')
plt.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
plt.grid(True, alpha=0.3, linestyle='--')
plt.ylim(-0.05, 1.1)
plt.xlim(0, 255)
plt.xticks(np.arange(0, 256, 30), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)
plt.tight_layout()
plt.savefig('grafik_value.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ 2/4 Grafik Value selesai")

# 3. Grafik Output (9 Grades)
grade_values = np.linspace(0, 100, 500)
C_minus_values = [mu_C_minus(x) for x in grade_values]
C_values = [mu_C(x) for x in grade_values]
C_plus_values = [mu_C_plus(x) for x in grade_values]
B_minus_values = [mu_B_minus(x) for x in grade_values]
B_values = [mu_B(x) for x in grade_values]
B_plus_values = [mu_B_plus(x) for x in grade_values]
A_minus_values = [mu_A_minus(x) for x in grade_values]
A_values = [mu_A(x) for x in grade_values]
A_plus_values = [mu_A_plus(x) for x in grade_values]

plt.figure(figsize=(14, 7))
plt.plot(grade_values, C_minus_values, color='#7F1D1D', linewidth=2.5, label='C-', alpha=0.9)
plt.plot(grade_values, C_values, color='#DC2626', linewidth=2.5, label='C', alpha=0.9)
plt.plot(grade_values, C_plus_values, color='#F97316', linewidth=2.5, label='C+', alpha=0.9)
plt.plot(grade_values, B_minus_values, color='#FBBF24', linewidth=2.5, label='B-', alpha=0.9)
plt.plot(grade_values, B_values, color='#EAB308', linewidth=2.5, label='B', alpha=0.9)
plt.plot(grade_values, B_plus_values, color='#3B82F6', linewidth=2.5, label='B+', alpha=0.9)
plt.plot(grade_values, A_minus_values, color='#0EA5E9', linewidth=2.5, label='A-', alpha=0.9)
plt.plot(grade_values, A_values, color='#22C55E', linewidth=2.5, label='A', alpha=0.9)
plt.plot(grade_values, A_plus_values, color='#16A34A', linewidth=2.5, label='A+', alpha=0.9)
plt.title('Fungsi Keanggotaan Output (Grade Mutu)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Mutu (0-100)', fontsize=14, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=14, fontweight='bold')
plt.legend(loc='upper left', fontsize=11, ncol=3, frameon=True, shadow=True)
plt.grid(True, alpha=0.3, linestyle='--')
plt.ylim(-0.05, 1.1)
plt.xlim(0, 100)
plt.xticks(np.arange(0, 101, 10), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.2), fontsize=12)
plt.tight_layout()
plt.savefig('grafik_output_9grades.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ 3/4 Grafik Output (9 Grades) selesai")

# 4. Grafik Defuzzification
create_defuzzification_example()
print("✅ 4/4 Grafik Defuzzification selesai")

print("\n" + "="*60)
print("🎉 SEMUA GRAFIK BERHASIL DIBUAT!")
print("="*60)
print("📁 File yang dihasilkan:")
print("   1. grafik_hue.png (resolusi 300 dpi)")
print("   2. grafik_value.png (resolusi 300 dpi)")
print("   3. grafik_output_9grades.png (resolusi 300 dpi)")
print("   4. grafik_defuzzification.png (resolusi 300 dpi)")
print("\n💡 File dapat diunduh dari Google Colab dan digunakan untuk jurnal")
print("="*60)
```

---

## 📝 Catatan:

1. **Semua grafik disimpan** dengan resolusi **300 DPI** (standar publikasi jurnal)
2. **Tidak ada nilai input** yang ditampilkan, hanya grafik fungsi keanggotaan murni
3. **Styling profesional** untuk dokumentasi akademik
4. File akan tersimpan di Google Colab dan dapat diunduh

---

## 🎯 Cara Penggunaan:

1. Buka **Google Colab**
2. Copy paste **Section 1** (Install Libraries)
3. Copy paste **Section 6** (Generate All Graphs) untuk membuat semua grafik sekaligus
4. **Download** semua file PNG yang dihasilkan
5. Gunakan untuk **dokumentasi jurnal**

---

**Dibuat untuk**: Dokumentasi Jurnal - Sistem Mutu Tembakau Madura  
**Metode**: Fuzzy Mamdani (9 Rules → 9 Grades)  
**Output**: 4 Grafik Profesional (300 DPI)  
**Date**: 16 Januari 2026

---

## 2️⃣ Grafik Fungsi Keanggotaan INPUT - HUE (Warna)

```python
# Fungsi Keanggotaan HUE (0-180)
def mu_emas(x):
    """Trapesium Kiri [0, 0, 15, 35]"""
    if x <= 15:
        return 1.0
    elif 15 < x < 35:
        return (35 - x) / 20
    return 0.0

def mu_kuning(x):
    """Segitiga [25, 45, 60]"""
    if 25 < x <= 45:
        return (x - 25) / 20
    elif 45 < x < 60:
        return (60 - x) / 15
    return 0.0

def mu_hijau(x):
    """Trapesium Kanan [50, 65, 80, 80]"""
    if x < 50:
        return 0.0
    elif 50 <= x < 65:
        return (x - 50) / 15
    return 1.0

# Generate data
hue_values = np.linspace(0, 180, 500)
emas_values = [mu_emas(x) for x in hue_values]
kuning_values = [mu_kuning(x) for x in hue_values]
hijau_values = [mu_hijau(x) for x in hue_values]

# Plot
plt.figure(figsize=(12, 6))
plt.plot(hue_values, emas_values, 'gold', linewidth=2.5, label='🟡 Emas (Premium)')
plt.plot(hue_values, kuning_values, 'orange', linewidth=2.5, label='🟠 Kuning (Sedang)')
plt.plot(hue_values, hijau_values, 'green', linewidth=2.5, label='🟢 Hijau (Rendah)')

# Contoh input
input_hue = 30  # Ganti dengan nilai input Anda
plt.axvline(x=input_hue, color='red', linestyle='--', linewidth=2, label=f'Input: {input_hue}')
plt.plot(input_hue, mu_emas(input_hue), 'ro', markersize=8)
plt.plot(input_hue, mu_kuning(input_hue), 'ro', markersize=8)
plt.plot(input_hue, mu_hijau(input_hue), 'ro', markersize=8)

# Styling
plt.title('Fungsi Keanggotaan HUE (Warna)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Hue (0-180)', fontsize=12, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=12, fontweight='bold')
plt.legend(loc='upper right', fontsize=11)
plt.grid(True, alpha=0.3)
plt.ylim(-0.05, 1.1)
plt.xlim(0, 180)

# Tambahkan nilai keanggotaan
plt.text(5, 0.95, f'μ_Emas({input_hue}) = {mu_emas(input_hue):.3f}', 
         bbox=dict(boxstyle='round', facecolor='gold', alpha=0.5), fontsize=10)
plt.text(5, 0.85, f'μ_Kuning({input_hue}) = {mu_kuning(input_hue):.3f}', 
         bbox=dict(boxstyle='round', facecolor='orange', alpha=0.5), fontsize=10)
plt.text(5, 0.75, f'μ_Hijau({input_hue}) = {mu_hijau(input_hue):.3f}', 
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5), fontsize=10)

plt.tight_layout()
plt.show()

print(f"📊 Nilai Keanggotaan untuk Hue = {input_hue}:")
print(f"   - μ Emas   = {mu_emas(input_hue):.4f}")
print(f"   - μ Kuning = {mu_kuning(input_hue):.4f}")
print(f"   - μ Hijau  = {mu_hijau(input_hue):.4f}")
```

---

## 3️⃣ Grafik Fungsi Keanggotaan INPUT - VALUE (Kecerahan)

```python
# Fungsi Keanggotaan VALUE (0-255)
def mu_gelap(x):
    """Trapesium Kiri [0, 0, 80, 140]"""
    if x <= 80:
        return 1.0
    elif 80 < x < 140:
        return (140 - x) / 60
    return 0.0

def mu_sedang(x):
    """Segitiga [120, 160, 200]"""
    if 120 < x <= 160:
        return (x - 120) / 40
    elif 160 < x < 200:
        return (200 - x) / 40
    return 0.0

def mu_cerah(x):
    """Trapesium Kanan [180, 220, 255, 255]"""
    if x < 180:
        return 0.0
    elif 180 <= x < 220:
        return (x - 180) / 40
    return 1.0

# Generate data
value_values = np.linspace(0, 255, 500)
gelap_values = [mu_gelap(x) for x in value_values]
sedang_values = [mu_sedang(x) for x in value_values]
cerah_values = [mu_cerah(x) for x in value_values]

# Plot
plt.figure(figsize=(12, 6))
plt.plot(value_values, gelap_values, 'darkblue', linewidth=2.5, label='🌑 Gelap')
plt.plot(value_values, sedang_values, 'steelblue', linewidth=2.5, label='🌤️ Sedang')
plt.plot(value_values, cerah_values, 'lightskyblue', linewidth=2.5, label='☀️ Cerah')

# Contoh input
input_value = 200  # Ganti dengan nilai input Anda
plt.axvline(x=input_value, color='red', linestyle='--', linewidth=2, label=f'Input: {input_value}')
plt.plot(input_value, mu_gelap(input_value), 'ro', markersize=8)
plt.plot(input_value, mu_sedang(input_value), 'ro', markersize=8)
plt.plot(input_value, mu_cerah(input_value), 'ro', markersize=8)

# Styling
plt.title('Fungsi Keanggotaan VALUE (Kecerahan)', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Value (0-255)', fontsize=12, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=12, fontweight='bold')
plt.legend(loc='upper right', fontsize=11)
plt.grid(True, alpha=0.3)
plt.ylim(-0.05, 1.1)
plt.xlim(0, 255)

# Tambahkan nilai keanggotaan
plt.text(10, 0.95, f'μ_Gelap({input_value}) = {mu_gelap(input_value):.3f}', 
         bbox=dict(boxstyle='round', facecolor='darkblue', alpha=0.5), fontsize=10, color='white')
plt.text(10, 0.85, f'μ_Sedang({input_value}) = {mu_sedang(input_value):.3f}', 
         bbox=dict(boxstyle='round', facecolor='steelblue', alpha=0.5), fontsize=10, color='white')
plt.text(10, 0.75, f'μ_Cerah({input_value}) = {mu_cerah(input_value):.3f}', 
         bbox=dict(boxstyle='round', facecolor='lightskyblue', alpha=0.5), fontsize=10)

plt.tight_layout()
plt.show()

print(f"📊 Nilai Keanggotaan untuk Value = {input_value}:")
print(f"   - μ Gelap  = {mu_gelap(input_value):.4f}")
print(f"   - μ Sedang = {mu_sedang(input_value):.4f}")
print(f"   - μ Cerah  = {mu_cerah(input_value):.4f}")
```

---

## 4️⃣ Grafik Fungsi Keanggotaan OUTPUT - 9 GRADES

```python
# Fungsi Keanggotaan OUTPUT (Grade 0-100) - 9 GRADES
def mu_C_minus(x):
    """Trapesium Kiri [0, 0, 5, 15]"""
    if x <= 5:
        return 1.0
    elif 5 < x < 15:
        return (15 - x) / 10
    return 0.0

def mu_C(x):
    """Segitiga [10, 20, 30]"""
    if 10 < x <= 20:
        return (x - 10) / 10
    elif 20 < x < 30:
        return (30 - x) / 10
    return 0.0

def mu_C_plus(x):
    """Segitiga [25, 35, 45]"""
    if 25 < x <= 35:
        return (x - 25) / 10
    elif 35 < x < 45:
        return (45 - x) / 10
    return 0.0

def mu_B_minus(x):
    """Segitiga [40, 48, 56]"""
    if 40 < x <= 48:
        return (x - 40) / 8
    elif 48 < x < 56:
        return (56 - x) / 8
    return 0.0

def mu_B(x):
    """Segitiga [52, 60, 68]"""
    if 52 < x <= 60:
        return (x - 52) / 8
    elif 60 < x < 68:
        return (68 - x) / 8
    return 0.0

def mu_B_plus(x):
    """Segitiga [64, 72, 80]"""
    if 64 < x <= 72:
        return (x - 64) / 8
    elif 72 < x < 80:
        return (80 - x) / 8
    return 0.0

def mu_A_minus(x):
    """Segitiga [75, 82, 89]"""
    if 75 < x <= 82:
        return (x - 75) / 7
    elif 82 < x < 89:
        return (89 - x) / 7
    return 0.0

def mu_A(x):
    """Segitiga [85, 91, 97]"""
    if 85 < x <= 91:
        return (x - 85) / 6
    elif 91 < x < 97:
        return (97 - x) / 6
    return 0.0

def mu_A_plus(x):
    """Trapesium Kanan [92, 96, 100, 100]"""
    if x < 92:
        return 0.0
    elif 92 <= x < 96:
        return (x - 92) / 4
    return 1.0

# Generate data
grade_values = np.linspace(0, 100, 500)
C_minus_values = [mu_C_minus(x) for x in grade_values]
C_values = [mu_C(x) for x in grade_values]
C_plus_values = [mu_C_plus(x) for x in grade_values]
B_minus_values = [mu_B_minus(x) for x in grade_values]
B_values = [mu_B(x) for x in grade_values]
B_plus_values = [mu_B_plus(x) for x in grade_values]
A_minus_values = [mu_A_minus(x) for x in grade_values]
A_values = [mu_A(x) for x in grade_values]
A_plus_values = [mu_A_plus(x) for x in grade_values]

# Plot dengan warna yang berbeda untuk setiap grade
plt.figure(figsize=(14, 7))

plt.plot(grade_values, C_minus_values, color='#7F1D1D', linewidth=2, label='🔴 C- (Rendah)', alpha=0.8)
plt.plot(grade_values, C_values, color='#DC2626', linewidth=2, label='🟠 C (Cukup)', alpha=0.8)
plt.plot(grade_values, C_plus_values, color='#F97316', linewidth=2, label='🟡 C+ (Cukup Plus)', alpha=0.8)
plt.plot(grade_values, B_minus_values, color='#FBBF24', linewidth=2, label='🟢 B- (Baik Minus)', alpha=0.8)
plt.plot(grade_values, B_values, color='#EAB308', linewidth=2, label='🟦 B (Baik)', alpha=0.8)
plt.plot(grade_values, B_plus_values, color='#3B82F6', linewidth=2, label='🔵 B+ (Baik Plus)', alpha=0.8)
plt.plot(grade_values, A_minus_values, color='#0EA5E9', linewidth=2, label='💙 A- (Tinggi Minus)', alpha=0.8)
plt.plot(grade_values, A_values, color='#22C55E', linewidth=2, label='💚 A (Tinggi)', alpha=0.8)
plt.plot(grade_values, A_plus_values, color='#16A34A', linewidth=2, label='⭐ A+ (Sangat Tinggi)', alpha=0.8)

# Contoh alpha-cut (hasil agregasi dari inference)
alpha_A_plus = 0.8  # Ganti dengan nilai agregasi Anda
alpha_A = 0.5
alpha_A_minus = 0.3
alpha_B_plus = 0.2
alpha_B = 0.1
alpha_B_minus = 0.0
alpha_C_plus = 0.0
alpha_C = 0.0
alpha_C_minus = 0.0

# Tampilkan alpha-cut lines
if alpha_A_plus > 0:
    plt.axhline(y=alpha_A_plus, color='#16A34A', linestyle='--', linewidth=1.5, alpha=0.6, label=f'α A+ = {alpha_A_plus:.2f}')
if alpha_A > 0:
    plt.axhline(y=alpha_A, color='#22C55E', linestyle='--', linewidth=1.5, alpha=0.6, label=f'α A = {alpha_A:.2f}')
if alpha_A_minus > 0:
    plt.axhline(y=alpha_A_minus, color='#0EA5E9', linestyle='--', linewidth=1.5, alpha=0.6, label=f'α A- = {alpha_A_minus:.2f}')

# Styling
plt.title('Fungsi Keanggotaan OUTPUT (9 Grades: A+, A, A-, B+, B, B-, C+, C, C-)', 
          fontsize=16, fontweight='bold')
plt.xlabel('Nilai Mutu (0-100)', fontsize=12, fontweight='bold')
plt.ylabel('Derajat Keanggotaan (μ)', fontsize=12, fontweight='bold')
plt.legend(loc='upper left', fontsize=9, ncol=2)
plt.grid(True, alpha=0.3)
plt.ylim(-0.05, 1.1)
plt.xlim(0, 100)

plt.tight_layout()
plt.show()

print("📊 Fungsi Keanggotaan Output (9 Grades):")
print("   - C- : [0, 0, 5, 15] (Trapesium Kiri)")
print("   - C  : [10, 20, 30] (Segitiga)")
print("   - C+ : [25, 35, 45] (Segitiga)")
print("   - B- : [40, 48, 56] (Segitiga)")
print("   - B  : [52, 60, 68] (Segitiga)")
print("   - B+ : [64, 72, 80] (Segitiga)")
print("   - A- : [75, 82, 89] (Segitiga)")
print("   - A  : [85, 91, 97] (Segitiga)")
print("   - A+ : [92, 96, 100, 100] (Trapesium Kanan)")
```

---

## 5️⃣ Simulasi Defuzzification dengan Area Arsiran

```python
# Simulasi Defuzzification (Centroid Method)
def defuzzification_simulation(alpha_values):
    """
    alpha_values = {
        'A_plus': 0.8,
        'A': 0.5,
        'A_minus': 0.3,
        'B_plus': 0.2,
        'B': 0.1,
        'B_minus': 0.0,
        'C_plus': 0.0,
        'C': 0.0,
        'C_minus': 0.0
    }
    """
    numerator = 0
    denominator = 0
    
    # Array untuk menyimpan kurva final (hasil clipping & union)
    x_values = np.arange(0, 101, 1)
    y_final = []
    
    for x in x_values:
        # Clipping: MIN(alpha, membership_function)
        clip_A_plus = min(alpha_values['A_plus'], mu_A_plus(x))
        clip_A = min(alpha_values['A'], mu_A(x))
        clip_A_minus = min(alpha_values['A_minus'], mu_A_minus(x))
        clip_B_plus = min(alpha_values['B_plus'], mu_B_plus(x))
        clip_B = min(alpha_values['B'], mu_B(x))
        clip_B_minus = min(alpha_values['B_minus'], mu_B_minus(x))
        clip_C_plus = min(alpha_values['C_plus'], mu_C_plus(x))
        clip_C = min(alpha_values['C'], mu_C(x))
        clip_C_minus = min(alpha_values['C_minus'], mu_C_minus(x))
        
        # Union: MAX dari semua clipped curves
        mu_final = max(clip_A_plus, clip_A, clip_A_minus, 
                       clip_B_plus, clip_B, clip_B_minus,
                       clip_C_plus, clip_C, clip_C_minus)
        
        y_final.append(mu_final)
        
        # Akumulasi untuk centroid
        numerator += x * mu_final
        denominator += mu_final
    
    # Hitung centroid
    centroid = numerator / denominator if denominator > 0 else 0
    
    # Plot
    plt.figure(figsize=(14, 7))
    
    # Area arsiran (filled area)
    plt.fill_between(x_values, 0, y_final, alpha=0.3, color='purple', label='Area Terarsir (Union)')
    
    # Kurva hasil clipping
    plt.plot(x_values, y_final, 'purple', linewidth=2.5, label='Kurva Final (Union)')
    
    # Centroid point
    centroid_y = y_final[int(centroid)]
    plt.plot(centroid, centroid_y, 'ro', markersize=12, label=f'Centroid: {centroid:.2f}', zorder=5)
    plt.axvline(x=centroid, color='red', linestyle='--', linewidth=2, alpha=0.7)
    
    # Styling
    plt.title('Defuzzification - Metode Centroid (COA)', fontsize=16, fontweight='bold')
    plt.xlabel('Nilai Mutu (0-100)', fontsize=12, fontweight='bold')
    plt.ylabel('Derajat Keanggotaan (μ)', fontsize=12, fontweight='bold')
    plt.legend(loc='upper right', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.ylim(-0.05, 1.1)
    plt.xlim(0, 100)
    
    # Tambahkan informasi
    plt.text(5, 0.95, f'Numerator = {numerator:.2f}', 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5), fontsize=10)
    plt.text(5, 0.85, f'Denominator = {denominator:.2f}', 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5), fontsize=10)
    plt.text(5, 0.75, f'Crisp Output = {centroid:.2f}', 
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7), fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    return centroid, numerator, denominator

# Contoh penggunaan
alpha_aggregation = {
    'A_plus': 0.8,
    'A': 0.5,
    'A_minus': 0.3,
    'B_plus': 0.2,
    'B': 0.1,
    'B_minus': 0.0,
    'C_plus': 0.0,
    'C': 0.0,
    'C_minus': 0.0
}

crisp_output, num, den = defuzzification_simulation(alpha_aggregation)

print(f"\n📊 Hasil Defuzzification:")
print(f"   - Numerator   : {num:.4f}")
print(f"   - Denominator : {den:.4f}")
print(f"   - Crisp Output: {crisp_output:.2f}")

# Tentukan grade berdasarkan score
if crisp_output >= 94:
    grade = "Grade A+ (Sangat Tinggi)"
elif crisp_output >= 88:
    grade = "Grade A (Tinggi)"
elif crisp_output >= 78:
    grade = "Grade A- (Tinggi Minus)"
elif crisp_output >= 68:
    grade = "Grade B+ (Baik Plus)"
elif crisp_output >= 56:
    grade = "Grade B (Baik)"
elif crisp_output >= 44:
    grade = "Grade B- (Baik Minus)"
elif crisp_output >= 32:
    grade = "Grade C+ (Cukup Plus)"
elif crisp_output >= 18:
    grade = "Grade C (Cukup)"
else:
    grade = "Grade C- (Rendah)"

print(f"   - Grade Final : {grade}")
```

---

## 6️⃣ Contoh Lengkap - End to End Simulation

```python
# ===== SIMULASI LENGKAP FUZZY MAMDANI =====

# INPUT
input_hue = 25    # Nilai Hue (0-180)
input_value = 200  # Nilai Value (0-255)

print("="*60)
print("🌿 SISTEM MUTU TEMBAKAU MADURA - FUZZY MAMDANI")
print("="*60)

# 1. FUZZIFICATION
print("\n1️⃣ FUZZIFICATION:")
print(f"   Input Hue   = {input_hue}")
print(f"   Input Value = {input_value}")

mu_emas_val = mu_emas(input_hue)
mu_kuning_val = mu_kuning(input_hue)
mu_hijau_val = mu_hijau(input_hue)
mu_gelap_val = mu_gelap(input_value)
mu_sedang_val = mu_sedang(input_value)
mu_cerah_val = mu_cerah(input_value)

print(f"\n   Keanggotaan Hue:")
print(f"      μ Emas   = {mu_emas_val:.4f}")
print(f"      μ Kuning = {mu_kuning_val:.4f}")
print(f"      μ Hijau  = {mu_hijau_val:.4f}")

print(f"\n   Keanggotaan Value:")
print(f"      μ Gelap  = {mu_gelap_val:.4f}")
print(f"      μ Sedang = {mu_sedang_val:.4f}")
print(f"      μ Cerah  = {mu_cerah_val:.4f}")

# 2. INFERENCE (9 RULES)
print("\n2️⃣ INFERENCE (9 RULES - MIN Implication):")

rules = {
    'R1': min(mu_emas_val, mu_cerah_val),      # Emas Cerah → A+
    'R2': min(mu_emas_val, mu_sedang_val),     # Emas Sedang → A
    'R3': min(mu_emas_val, mu_gelap_val),      # Emas Gelap → A-
    'R4': min(mu_kuning_val, mu_cerah_val),    # Kuning Cerah → B+
    'R5': min(mu_kuning_val, mu_sedang_val),   # Kuning Sedang → B
    'R6': min(mu_kuning_val, mu_gelap_val),    # Kuning Gelap → B-
    'R7': min(mu_hijau_val, mu_cerah_val),     # Hijau Cerah → C+
    'R8': min(mu_hijau_val, mu_sedang_val),    # Hijau Sedang → C
    'R9': min(mu_hijau_val, mu_gelap_val)      # Hijau Gelap → C-
}

for rule_name, alpha in rules.items():
    print(f"   {rule_name} = {alpha:.4f}")

# 3. AGGREGATION
print("\n3️⃣ AGGREGATION (Setiap rule → 1 grade):")

aggregation = {
    'A_plus': rules['R1'],
    'A': rules['R2'],
    'A_minus': rules['R3'],
    'B_plus': rules['R4'],
    'B': rules['R5'],
    'B_minus': rules['R6'],
    'C_plus': rules['R7'],
    'C': rules['R8'],
    'C_minus': rules['R9']
}

for grade_name, alpha in aggregation.items():
    print(f"   α {grade_name:8s} = {alpha:.4f}")

# 4. DEFUZZIFICATION
print("\n4️⃣ DEFUZZIFICATION (Centroid Method):")
crisp_output, num, den = defuzzification_simulation(aggregation)

# 5. GRADE DETERMINATION
if crisp_output >= 94:
    final_grade = "Grade A+ (Sangat Tinggi)"
    harga = 95000
elif crisp_output >= 88:
    final_grade = "Grade A (Tinggi)"
    harga = 85000
elif crisp_output >= 78:
    final_grade = "Grade A- (Tinggi Minus)"
    harga = 75000
elif crisp_output >= 68:
    final_grade = "Grade B+ (Baik Plus)"
    harga = 65000
elif crisp_output >= 56:
    final_grade = "Grade B (Baik)"
    harga = 55000
elif crisp_output >= 44:
    final_grade = "Grade B- (Baik Minus)"
    harga = 45000
elif crisp_output >= 32:
    final_grade = "Grade C+ (Cukup Plus)"
    harga = 35000
elif crisp_output >= 18:
    final_grade = "Grade C (Cukup)"
    harga = 25000
else:
    final_grade = "Grade C- (Rendah)"
    harga = 15000

# Tentukan kategori tembakau berdasarkan rule dominan
max_rule = max(rules.items(), key=lambda x: x[1])
tobacco_mapping = {
    'R1': 'Tembakau Emas Cerah',
    'R2': 'Tembakau Emas Sedang',
    'R3': 'Tembakau Emas Gelap',
    'R4': 'Tembakau Kuning Cerah',
    'R5': 'Tembakau Kuning Sedang',
    'R6': 'Tembakau Kuning Gelap',
    'R7': 'Tembakau Hijau Cerah',
    'R8': 'Tembakau Hijau Sedang',
    'R9': 'Tembakau Hijau Gelap'
}
tobacco_type = tobacco_mapping[max_rule[0]]

print("\n" + "="*60)
print("🎯 HASIL AKHIR:")
print("="*60)
print(f"   Kategori      : {tobacco_type}")
print(f"   Grade         : {final_grade}")
print(f"   Skor          : {crisp_output:.2f}")
print(f"   Harga Estimasi: Rp {harga:,}/kg")
print(f"   Rule Dominan  : {max_rule[0]} (α = {max_rule[1]:.4f})")
print("="*60)
```

---

## 📝 Catatan Penggunaan:

1. **Ubah nilai input** pada variabel `input_hue` dan `input_value` sesuai data Anda
2. **Ubah nilai alpha** pada dictionary `alpha_aggregation` untuk simulasi defuzzification
3. **Semua grafik** akan otomatis ditampilkan
4. **Copy-paste** setiap cell ke Google Colab secara berurutan

---

## 🎯 Fitur:

✅ Grafik Keanggotaan Input (Hue & Value)  
✅ Grafik Keanggotaan Output (9 Grades)  
✅ Visualisasi Defuzzification dengan area arsiran  
✅ Simulasi End-to-End Fuzzy Mamdani  
✅ Output lengkap dengan grade & harga estimasi  

---

**Dibuat untuk**: Sistem Mutu Tembakau Madura  
**Metode**: Fuzzy Mamdani (9 Rules → 9 Grades)  
**Date**: 16 Januari 2026
