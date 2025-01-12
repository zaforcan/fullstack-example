from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import json
import aiohttp
import asyncio
import urllib.request
import os
from PIL import Image
import io
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Static klasör tanımı
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)  # Static klasörünü oluştur

# Static klasörünü servis etmek için
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS Middleware ekleniyor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Buraya izin vermek istediğiniz kaynakların URL'lerini yazabilirsiniz. Örneğin: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin veriliyor (GET, POST, PUT, DELETE, vb.)
    allow_headers=["*"],  # Tüm başlıklara izin veriliyor
)

class PromptRequest(BaseModel):
    text: str

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


async def queue_prompt(prompt, server_address):
    url = f"http://{server_address}/prompt"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=prompt) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def get_history(prompt_id, server_address):
    max_attempts = 20
    attempt = 0
    url = f"http://{server_address}/history/{prompt_id}"
    
    while attempt < max_attempts:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=120) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        print("Response from get_history:", response_data)
                        
                        # Boş olmayan bir yanıt alındığında işlemi kontrol et
                        if response_data and response_data != {}:
                            uuid_key = list(response_data.keys())[0]  # İlk UUID anahtarı al
                            return response_data[uuid_key]
                        else:
                            print(f"Attempt {attempt + 1}: Still waiting for completion...")
                    else:
                        print(f"Attempt {attempt + 1}: Unexpected status code: {response.status}")
        except Exception as e:
            print(f"Error fetching history on attempt {attempt + 1}: {e}")
        
        await asyncio.sleep(10)  # Her denemeden sonra 60 saniye bekle
        attempt += 1

    print("Failed to retrieve history after several attempts.")
    return None

def get_image(filename, subfolder, folder_type, server_address="host.docker.internal:8188"):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    url = f"http://{server_address}/view?{url_values}"
    print(f"Fetching image from URL: {url}")
    
    try:
        with urllib.request.urlopen(url, timeout=120) as response:
            return response.read()
    except Exception as e:
        print(f"Failed to fetch image: {e}")
        return None

@app.post("/generate-images/")
async def generate_images(request: PromptRequest):
    server_address = "host.docker.internal:8188"
    client_id = str(uuid.uuid4())

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        workflow_file_path = os.path.join(current_dir, "workflow_api.json")
        with open(workflow_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="workflow_api.json file not found.")
    
    json_data["6"]["inputs"]["text"] = request.text
    prompt = {"prompt": json_data, "client_id": client_id}

    # Prompt'u kuyruğa eklemek için sunucuya gönder
    queue_response = await queue_prompt(prompt, server_address)
    if not queue_response:
        raise HTTPException(status_code=500, detail="Failed to queue the prompt due to an error.")

    prompt_id = queue_response.get("prompt_id")
    if not prompt_id:
        raise HTTPException(status_code=500, detail="No prompt ID returned.")

    # İşlem tamamlanana kadar get_history üzerinden durum kontrolü yap
    history = await get_history(prompt_id, server_address)
    if not history:
        raise HTTPException(status_code=500, detail="Failed to retrieve history.")

    # Görüntüleri işleme ve kaydetme
    outputs = history.get("outputs", {})
    saved_images = []
    for node_id, node_output in outputs.items():
        if "images" in node_output:
            for image_info in node_output["images"]:
                filename = image_info["filename"]
                subfolder = image_info["subfolder"]
                folder_type = image_info["type"]

                # Görüntüyü indir
                image_data = get_image(filename, subfolder, folder_type, server_address)
                if image_data:
                    # Görüntüyü aç ve kaydet
                    image = Image.open(io.BytesIO(image_data))
                    save_path = os.path.join(STATIC_DIR, filename)
                    image.save(save_path)
                    saved_images.append(f"/static/{filename}")
                    print(f"Image saved at {save_path}")

    if not saved_images:
        raise HTTPException(status_code=500, detail="No images were generated.")

    # İşlem tamamlandıktan sonra sonuçları döndür
    return {"message": "Images generated successfully", "images": saved_images}




