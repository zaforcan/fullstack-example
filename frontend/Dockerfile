# Base image olarak Node.js kullanılıyor
FROM node:18-alpine

# Çalışma dizinini ayarla
WORKDIR /app

# package.json ve package-lock.json dosyalarını kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm install

# Uygulama dosyalarını kopyala
COPY . .

# Vite server'ı başlatmak için portu aç
EXPOSE 8501

# Başlatma komutunu ayarla
CMD ["npm", "run", "dev", "--", "--host"]
