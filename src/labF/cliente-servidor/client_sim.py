import pandas as pd
import requests
import time
import random

# Configuración
RUTA_CSV = '/content/drive/MyDrive/Colab Notebooks/iaic/labF/Resultados/df_imagenes_preprocesado.csv'
URL_SERVIDOR = 'http://localhost:5000/predict_bus'

# Cargar el dataset para simular
df = pd.read_csv(RUTA_CSV)

def simular_ruta():
    print("=== INICIANDO SISTEMA DE MONITOREO DE RUTA DINÁMICA ===")
    
    # Seleccionamos 5 paradas aleatorias para la simulación
    muestras = df.sample(5)
    
    for i, (index, row) in enumerate(muestras.iterrows()):
        foto_actual = row['ruta_imagen']
        personas_reales = row['personas_detectadas'] # Solo para comparar
        
        print(f"\n[Parada {i+1}] Autobús llegando... Enviando imagen a la central...")
        
        try:
            # Llamada al servidor
            response = requests.post(URL_SERVIDOR, json={'ruta_imagen': foto_actual})
            res = response.json()
            
            if response.status_code == 200:
                print(f"--- RESULTADO DE IA ---")
                print(f"ESTADO DETECTADO: {res['estado_aforo']} (Confianza: {res['confianza_deteccion']})")
                print(f"DECISIÓN DE NEGOCIO: {res['decision_ruteo']}")
                print(f"NOTIFICACIÓN: {res['mensaje_central']}")
                print(f"(Validación manual: Realmente había {personas_reales} personas)")
            else:
                print(f"Error en el servidor: {res.get('error')}")
                
        except Exception as e:
            print(f"Error de conexión con el servidor: {e}")
        
        time.sleep(3) # Esperar 3 segundos para la siguiente parada

if __name__ == '__main__':
    simular_ruta()
