from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import joblib
import cv2
import os

app = Flask(__name__)

# --- CONFIGURACIÓN Y CARGA DE MODELOS ---
RUTA_RESULTADOS = '/content/drive/MyDrive/Colab Notebooks/iaic/labF/Resultados/'
MODELO_CNN_PATH = os.path.join(RUTA_RESULTADOS, 'modelo_cnn.keras')
MODELO_Q_PATH = os.path.join(RUTA_RESULTADOS, 'pipeline_qlearning.joblib')

print("Cargando modelos en el servidor...")
cnn_model = load_model(MODELO_CNN_PATH)
q_pipeline = joblib.load(MODELO_Q_PATH)

# Mapeos
ESTADOS = q_pipeline['estados']    # ['Vacío', 'Medio', 'Lleno']
ACCIONES = q_pipeline['acciones']  # ['Normal', 'Saltar_Parada', 'Enviar_Refuerzo']
Q_TABLE = q_pipeline['Q_table']

def preparar_imagen(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    img = cv2.resize(img, (150, 150)) # El tamaño que definimos en el entrenamiento
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/predict_bus', methods=['POST'])
def predict_bus():
    data = request.get_json()
    ruta_img = data.get('ruta_imagen')
    
    if not os.path.exists(ruta_img):
        return jsonify({'error': 'Imagen no encontrada'}), 404

    # 1. Percepción (CNN)
    img_ready = preparar_imagen(ruta_img)
    pred_cnn = cnn_model.predict(img_ready)
    idx_estado = np.argmax(pred_cnn)
    estado_nombre = ESTADOS[idx_estado]
    confianza_cnn = float(np.max(pred_cnn))

    # 2. Decisión (Q-Learning)
    # Buscamos en la Q-Table la mejor acción para el estado detectado
    idx_accion = np.argmax(Q_TABLE[idx_estado])
    accion_nombre = ACCIONES[idx_accion]
    valor_q = float(Q_TABLE[idx_estado][idx_accion])

    # 3. Respuesta profesional
    return jsonify({
        'estado_aforo': estado_nombre,
        'confianza_deteccion': f"{confianza_cnn:.2%}",
        'decision_ruteo': accion_nombre,
        'valor_confianza_ia': round(valor_q, 2),
        'mensaje_central': f"Atención: Aforo {estado_nombre}. Acción: {accion_nombre}"
    })

if __name__ == '__main__':
    # Ejecutar en puerto 5000
    app.run(host='0.0.0.0', port=5000)
