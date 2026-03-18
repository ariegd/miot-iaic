from fastapi import FastAPI, Response
import torch
import torch.nn as nn
from io import BytesIO
from PIL import Image
import numpy as np

app = FastAPI()

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

# Cambiamos la ruta a "/" para que sea la página principal
@app.get("/")
def generar_imagen():
    # 1. Generar ruido aleatorio
    ruido = torch.randn(1, 100)
    with torch.no_grad():
        img_tensor = modelo(ruido)

    # 2. Post-procesar tensor a imagen
    img_array = img_tensor.squeeze().numpy()
    img_array = ((img_array + 1) / 2.0 * 255).astype(np.uint8) # Des-normalizar
    img_pil = Image.fromarray(img_array, mode='L')

    # 3. Guardar en memoria virtual como PNG
    buffered = BytesIO()
    img_pil.save(buffered, format="PNG")

    # 4. Devolver DIRECTAMENTE la imagen al navegador
    return Response(content=buffered.getvalue(), media_type="image/png")
