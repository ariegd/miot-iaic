from flask import Flask, request, jsonify
from surprise import dump

app = Flask(__name__)

# Cargar el modelo que exportamos previamente
print("Cargando modelo...")
_, loaded_model = dump.load('mejor_modelo_svd.pkl')
print("Modelo listo.")

@app.route('/predict', methods=['POST'])
def predict_rating():
    # Recibimos el JSON del cliente
    data = request.json
    
    if not data or 'user_id' not in data or 'item_id' not in data:
        return jsonify({'error': 'Faltan parámetros user_id o item_id'}), 400
        
    user_id = str(data['user_id'])
    item_id = str(data['item_id'])
    
    # Realizamos la inferencia
    prediction = loaded_model.predict(user_id, item_id)
    
    # Devolvemos la predicción
    return jsonify({
        'user_id': user_id,
        'item_id': item_id,
        'predicted_rating': round(prediction.est, 2)
    })

if __name__ == '__main__':
    # Arrancamos el servidor en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
