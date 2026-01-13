# Panduan Troubleshooting Production

## Cek Status Backend di VPS

```bash
# 1. Cek apakah container berjalan
docker-compose ps

# Output yang diharapkan:
# NAME               STATUS              PORTS
# simadu-backend     Up 2 minutes        0.0.0.0:5012->5012/tcp
# simadu-frontend    Up 2 minutes        0.0.0.0:3012->3012/tcp

# 2. Cek logs backend
docker-compose logs -f backend

# 3. Cek logs frontend
docker-compose logs -f frontend

# 4. Test backend langsung dari VPS
curl http://localhost:5012/api/grade
# Seharusnya return: {"status": "SiMadu API is running"}

# 5. Test backend dari luar (jika firewall dibuka)
curl http://<IP-VPS>:5012/api/grade

# 6. Cek apakah port terbuka
sudo netstat -tulpn | grep 5012
sudo netstat -tulpn | grep 3012
```

## Fix Error 502 Bad Gateway

Error 502 berarti Nginx tidak bisa connect ke backend. Kemungkinan penyebab:

### 1. Backend tidak running
```bash
# Restart backend
docker-compose restart backend

# Atau rebuild
docker-compose up -d --build backend
```

### 2. Port tidak exposed
```bash
# Cek port mapping
docker port simadu-backend

# Seharusnya output:
# 5012/tcp -> 0.0.0.0:5012
```

### 3. Firewall block port
```bash
# Buka port untuk Docker
sudo ufw allow 5012/tcp
sudo ufw allow 3012/tcp
sudo ufw reload
```

### 4. Nginx config salah
```bash
# Test nginx config
sudo nginx -t

# Cek apakah proxy_pass benar
sudo cat /etc/nginx/sites-available/api.simadu.agribunker.id

# Seharusnya ada:
# proxy_pass http://localhost:5012;
```

### 5. SSL Certificate Issue
```bash
# Cek SSL certificate
sudo certbot certificates

# Renew jika ada masalah
sudo certbot renew --force-renewal
```

## Fix CORS Issues

Jika ada CORS error setelah backend running:

### 1. Cek CORS di Backend
Backend sudah ada CORS config. Pastikan allow semua origin:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})
```

### 2. Tambah CORS headers di Nginx (Opsional)
Edit `/etc/nginx/sites-available/api.simadu.agribunker.id`:

```nginx
location / {
    # CORS Headers
    add_header 'Access-Control-Allow-Origin' '*' always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
    add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization' always;
    
    # Handle preflight
    if ($request_method = 'OPTIONS') {
        return 204;
    }
    
    proxy_pass http://localhost:5012;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;
}
```

Lalu reload nginx:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

## Complete Diagnostic Commands

```bash
# Jalankan semua checks ini:

echo "=== Docker Status ==="
docker-compose ps

echo "=== Backend Logs (last 50 lines) ==="
docker-compose logs --tail=50 backend

echo "=== Frontend Logs (last 50 lines) ==="
docker-compose logs --tail=50 frontend

echo "=== Port Check ==="
sudo netstat -tulpn | grep -E '5012|3012'

echo "=== Backend Health Check ==="
curl http://localhost:5012/api/grade

echo "=== Nginx Config Test ==="
sudo nginx -t

echo "=== Nginx Status ==="
sudo systemctl status nginx

echo "=== SSL Certificate ==="
sudo certbot certificates

echo "=== Disk Space ==="
df -h

echo "=== Memory Usage ==="
free -h

echo "=== Docker Resources ==="
docker stats --no-stream
```

## Quick Fix Command

Jika semua gagal, coba rebuild total:

```bash
# Stop semua
docker-compose down

# Clean up
docker system prune -f

# Pull latest code
git pull origin main

# Rebuild dan restart
docker-compose up -d --build --force-recreate

# Wait 30 seconds
sleep 30

# Check status
docker-compose ps
docker-compose logs backend
curl http://localhost:5012/api/grade

# Reload nginx
sudo nginx -t && sudo systemctl reload nginx
```

## Check Environment Variables

```bash
# Di VPS, check file .env.production
cat fe-simadu/.env.production

# Seharusnya:
# VITE_API_URL=https://api.simadu.agribunker.id

# Check backend environment
docker-compose exec backend env | grep PORT
# Seharusnya: PORT=5012
```
