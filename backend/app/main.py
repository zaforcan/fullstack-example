from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware ekleniyor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Buraya izin vermek istediğiniz kaynakların URL'lerini yazabilirsiniz. Örneğin: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin veriliyor (GET, POST, PUT, DELETE, vb.)
    allow_headers=["*"],  # Tüm başlıklara izin veriliyor
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

# Example endpoint
@app.get("/hello")
def read_item():
    return {"message": f"Hello apisi çok iyi çalıştı"}


