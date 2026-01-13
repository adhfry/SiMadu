# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build aplikasi
RUN npm run build

# Stage 2: Production dengan Nginx
FROM nginx:alpine

# Copy hasil build
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy konfigurasi nginx custom
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3012

CMD ["nginx", "-g", "daemon off;"]
