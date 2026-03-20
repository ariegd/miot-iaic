import streamlit as st
import requests

# 1. Configuración básica de la página
st.set_page_config(page_title="Recomendador IA", page_icon="🍿", layout="centered")

# 2. Título y descripción
st.title("🎬 Sistema de Recomendación de Películas")
st.markdown("---")
st.write("Introduce el ID de un usuario y el ID de una película para consultar al modelo **SVD** qué calificación le daría.")

# 3. Creación de columnas para organizar los inputs
col1, col2 = st.columns(2)

with col1:
    user_id = st.text_input("👤 ID del Usuario", value="196")
    
with col2:
    item_id = st.text_input("🎞️ ID de la Película", value="302")

# 4. Botón de acción principal
st.markdown("<br>", unsafe_allow_html=True) # Espacio en blanco
if st.button("🔮 Obtener Predicción", use_container_width=True):
    
    if user_id and item_id:
        # Mostrar un spinner visual mientras esperamos al servidor
        with st.spinner('Consultando al servidor de IA...'):
            try:
                # Hacemos la petición al servidor Flask que creamos en la Parte B
                url = 'http://127.0.0.1:5000/predict'
                data = {'user_id': user_id, 'item_id': item_id}
                
                response = requests.post(url, json=data)
                response.raise_for_status() # Lanza error si el servidor falla
                
                resultado = response.json()
                rating = float(resultado['predicted_rating'])
                
                # 5. Mostrar el resultado de forma atractiva
                st.success("¡Predicción recibida con éxito!")
                
                # Usamos st.metric para un diseño de "Dashboard"
                st.metric(label="🌟 Rating Estimado", value=f"{rating} / 5.0")
                
                # Extra: Mostrar estrellas visuales basadas en el rating redondeado
                estrellas = int(round(rating))
                st.markdown(f"**Calificación visual:** {'⭐' * estrellas}{'🌑' * (5 - estrellas)}")
                
            except requests.exceptions.ConnectionError:
                st.error("🚨 Error: No se pudo conectar al servidor. Asegúrate de que `server.py` está corriendo en otra terminal.")
            except Exception as e:
                st.error(f"⚠️ Ocurrió un error inesperado: {e}")
    else:
        st.warning("👆 Por favor, introduce tanto el ID del usuario como el ID de la película.")
