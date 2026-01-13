import numpy as np
import cv2
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# ============================================
# KONFIGURASI & LOGGING
# ============================================
# Mengatur logging agar rapi dan informatif (Traceability)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("SiMadu_Fuzzy")

app = Flask(__name__)

# CORS - Izinkan semua origin untuk production
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})

# ============================================
# 1. IMAGE PROCESSING (PRE-PROCESSING)
# ============================================
def extract_hue_value_from_image(image_file):
    """
    Mengambil nilai rata-rata Hue (Warna) dan Value (Kecerahan)
    dari citra yang diupload.
    """
    try:
        # 1. Baca gambar ke numpy array
        file_bytes = image_file.read()
        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("File gambar rusak atau format tidak didukung.")

        # 2. Resize untuk mempercepat komputasi (Opsional tapi direkomendasikan)
        img = cv2.resize(img, (300, 300))

        # 3. Konversi BGR ke HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 4. Hitung Rata-rata
        # Hue OpenCV: 0-179 (Kita pakai 0-80 sesuai domain tembakau)
        # Value OpenCV: 0-255
        avg_hue = np.mean(hsv[:, :, 0])
        avg_value = np.mean(hsv[:, :, 2])
        
        # LOGGING PENTING
        logger.info(f"[CITRA] Hue Asli: {avg_hue:.2f}, Value Asli: {avg_value:.2f}")

        return round(avg_hue, 2), round(avg_value, 2)

    except Exception as e:
        logger.error(f"Error Processing: {str(e)}")
        raise

# ============================================
# 2. FUZZIFICATION (CRISP -> FUZZY)
# ============================================
def fuzzification(hue, value):
    """
    Menghitung derajat keanggotaan (μ) dengan parameter yang LEBIH LONGGAR.
    Tujuannya agar foto indoor/kamera HP bisa mendapatkan Grade A.
    """
    fuzzy_input = {}
    
    # --- VARIABEL 1: WARNA (HUE) [0-180] ---
    # Update: Range Emas diperlebar agar Kuning agak oranye tetap dianggap Emas
    
    # Himpunan EMAS (Premium): Trapesium Kiri [0, 0, 25, 45] (Sebelumnya 20, 35)
    if hue <= 25:
        fuzzy_input['emas'] = 1.0
    elif 25 < hue < 45:
        fuzzy_input['emas'] = (45 - hue) / (45 - 25)
    else:
        fuzzy_input['emas'] = 0.0

    # Himpunan KUNING (Sedang): Segitiga [25, 45, 65] (Digeser menyesuaikan Emas)
    if 25 < hue <= 45:
        fuzzy_input['kuning'] = (hue - 25) / (45 - 25)
    elif 45 < hue < 65:
        fuzzy_input['kuning'] = (65 - hue) / (65 - 45)
    else:
        fuzzy_input['kuning'] = 0.0

    # Himpunan HIJAU (Rendah): Trapesium Kanan [55, 75, 80, 80]
    if hue < 55:
        fuzzy_input['hijau'] = 0.0
    elif 55 <= hue < 75:
        fuzzy_input['hijau'] = (hue - 55) / (75 - 55)
    else:
        fuzzy_input['hijau'] = 1.0

    # --- VARIABEL 2: KECERAHAN (VALUE) [0-255] ---
    # Update PENTING: Menurunkan standar "Cerah" agar foto indoor bisa masuk Grade A
    
    # Himpunan GELAP (Buruk): Trapesium Kiri [0, 0, 80, 120]
    if value <= 80:
        fuzzy_input['gelap'] = 1.0
    elif 80 < value < 120:
        fuzzy_input['gelap'] = (120 - value) / (120 - 80)
    else:
        fuzzy_input['gelap'] = 0.0

    # Himpunan SEDANG: Segitiga [100, 140, 180]
    if 100 < value <= 140:
        fuzzy_input['sedang'] = (value - 100) / (140 - 100)
    elif 140 < value < 180:
        fuzzy_input['sedang'] = (180 - value) / (180 - 140)
    else:
        fuzzy_input['sedang'] = 0.0

    # Himpunan CERAH (Bagus): Trapesium Kanan [130, 170, 255, 255] (Sebelumnya start 150)
    # Sekarang nilai 170 sudah dianggap Cerah Sempurna (1.0)
    if value < 130:
        fuzzy_input['cerah'] = 0.0
    elif 130 <= value < 170:
        fuzzy_input['cerah'] = (value - 130) / (170 - 130)
    else: 
        fuzzy_input['cerah'] = 1.0

    logger.info(f"[FUZZY TUNED] Input μ: {fuzzy_input}")
    return fuzzy_input

# ============================================
# 3. INFERENCE (EVALUASI RULE)
# ============================================
def inference(fi):
    """
    Menerapkan Aturan IF-THEN (Min Implication)
    Dan Agregasi (Max Composition)
    """
    rules = {}
    
    # Rule 1: IF Emas AND Cerah THEN Grade A
    rules['R1'] = min(fi['emas'], fi['cerah'])
    
    # Rule 2: IF Emas AND Sedang THEN Grade B
    rules['R2'] = min(fi['emas'], fi['sedang'])
    
    # Rule 3: IF Kuning AND Cerah THEN Grade B
    rules['R3'] = min(fi['kuning'], fi['cerah'])
    
    # Rule 4: IF Kuning AND Sedang THEN Grade B
    rules['R4'] = min(fi['kuning'], fi['sedang'])
    
    # Rule 5: IF Hijau THEN Grade C (Singular rule, no AND)
    rules['R5'] = fi['hijau']
    
    # Rule 6: IF Gelap THEN Grade C (Singular rule, no AND)
    rules['R6'] = fi['gelap']

    # AGREGASI (MAX)
    # Menentukan tinggi daerah arsir untuk setiap himpunan Output
    aggregated = {
        'A': rules['R1'],
        'B': max(rules['R2'], rules['R3'], rules['R4']),
        'C': max(rules['R5'], rules['R6'])
    }
    
    logger.info(f"[INFERENCE] Rules: {rules}")
    logger.info(f"[AGGREGATION] Max Values: {aggregated}")
    
    return rules, aggregated

# ============================================
# 4. DEFUZZIFICATION (CENTROID DISKRIT)
# ============================================

# --- Fungsi Keanggotaan Output (Grade 0-100) ---
def mu_grade_C(x): # Trapesium Kiri [0, 0, 20, 50]
    if x <= 20: return 1.0
    elif 20 < x < 50: return (50 - x) / (50 - 20)
    return 0.0

def mu_grade_B(x): # Segitiga [30, 50, 70]
    if 30 < x <= 50: return (x - 30) / (50 - 30)
    elif 50 < x < 70: return (70 - x) / (70 - 50)
    return 0.0

def mu_grade_A(x): # Trapesium Kanan [50, 80, 100, 100]
    if x < 50: return 0.0
    elif 50 <= x < 80: return (x - 50) / (80 - 50)
    return 1.0

def defuzzification(aggregated):
    """
    Menghitung Titik Berat (Centroid) dari area terarsir.
    Metode: Discretized Centroid (Sesuai PDF Hal 19)
    """
    numerator = 0   # Σ(x * μ)
    denominator = 0 # Σ(μ)
    
    # Array untuk menampung titik grafik (untuk visualisasi Frontend)
    graph_points = []
    
    # Loop sampling x dari 0 sampai 100
    for x in range(0, 101, 1):
        # Cari nilai asli kurva output pada titik x
        m_A = mu_grade_A(x)
        m_B = mu_grade_B(x)
        m_C = mu_grade_C(x)
        
        # Potong (Clip) kurva dengan nilai Agregasi (Alpha Predikat)
        # Teknik: MIN
        clip_A = min(aggregated['A'], m_A)
        clip_B = min(aggregated['B'], m_B)
        clip_C = min(aggregated['C'], m_C)
        
        # Gabungkan semua kurva terpotong (Union)
        # Teknik: MAX
        mu_final = max(clip_A, clip_B, clip_C)
        
        # Akumulasi Momen
        numerator += x * mu_final
        denominator += mu_final
        
        # Simpan untuk grafik
        graph_points.append({'x': x, 'y': float(mu_final)})
        
    # Hitung Crisp Output
    if denominator == 0:
        score = 0
    else:
        score = numerator / denominator

    logger.info(f"[DEFUZZ] Score: {score:.2f} (Num: {numerator:.2f}, Den: {denominator:.2f})")
    
    return score, numerator, denominator, graph_points

# ============================================
# API ENDPOINT
# ============================================
@app.route('/api/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    try:
        # 1. Image Processing
        hue, value = extract_hue_value_from_image(request.files['image'])
        
        # 2. Fuzzification
        fuzzy_mem = fuzzification(hue, value)
        
        # 3. Inference
        rules, agg = inference(fuzzy_mem)
        
        # 4. Defuzzification
        score, num, den, graph = defuzzification(agg)
        
        # Penentuan Label Akhir (5 Kategori) & Harga
        grade_label = ""
        harga = 0
        
        # KATEGORI 1: Sangat Tinggi (Premium Grade A+)
        if score >= 85:
            grade_label = "Sangat Tinggi (Premium+)"
            harga = 95000
        # KATEGORI 2: Tinggi (Grade A)
        elif score >= 70:
            grade_label = "Tinggi (Grade A)"
            harga = 80000
        # KATEGORI 3: Standar (Grade B)
        elif score >= 50:
            grade_label = "Standar (Grade B)"
            harga = 60000
        # KATEGORI 4: Rendah (Grade C)
        elif score >= 30:
            grade_label = "Rendah (Grade C)"
            harga = 40000
        # KATEGORI 5: Sangat Rendah (Grade D/Afkir)
        else:
            grade_label = "Sangat Rendah (Grade D)"
            harga = 15000

        # Response JSON Lengkap (Traceable)
        return jsonify({
            'success': True,
            'data': {
                'input': {'hue': hue, 'value': value},
                'fuzzification': fuzzy_mem,
                'inference': {
                    'rules': {k: float(v) for k,v in rules.items()},
                    'aggregation': {k: float(v) for k,v in agg.items()}
                },
                'defuzzification': {
                    'score': round(score, 2),
                    'numerator': round(num, 2),
                    'denominator': round(den, 2)
                },
                'result': {
                    'grade': grade_label,
                    'price': harga
                },
                'graph_data': graph # Penting untuk Chart.js
            }
        })

    except Exception as e:
        logger.error(f"System Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    # Host 0.0.0.0 agar bisa diakses device lain di jaringan
    # Port bisa di-override via environment variable
    port = int(os.environ.get('PORT', 5012))
    app.run(debug=False, host='0.0.0.0', port=port)