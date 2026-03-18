# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
import base64
from io import BytesIO
from PIL import Image
import numpy as np

app = FastAPI()

# Permitir conexiones desde el cliente HTML
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Recrear la clase del Generador
class Generador(nn.Module):
    def __init__(self):
        super(Generador, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(100, 256), nn.LeakyReLU(0.2),
            nn.Linear(256, 512), nn.LeakyReLU(0.2),
            nn.Linear(512, 1024), nn.LeakyReLU(0.2),
            nn.Linear(1024, 28 * 28), nn.Tanh()
        )
    def forward(self, x):
        return self.main(x).view(-1, 1, 28, 28)

# Cargar modelo
modelo = Generador()
modelo.load_state_dict(torch.load('generador.pth', weights_only=True))
modelo.eval()

@app.get("/generar")
def generar_imagen():
    # Generar ruido aleatorio
    ruido = torch.randn(1, 100)
    with torch.no_grad():
        img_tensor = modelo(ruido)

    # Post-procesar tensor a imagen
    img_array = img_tensor.squeeze().numpy()
    img_array = ((img_array + 1) / 2.0 * 255).astype(np.uint8) # Des-normalizar
    img_pil = Image.fromarray(img_array, mode='L')

    # Convertir a Base64 para enviarlo al cliente
    buffered = BytesIO()
    img_pil.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"imagen_base64": img_str}
