import requests
import random
import time

# URL del servidor (apuntando al puerto 8080 configurado previamente)
URL_SERVIDOR = 'http://localhost:8080/telemetria'

print("Iniciando simulación del dispositivo IoT (Cosecha)...")

while True:
    # Simular lecturas de los sensores
    temp_simulada = round(random.uniform(20.0, 35.0), 2)  # Temperatura entre 20 y 35 grados
    hum_simulada = round(random.uniform(40.0, 80.0), 2)   # Humedad entre 40% y 80%

    datos_iot = {
        'temperatura': temp_simulada,
        'humedad': hum_simulada
    }

    print(f"\n[IoT] Enviando -> Temperatura: {temp_simulada}°C | Humedad: {hum_simulada}%")

    try:
        # Enviar petición POST al servidor
        respuesta = requests.post(URL_SERVIDOR, json=datos_iot)

        if respuesta.status_code == 200:
            resultado = respuesta.json()
            print(f"[Servidor] {resultado['mensaje']}")
        else:
            print(f"Error en el servidor: Código {respuesta.status_code}")

    except requests.exceptions.ConnectionError:
        print("[Error] No se pudo conectar al servidor. Asegúrate de que esté encendido.")

    # Esperar 5 segundos antes de enviar la siguiente lectura
    time.sleep(5)
