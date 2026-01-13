# Docker & Deployment Guide - SiMadu Project

## 📋 Ringkasan Konfigurasi
- **Backend Port**: 5012
- **Frontend Port**: 3012
- **Technology**: Flask (Backend), Vue.js (Frontend), Docker, Nginx

---

## 🚀 Cara Deploy ke VPS

### 1. Persiapan VPS
```bash
# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose-plugin

# Atau install docker-compose standalone
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clone & Deploy Project
```bash
# Clone repository
git clone <your-repo-url> simadu-project
cd simadu-project

# Build & Run dengan Docker Compose
docker-compose up -d --build

# Cek status container
docker-compose ps

# Lihat logs
docker-compose logs -f
```

### 3. Konfigurasi Nginx di VPS Ubuntu

```bash
# Copy file konfigurasi
sudo cp nginx-host.conf /etc/nginx/sites-available/simadu

# Aktifkan konfigurasi
sudo ln -s /etc/nginx/sites-available/simadu /etc/nginx/sites-enabled/

# Test konfigurasi
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

**Pastikan DNS sudah di-pointing ke VPS:**
- `simadu.agribunker.id` → IP VPS Anda
- `api.simadu.agribunker.id` → IP VPS Anda

**Buka port di firewall (jika belum):**
```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 3012
sudo ufw allow 5012
```

### 4. Setup SSL dengan Let's Encrypt (PENTING untuk Production)
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Generate SSL Certificate untuk kedua domain
sudo certbot --nginx -d simadu.agribunker.id -d api.simadu.agribunker.id

# Certbot akan otomatis:
# 1. Generate SSL certificate
# 2. Update konfigurasi Nginx
# 3. Setup auto-renewal

# Verifikasi auto-renewal
sudo certbot renew --dry-run
```

---

## 🛠️ Development

### Build Ulang Container
```bash
# Rebuild semua services
docker-compose up -d --build

# Rebuild service tertentu
docker-compose up -d --build backend
docker-compose up -d --build frontend
```

### Debugging
```bash
# Masuk ke container backend
docker exec -it simadu-backend sh

# Masuk ke container frontend
docker exec -it simadu-frontend sh

# Lihat logs real-time
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop & Remove
```bash
# Stop containers
docker-compose stop

# Stop & remove containers
docker-compose down

# Remove dengan volumes
docker-compose down -v
```

---

## 📝 Struktur File Docker

```
simadu-project/
├── docker-compose.yml          # Orchestration untuk semua services
├── nginx-host.conf             # Konfigurasi Nginx untuk VPS host
├── backend/
│   ├── Dockerfile              # Docker image untuk Flask backend
│   ├── app.py
│   └── requirements.txt
└── fe-simadu/
    ├── Dockerfile              # Docker image untuk Vue.js frontend
    ├── nginx.conf              # Nginx config di dalam container frontend
    ├── package.json
    └── src/
```

---

## 🔧 Troubleshooting

### Port Sudah Digunakan
```bash
# Cek port yang digunakan
sudo netstat -tulpn | grep :5012
sudo netstat -tulpn | grep :3012

# Matikan process yang menggunakan port
sudo kill -9 <PID>
```

### Container Tidak Bisa Start
```bash
# Lihat logs error
docker-compose logs

# Rebuild dari scratch
docker-compose down
docker-compose up -d --build --force-recreate
```

### Frontend Tidak Bisa Akses Backend
Pastikan di file `.env` atau konfigurasi frontend, API URL mengarah ke:
- Development: `http://localhost:5012`
- Production: `https://api.simadu.agribunker.id`

Update file `.env` di frontend sebelum build:
```bash
VITE_API_URL=https://api.simadu.agribunker.id
```

---

## 🔄 Update Aplikasi

```bash
# Pull perubahan terbaru
git pull origin main

# Rebuild & restart
docker-compose up -d --build

# Atau rebuild tanpa cache
docker-compose build --no-cache
docker-compose up -d
```

---

## 💡 Tips

1. **Backup Database**: Jika menggunakan database, tambahkan volume mapping di docker-compose.yml
2. **Environment Variables**: Gunakan file `.env` untuk konfigurasi sensitif
3. **Monitoring**: Gunakan `docker stats` untuk monitoring resource usage
4. **Logs Rotation**: Setup log rotation untuk mencegah disk penuh

---

## 📞 Support

Jika ada masalah, cek:
1. Logs container: `docker-compose logs`
2. Status container: `docker-compose ps`
3. Resource VPS: `free -h` dan `df -h`
