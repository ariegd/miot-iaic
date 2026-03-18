# Guardar como app.py y ejecutar: python app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

# app = Flask(__name__)
app = Flask(__name__, template_folder='../frontend')
CORS(app) # Permite peticiones desde el cliente web

# Cargar el modelo y el tokenizer
model = tf.keras.models.load_model('brnn_sentiment_model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

MAX_LENGTH = 20

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    texto = data.get('texto', '')

    if not texto:
        return jsonify({'error': 'No se proporcionó texto'}), 400

    # Preprocesar el texto entrante
    secuencia = tokenizer.texts_to_sequences([texto])
    padded = pad_sequences(secuencia, maxlen=MAX_LENGTH, padding='post')

    # Predecir usando la BRNN
    prediccion = model.predict(padded)[0][0]
    sentimiento = "Positivo" if prediccion > 0.5 else "Negativo"

    return jsonify({
        'texto': texto,
        'sentimiento': sentimiento,
        'confianza': float(prediccion)
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
