from flask import Flask, request, jsonify
import joblib
import warnings

# Ignorar advertencias de scikit-learn
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Cargar el modelo previamente descargado
modelo = joblib.load('modelo_cosecha.pkl')

@app.route('/telemetria', methods=['POST'])
def recibir_telemetria():
    datos = request.json
    temperatura = datos.get('temperatura')
    humedad = datos.get('humedad')

    # El modelo espera una matriz 2D: [[temperatura, humedad]]
    prediccion = modelo.predict([[temperatura, humedad]])[0]

    # Si la predicción es 1 (temperatura > 28 y humedad > 60), se activa el riego
    if prediccion == 1:
        mensaje = "ALERTA: Temperatura y humedad muy altas. ACTIVANDO RIEGO DE AGUA."
        regar = True
    else:
        mensaje = "Condiciones estables. Riego apagado."
        regar = False

    return jsonify({
        'temperatura_recibida': temperatura,
        'humedad_recibida': humedad,
        'prediccion_modelo': int(prediccion),
        'activar_riego': regar,
        'mensaje': mensaje
    })

if __name__ == '__main__':
    # Usamos el puerto 8080 para evitar el 5000
    app.run(host='0.0.0.0', port=8080)
