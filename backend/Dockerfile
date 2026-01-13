FROM python:3.11-slim

WORKDIR /app

# Install dependencies untuk OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy aplikasi
COPY . .

# Expose port 5012
EXPOSE 5012

# Jalankan aplikasi
CMD ["python", "app.py"]
