from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

app = Flask(__name__, template_folder='../frontend')
CORS(app) # Permite peticiones desde el cliente web

# 1. CARGAMOS LOS ARCHIVOS NUEVOS EN ESPAÑOL
model = tf.keras.models.load_model('brnn_sentiment_es_model.h5')
with open('tokenizer_es.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# 2. EL MISMO TAMAÑO QUE EN EL ENTRENAMIENTO (50)
MAX_LENGTH = 50

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # 1. Obtenemos el texto
    texto = data.get('text', '')
    if not texto:
        texto = data.get('texto', '')

    if not texto:
        return jsonify({'error': 'No se proporcionó texto'}), 400

    try:
        # 2. Preprocesamiento
        secuencia = tokenizer.texts_to_sequences([texto])
        padded = pad_sequences(secuencia, maxlen=MAX_LENGTH, padding='post')

        # 3. Predicción
        predicciones = model.predict(padded)
        score_crudo = float(predicciones[0][0].item()) # Número puro (0.0 a 1.0)

        # 4. Lógica de Sentimiento
        if score_crudo > 0.5:
            sentimiento = "Positivo"
        else:
            sentimiento = "Negativo"

        # 5. ¡AQUÍ ESTABA EL ERROR!
        # Volvemos a usar la palabra 'confianza' y enviamos el número crudo
        # para que el index.html no se rompa.
        return jsonify({
            'texto': texto,
            'sentimiento': sentimiento,
            'confianza': score_crudo
        })

    except Exception as e:
        print(f"Error en predicción: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
