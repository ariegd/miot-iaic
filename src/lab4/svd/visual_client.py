import streamlit as st
import requests
import pandas as pd

# Configuración básica de la página
st.set_page_config(page_title="Recomendador IA", page_icon="🍿", layout="centered")

st.title("🎬 Sistema de Recomendación de Películas")
st.markdown("---")

# Creamos dos pestañas para separar las funcionalidades
tab1, tab2 = st.tabs(["🔮 Predicción Individual", "🏆 Top 10 Recomendaciones"])

# ==========================================
# PESTAÑA 1: PREDICCIÓN INDIVIDUAL (La que ya teníamos)
# ==========================================
with tab1:
    st.write("Consulta la calificación estimada para una película específica.")
    col1, col2 = st.columns(2)

    with col1:
        user_id_single = st.text_input("👤 ID del Usuario", value="196", key="user1")
    with col2:
        item_id_single = st.text_input("🎞️ ID de la Película", value="302")

    if st.button("Obtener Predicción", use_container_width=True):
        if user_id_single and item_id_single:
            with st.spinner('Consultando al servidor...'):
                try:
                    url = 'http://127.0.0.1:5000/predict'
                    response = requests.post(url, json={'user_id': user_id_single, 'item_id': item_id_single})
                    response.raise_for_status()
                    
                    rating = float(response.json()['predicted_rating'])
                    st.success("¡Predicción recibida!")
                    st.metric(label="🌟 Rating Estimado", value=f"{rating} / 5.0")
                    
                except Exception as e:
                    st.error(f"Error conectando al servidor: {e}")
        else:
            st.warning("Introduce ambos IDs.")

# ==========================================
# PESTAÑA 2: TOP 10 RECOMENDACIONES (La nueva funcionalidad)
# ==========================================
with tab2:
    st.write("Genera las 10 mejores recomendaciones personalizadas para un usuario.")
    
    user_id_top = st.text_input("👤 ID del Usuario", value="196", key="user2")
    
    if st.button("Generar Top 10", use_container_width=True, type="primary"):
        if user_id_top:
            with st.spinner('El modelo de IA está analizando el catálogo...'):
                try:
                    url = 'http://127.0.0.1:5000/recommend'
                    response = requests.post(url, json={'user_id': user_id_top})
                    response.raise_for_status()
                    
                    datos = response.json()
                    top_10_list = datos['top_10']
                    
                    st.success(f"¡Top 10 generado para el usuario {user_id_top}!")
                    
                    # Convertimos la lista de diccionarios en un DataFrame de Pandas para que Streamlit lo dibuje como una tabla interactiva
                    df_top10 = pd.DataFrame(top_10_list)
                    
                    # Añadimos una columna de "Ranking" del 1 al 10
                    df_top10.index = range(1, 11)
                    
                    st.dataframe(df_top10, use_container_width=True)
                    st.balloons() # ¡Un toque visual de celebración!
                    
                except Exception as e:
                    st.error(f"Error conectando al servidor: {e}")
        else:
            st.warning("Introduce un ID de usuario válido.")
