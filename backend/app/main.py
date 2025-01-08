from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI()

# CORS Middleware ekleniyor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Buraya izin vermek istediğiniz kaynakların URL'lerini yazabilirsiniz. Örneğin: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin veriliyor (GET, POST, PUT, DELETE, vb.)
    allow_headers=["*"],  # Tüm başlıklara izin veriliyor
)

count = 0  # Butona kaç kez tıklandığını tutacak olan değişken

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.get("/hello")
def read_item():
    global count  # Global değişkeni kullanmak için belirtiyoruz
    count += 1    # Her istek yapıldığında count arttırılıyor
    return {"message": f"Butona {count} kez tıklandı!"}




