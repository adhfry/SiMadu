# SiMadu - Sistem Mutu Tembakau Madura

## Backend (Flask + Python)

### Setup Virtual Environment

```bash
# Aktivasi virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Menjalankan Server

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

### API Endpoints

- **POST** `/api/classify` - Klasifikasi mutu tembakau
- **GET** `/api/health` - Health check

### Metode Fuzzy Mamdani

1. **Fuzzifikasi**: Konversi crisp input (Hue, Value) ke derajat keanggotaan
2. **Inference**: Evaluasi aturan IF-THEN dengan MIN-MAX
3. **Defuzzifikasi**: Discretized Centroid untuk output crisp
