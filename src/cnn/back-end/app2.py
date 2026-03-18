import torch
import torch.nn as nn
import torchvision.transforms as transforms
from flask import Flask, request, jsonify, render_template
#from PIL import Image, ImageOps
from PIL import Image, ImageOps, ImageFilter
import io
import base64

# app = Flask(__name__)
app = Flask(__name__, template_folder='../front-end')

# 1. Definir la misma arquitectura de red que usamos antes
class FashionCNN(nn.Module):
    def __init__(self):
        super(FashionCNN, self).__init__()

        # Primera capa Convolucional
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        # Segunda capa Convolucional
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        # Capas Lineales (Totalmente conectadas)
        self.fc1 = nn.Linear(in_features=64 * 6 * 6, out_features=600)
        self.drop = nn.Dropout(0.25)
        self.fc2 = nn.Linear(in_features=600, out_features=10)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.view(out.size(0), -1)
        out = self.fc1(out)
        out = self.drop(out)
        out = self.fc2(out)
        return out

# 2. Cargar el modelo
model = FashionCNN()
model.load_state_dict(torch.load('modelo_zalando_aumentado.pth', map_location=torch.device('cpu')))
model.eval() # Modo evaluación

classes = ('Camiseta/Top', 'Pantalón', 'Jersey', 'Vestido', 'Abrigo',
           'Sandalia', 'Camisa', 'Zapatilla', 'Bolso', 'Botín')

# Transformación: igual a la del entrenamiento, pero añadiendo el redimensionado
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.Grayscale(),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Recibir la imagen en base64 desde la web
    data = request.get_json()
    image_data = data['image'].split(',')[1] # Quitar la cabecera "data:image/png;base64,"
    
    # Decodificar la imagen
    '''image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    
    # IMPORTANTE: Fashion-MNIST tiene fondo negro y trazo blanco. 
    # Si en la web dibujan sobre fondo blanco, hay que invertir los colores.
    # image = ImageOps.invert(image.convert('RGB')) 
    
    # Aplicar transformaciones para PyTorch
    tensor = transform(image).unsqueeze(0) # Añadir dimensión de 'batch' (1, 1, 28, 28)'''

    # Decodificar la imagen
    image_bytes = base64.b64decode(image_data)

    # 1. Abrir y asegurar que está en escala de grises ('L')
    image = Image.open(io.BytesIO(image_bytes)).convert('L')

    # --- EL TRUCO DE PREPROCESAMIENTO ---
    # 2. Engordar las líneas (MaxFilter expande los píxeles blancos)
    # Un valor de 9 o 11 hace que las líneas de 280x280 se vuelvan muy gruesas
    image = image.filter(ImageFilter.MaxFilter(11))

    # 3. Desenfocar los bordes para simular la textura de Fashion-MNIST
    image = image.filter(ImageFilter.GaussianBlur(radius=4))
    # ------------------------------------

    # 4. Aplicar transformaciones para PyTorch (Reducir a 28x28 y normalizar)
    tensor = transform(image).unsqueeze(0)


    
    # Hacer la predicción
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted = torch.max(outputs.data, 1)
        clase_predicha = classes[predicted.item()]
        
    return jsonify({'prediction': clase_predicha})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
