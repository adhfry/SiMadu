# Panduan Setup di VPS Ubuntu

## 1. Upload Project ke VPS
```bash
# Clone atau upload project ke VPS
git clone <your-repo> simadu-project
cd simadu-project
```

## 2. Jalankan Docker
```bash
# Build dan jalankan semua container
docker-compose up -d --build

# Cek status container
docker-compose ps

# Output yang diharapkan:
# simadu-backend    running    0.0.0.0:5012->5012/tcp
# simadu-frontend   running    0.0.0.0:3012->3012/tcp

# Cek logs
docker-compose logs -f
```

## 3. Setup Nginx di VPS

### Copy file konfigurasi Nginx
```bash
# Copy file untuk backend
sudo cp nginx-configs/api.simadu.agribunker.id /etc/nginx/sites-available/

# Copy file untuk frontend
sudo cp nginx-configs/simadu.agribunker.id /etc/nginx/sites-available/

# Buat symlink untuk mengaktifkan
sudo ln -s /etc/nginx/sites-available/api.simadu.agribunker.id /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/simadu.agribunker.id /etc/nginx/sites-enabled/

# Test konfigurasi Nginx
sudo nginx -t

# Jika OK, reload Nginx
sudo systemctl reload nginx
```

## 4. Setup Firewall (UFW)
```bash
# Pastikan port yang diperlukan terbuka
sudo ufw allow 'Nginx Full'
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3012/tcp
sudo ufw allow 5012/tcp

# Cek status
sudo ufw status
```

## 5. Test Akses
```bash
# Test backend (dari VPS)
curl http://localhost:5012/api/grade

# Test frontend (dari VPS)
curl http://localhost:3012

# Test dari browser:
# http://api.simadu.agribunker.id
# http://simadu.agribunker.id
```

## 6. Setup SSL dengan Let's Encrypt
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Generate SSL untuk kedua domain sekaligus
sudo certbot --nginx -d api.simadu.agribunker.id -d simadu.agribunker.id

# Ikuti instruksi interaktif
# - Enter email
# - Agree to terms
# - Pilih redirect HTTP ke HTTPS (recommended)

# Test auto-renewal
sudo certbot renew --dry-run
```

## 7. Monitoring & Maintenance

### Cek Status Docker
```bash
# Lihat container yang berjalan
docker-compose ps

# Lihat resource usage
docker stats

# Lihat logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services
```bash
# Restart semua container
docker-compose restart

# Restart service tertentu
docker-compose restart backend
docker-compose restart frontend

# Rebuild jika ada perubahan code
docker-compose up -d --build
```

### Cek Nginx
```bash
# Test konfigurasi
sudo nginx -t

# Reload
sudo systemctl reload nginx

# Restart
sudo systemctl restart nginx

# Lihat status
sudo systemctl status nginx
```

## 8. Update Aplikasi
```bash
# Pull perubahan terbaru
git pull origin main

# Rebuild dan restart
docker-compose down
docker-compose up -d --build

# Atau tanpa downtime (zero-downtime)
docker-compose up -d --build --no-deps backend
docker-compose up -d --build --no-deps frontend
```

## Troubleshooting

### Port sudah digunakan
```bash
# Cek port 5012
sudo netstat -tulpn | grep :5012
sudo lsof -i :5012

# Cek port 3012
sudo netstat -tulpn | grep :3012
sudo lsof -i :3012

# Kill process jika perlu
sudo kill -9 <PID>
```

### Container tidak start
```bash
# Lihat logs error
docker-compose logs backend
docker-compose logs frontend

# Remove dan rebuild
docker-compose down -v
docker-compose up -d --build --force-recreate
```

### Nginx error
```bash
# Cek error log
sudo tail -f /var/log/nginx/error.log

# Cek access log
sudo tail -f /var/log/nginx/access.log

# Cek konfigurasi
sudo nginx -t
```

## Struktur Akhir di VPS

```
/home/user/simadu-project/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   └── app.py
├── fe-simadu/
│   ├── Dockerfile
│   └── nginx.conf
└── nginx-configs/
    ├── api.simadu.agribunker.id
    └── simadu.agribunker.id

/etc/nginx/sites-available/
├── api.simadu.agribunker.id
└── simadu.agribunker.id

/etc/nginx/sites-enabled/
├── api.simadu.agribunker.id -> ../sites-available/api.simadu.agribunker.id
└── simadu.agribunker.id -> ../sites-available/simadu.agribunker.id
```

## Alur Request

```
User Browser
    ↓
simadu.agribunker.id (DNS)
    ↓
Nginx (Port 80/443)
    ↓
localhost:3012 (Docker Frontend)


User Browser
    ↓
api.simadu.agribunker.id (DNS)
    ↓
Nginx (Port 80/443)
    ↓
localhost:5012 (Docker Backend)
```
