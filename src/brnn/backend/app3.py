from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import re
import nltk
from nltk.corpus import stopwords

# Descargar las stopwords de español en el servidor local la primera vez
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('spanish'))

app = Flask(__name__, template_folder='../frontend')
CORS(app)

# 1. Cargar los NUEVOS archivos
model = tf.keras.models.load_model('brnn_sentiment_es_model3.h5')
with open('tokenizer_es3.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

MAX_LENGTH = 100

# Función vital: La misma "dieta" que en el entrenamiento
def limpiar_texto(texto):
    texto = texto.lower() # Minúsculas
    texto = re.sub(r'[^\w\s]', '', texto) # Quitar puntuación
    # Dejar solo las palabras importantes
    palabras = [palabra for palabra in texto.split() if palabra not in stop_words]
    return " ".join(palabras)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Obtener el texto original
    texto_original = data.get('text', '')
    if not texto_original:
        texto_original = data.get('texto', '')

    if not texto_original:
        return jsonify({'error': 'No se proporcionó texto'}), 400

    try:
        # --- EL CAMBIO MÁGICO ---
        # Limpiamos el texto ANTES de tokenizarlo
        texto_limpio = limpiar_texto(texto_original)

        # Preprocesamiento con el texto ya limpio
        secuencia = tokenizer.texts_to_sequences([texto_limpio])
        padded = pad_sequences(secuencia, maxlen=MAX_LENGTH, padding='post')

        # Predicción
        predicciones = model.predict(padded)
        score_crudo = float(predicciones[0][0].item())

        # Lógica de Sentimiento
        if score_crudo > 0.5:
            sentimiento = "Positivo"
        else:
            sentimiento = "Negativo"

        # Enviamos la respuesta a tu index.html
        return jsonify({
            'texto': texto_original, # Devolvemos el texto original para que se vea bien
            'sentimiento': sentimiento,
            'confianza': score_crudo
        })

    except Exception as e:
        print(f"Error en predicción: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
