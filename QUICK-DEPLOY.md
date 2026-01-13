# Quick Deployment Commands

## Di VPS (Ubuntu)

```bash
# 1. Clone project
git clone <repo-url> simadu-project && cd simadu-project

# 2. Jalankan Docker
docker-compose up -d --build

# 3. Setup Nginx
sudo cp nginx-configs/api.simadu.agribunker.id /etc/nginx/sites-available/
sudo cp nginx-configs/simadu.agribunker.id /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/api.simadu.agribunker.id /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/simadu.agribunker.id /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 4. Setup SSL
sudo certbot --nginx -d api.simadu.agribunker.id -d simadu.agribunker.id

# 5. Buka firewall
sudo ufw allow 'Nginx Full'

# SELESAI! Akses:
# Frontend: https://simadu.agribunker.id
# Backend API: https://api.simadu.agribunker.id
```

## Verifikasi

```bash
# Cek Docker
docker-compose ps

# Expected output:
# NAME               STATUS    PORTS
# simadu-backend     Up        0.0.0.0:5012->5012/tcp
# simadu-frontend    Up        0.0.0.0:3012->3012/tcp

# Test port
curl http://localhost:5012/api/grade
curl http://localhost:3012

# Cek Nginx
sudo nginx -t
sudo systemctl status nginx
```
