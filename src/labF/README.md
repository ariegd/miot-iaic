---

**Asunto: Propuesta de Proyecto \- Sistema AIoT de Gestión de Aforo y Ruteo Dinámico en Transporte Urbano**  
Hola a todos,  
A continuación, presentamos la propuesta de proyecto final para nuestro grupo:  
**1\. Descripción del problema:**  
Nuestro proyecto abordará un problema de clasificación y regresión dentro del ámbito del transporte urbano inteligente (Smart Mobility / AIoT). El objetivo es desarrollar un sistema capaz de predecir el nivel de aforo en tiempo real. La finalidad de negocio del modelo será ayudar a un sistema central a tomar decisiones de ruteo dinámico (ej .clasificación\[Vacío, Medio, Lleno\],  saltar paradas si el aforo es máximo o enviar vehículos de refuerzo).  
**2\. Naturaleza Multimodal y Datasets:**  
Para cumplir con los requisitos de la asignatura, abordaremos el problema de forma multimodal utilizando dos datasets de naturaleza distinta obtenidos de Kaggle:

* **Dataset 1 (Imágenes \- Visión por Computador):** Utilizaremos un dataset de conteo de multitudes en cámaras de seguridad (ej. *Crowd Counting Dataset* de Kaggle). Estos datos simularán las cámaras IoT del interior del vehículo. Los modelos aplicados a este dataset clasificará el nivel de ocupación visual.  
* **Dataset 2 (Tabular \- Telemetría y Entorno):** Utilizaremos un dataset de registros de tránsito (ej. *Public Transport Delays and Traffic* de Kaggle) que contiene variables como el índice de congestión del tráfico, condiciones meteorológicas, hora del día y tipo de vehículo. Los modelos aplicados aquí predecir la probabilidad de saturación de la ruta basándose en el contexto del sensor y el entorno.

**3\. Aplicación de Explicabilidad (XAI):**

* Para los modelos de imágenes, utilizaremos técnicas como Grad-CAM para visualizar en qué zonas del fotograma (cabezas, pasillo) se está fijando el modelo para determinar el aforo.  
* Para los modelos tabulares, aplicaremos técnicas como SHAP para entender qué peso tienen variables como la "hora punta" o la "lluvia" a la hora de predecir el colapso de la ruta.

---

