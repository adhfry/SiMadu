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

    # Himpunan KUNING (Sedang): Segitiga [25, 45, 60]
    if 25 < hue <= 45:
        fuzzy_input['kuning'] = (hue - 25) / (45 - 25)
    elif 45 < hue < 60:
        fuzzy_input['kuning'] = (60 - hue) / (60 - 45)
    else:
        fuzzy_input['kuning'] = 0.0

    # Himpunan HIJAU (Rendah): Trapesium Kanan [50, 65, 80, 80]
    if hue < 50:
        fuzzy_input['hijau'] = 0.0
    elif 50 <= hue < 65:
        fuzzy_input['hijau'] = (hue - 50) / (65 - 50)
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
# 3. INFERENCE (EVALUASI RULE) - 9 RULES → 9 GRADES
# ============================================
def inference(fi):
    """
    Menerapkan 9 Aturan IF-THEN (Min Implication)
    Kombinasi: Warna (Emas, Kuning, Hijau) x Kecerahan (Cerah, Sedang, Gelap)
    Setiap rule menghasilkan grade berbeda (9 grades total)
    """
    rules = {}
    
    # === KATEGORI EMAS ===
    # Rule 1: IF Emas AND Cerah THEN Emas Cerah (Grade A+)
    rules['R1'] = min(fi['emas'], fi['cerah'])
    
    # Rule 2: IF Emas AND Sedang THEN Emas Sedang (Grade A)
    rules['R2'] = min(fi['emas'], fi['sedang'])
    
    # Rule 3: IF Emas AND Gelap THEN Emas Gelap (Grade A-)
    rules['R3'] = min(fi['emas'], fi['gelap'])
    
    # === KATEGORI KUNING ===
    # Rule 4: IF Kuning AND Cerah THEN Kuning Cerah (Grade B+)
    rules['R4'] = min(fi['kuning'], fi['cerah'])
    
    # Rule 5: IF Kuning AND Sedang THEN Kuning Sedang (Grade B)
    rules['R5'] = min(fi['kuning'], fi['sedang'])
    
    # Rule 6: IF Kuning AND Gelap THEN Kuning Gelap (Grade B-)
    rules['R6'] = min(fi['kuning'], fi['gelap'])
    
    # === KATEGORI HIJAU ===
    # Rule 7: IF Hijau AND Cerah THEN Hijau Cerah (Grade C+)
    rules['R7'] = min(fi['hijau'], fi['cerah'])
    
    # Rule 8: IF Hijau AND Sedang THEN Hijau Sedang (Grade C)
    rules['R8'] = min(fi['hijau'], fi['sedang'])
    
    # Rule 9: IF Hijau AND Gelap THEN Hijau Gelap (Grade C-)
    rules['R9'] = min(fi['hijau'], fi['gelap'])

    # AGREGASI (MAX) - 9 GRADES
    # Setiap rule menghasilkan grade sendiri
    aggregated = {
        'A_plus': rules['R1'],   # Emas Cerah
        'A': rules['R2'],         # Emas Sedang
        'A_minus': rules['R3'],   # Emas Gelap
        'B_plus': rules['R4'],    # Kuning Cerah
        'B': rules['R5'],         # Kuning Sedang
        'B_minus': rules['R6'],   # Kuning Gelap
        'C_plus': rules['R7'],    # Hijau Cerah
        'C': rules['R8'],         # Hijau Sedang
        'C_minus': rules['R9']    # Hijau Gelap
    }
    
    logger.info(f"[INFERENCE] 9 Rules: {rules}")
    logger.info(f"[AGGREGATION] 9 Grades: {aggregated}")
    
    return rules, aggregated

# ============================================
# 4. DEFUZZIFICATION (CENTROID DISKRIT)
# ============================================

# --- Fungsi Keanggotaan Output (Grade 0-100) - 9 GRADES ---
def mu_grade_C_minus(x): # Trapesium Kiri [0, 0, 5, 15]
    if x <= 5: return 1.0
    elif 5 < x < 15: return (15 - x) / 10
    return 0.0

def mu_grade_C(x): # Segitiga [10, 20, 30]
    if 10 < x <= 20: return (x - 10) / 10
    elif 20 < x < 30: return (30 - x) / 10
    return 0.0

def mu_grade_C_plus(x): # Segitiga [25, 35, 45]
    if 25 < x <= 35: return (x - 25) / 10
    elif 35 < x < 45: return (45 - x) / 10
    return 0.0

def mu_grade_B_minus(x): # Segitiga [40, 48, 56]
    if 40 < x <= 48: return (x - 40) / 8
    elif 48 < x < 56: return (56 - x) / 8
    return 0.0

def mu_grade_B(x): # Segitiga [52, 60, 68]
    if 52 < x <= 60: return (x - 52) / 8
    elif 60 < x < 68: return (68 - x) / 8
    return 0.0

def mu_grade_B_plus(x): # Segitiga [64, 72, 80]
    if 64 < x <= 72: return (x - 64) / 8
    elif 72 < x < 80: return (80 - x) / 8
    return 0.0

def mu_grade_A_minus(x): # Segitiga [75, 82, 89]
    if 75 < x <= 82: return (x - 75) / 7
    elif 82 < x < 89: return (89 - x) / 7
    return 0.0

def mu_grade_A(x): # Segitiga [85, 91, 97]
    if 85 < x <= 91: return (x - 85) / 6
    elif 91 < x < 97: return (97 - x) / 6
    return 0.0

def mu_grade_A_plus(x): # Trapesium Kanan [92, 96, 100, 100]
    if x < 92: return 0.0
    elif 92 <= x < 96: return (x - 92) / 4
    return 1.0

def defuzzification(aggregated):
    """
    Menghitung Titik Berat (Centroid) dari area terarsir.
    Metode: Discretized Centroid (Sesuai PDF Hal 19)
    Dengan 9 Grades: A+, A, A-, B+, B, B-, C+, C, C-
    """
    numerator = 0   # Σ(x * μ)
    denominator = 0 # Σ(μ)
    
    # Array untuk menampung titik grafik (untuk visualisasi Frontend)
    graph_points = []
    
    # Loop sampling x dari 0 sampai 100
    for x in range(0, 101, 1):
        # Cari nilai asli kurva output pada titik x untuk setiap grade
        m_A_plus = mu_grade_A_plus(x)
        m_A = mu_grade_A(x)
        m_A_minus = mu_grade_A_minus(x)
        m_B_plus = mu_grade_B_plus(x)
        m_B = mu_grade_B(x)
        m_B_minus = mu_grade_B_minus(x)
        m_C_plus = mu_grade_C_plus(x)
        m_C = mu_grade_C(x)
        m_C_minus = mu_grade_C_minus(x)
        
        # Potong (Clip) kurva dengan nilai Agregasi (Alpha Predikat)
        # Setiap grade punya alpha sendiri dari aggregated
        clip_A_plus = min(aggregated['A_plus'], m_A_plus)
        clip_A = min(aggregated['A'], m_A)
        clip_A_minus = min(aggregated['A_minus'], m_A_minus)
        clip_B_plus = min(aggregated['B_plus'], m_B_plus)
        clip_B = min(aggregated['B'], m_B)
        clip_B_minus = min(aggregated['B_minus'], m_B_minus)
        clip_C_plus = min(aggregated['C_plus'], m_C_plus)
        clip_C = min(aggregated['C'], m_C)
        clip_C_minus = min(aggregated['C_minus'], m_C_minus)
        
        # Gabungkan semua kurva terpotong (Union)
        # Teknik: MAX
        mu_final = max(clip_A_plus, clip_A, clip_A_minus, 
                      clip_B_plus, clip_B, clip_B_minus,
                      clip_C_plus, clip_C, clip_C_minus)
        
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
# API ENDPOINTS
# ============================================
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'SiMadu API is running', 'version': '1.0.0'}), 200

@app.route('/api/grade', methods=['GET'])
def grade():
    return jsonify({'status': 'SiMadu API is running', 'version': '1.0.0'}), 200

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
        
        # Penentuan Label Akhir berdasarkan Rule yang Dominan
        # Cari rule dengan nilai tertinggi untuk menentukan kategori spesifik
        max_rule = max(rules.items(), key=lambda x: x[1])
        rule_name = max_rule[0]
        
        # Mapping rule ke kategori tembakau
        tobacco_category = {
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
        
        tobacco_type = tobacco_category.get(rule_name, 'Tembakau Unknown')
        
        # Penentuan Grade & Harga berdasarkan Skor
        grade_label = ""
        harga = 0
        
        # 9 KATEGORI GRADE
        if score >= 94:
            grade_label = "Grade A+ (Sangat Tinggi)"
            harga = 95000
        elif score >= 88:
            grade_label = "Grade A (Tinggi)"
            harga = 85000
        elif score >= 78:
            grade_label = "Grade A- (Tinggi Minus)"
            harga = 75000
        elif score >= 68:
            grade_label = "Grade B+ (Baik Plus)"
            harga = 65000
        elif score >= 56:
            grade_label = "Grade B (Baik)"
            harga = 55000
        elif score >= 44:
            grade_label = "Grade B- (Baik Minus)"
            harga = 45000
        elif score >= 32:
            grade_label = "Grade C+ (Cukup Plus)"
            harga = 35000
        elif score >= 18:
            grade_label = "Grade C (Cukup)"
            harga = 25000
        else:
            grade_label = "Grade C- (Rendah)"
            harga = 15000

        # Response JSON Lengkap (Traceable)
        return jsonify({
            'success': True,
            'data': {
                'input': {'hue': hue, 'value': value},
                'fuzzification': fuzzy_mem,
                'inference': {
                    'rules': {k: float(v) for k,v in rules.items()},
                    'aggregation': {k: float(v) for k,v in agg.items()},
                    'dominant_rule': rule_name
                },
                'defuzzification': {
                    'score': round(score, 2),
                    'numerator': round(num, 2),
                    'denominator': round(den, 2)
                },
                'result': {
                    'tobacco_type': tobacco_type,
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
    port = int(os.environ.get('PORT', 5055))
    app.run(debug=False, host='0.0.0.0', port=port)