import requests

# URL del servidor local
url = 'http://127.0.0.1:5000/predict'

# Datos de prueba: queremos saber qué nota le daría el usuario 196 a la peli 302
data = {
    'user_id': '196',
    'item_id': '302'
}

print(f"Enviando petición al servidor para User {data['user_id']} e Item {data['item_id']}...")

try:
    response = requests.post(url, json=data)
    response.raise_for_status() # Verifica si hubo error HTTP
    
    resultado = response.json()
    print("\n¡Respuesta recibida del servidor!")
    print(f"El sistema estima que el usuario {resultado['user_id']} le dará un rating de {resultado['predicted_rating']} a la película {resultado['item_id']}.")
    
except Exception as e:
    print(f"Error conectando con el servidor: {e}")
