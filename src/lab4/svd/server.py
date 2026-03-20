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
    
@app.route('/recommend', methods=['POST'])
def recommend_top_10():
    data = request.json
    
    if not data or 'user_id' not in data:
        return jsonify({'error': 'Falta el parámetro user_id'}), 400
        
    user_id = str(data['user_id'])
    
    # 1. Obtener todos los IDs de películas que el modelo conoce
    # El trainset guarda los IDs internos, los convertimos a los IDs originales
    all_item_inner_ids = loaded_model.trainset.all_items()
    all_item_raw_ids = [loaded_model.trainset.to_raw_iid(inner_id) for inner_id in all_item_inner_ids]
    
    # 2. Predecir la calificación para todas esas películas
    predictions = []
    for item_id in all_item_raw_ids:
        pred = loaded_model.predict(user_id, item_id)
        predictions.append({
            'ID Película': item_id, 
            'Rating Estimado': round(pred.est, 2)
        })
        
    # 3. Ordenar de mayor a menor calificación y quedarnos con las 10 mejores
    predictions.sort(key=lambda x: x['Rating Estimado'], reverse=True)
    top_10 = predictions[:10]
    
    return jsonify({
        'user_id': user_id,
        'top_10': top_10
    })


if __name__ == '__main__':
    # Arrancamos el servidor en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
