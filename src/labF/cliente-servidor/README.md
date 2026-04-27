Para construir esta aplicación profesional en un entorno **cliente-servidor**, utilizaremos **Flask** para el servidor (el "Cerebro" que procesa la IA) y un script de **Cliente** que simulará la llegada de los autobuses enviando imágenes reales de tu dataset.

Esta arquitectura separa la computación pesada (la CNN y el Q-Learning) de la interfaz de usuario.

### **Estructura de la Aplicación**

1. **Servidor (IA-Server):** Carga modelo\_cnn.keras y pipeline\_qlearning.joblib. Recibe una imagen, predice el estado y devuelve la decisión de negocio.  
2. **Cliente (Bus-Simulator):** Lee tu CSV, elige una imagen al azar y se la envía al servidor para obtener las instrucciones de ruteo.

---

**3\. Explicación de la Lógica de Aforo**

Para que la App responda correctamente "Vacío, Medio, Lleno", el servidor hace lo siguiente:

1. **Recibe la ruta de la imagen:** El cliente le dice "mira la foto del bus 101".  
2. **Visión Artificial (CNN):** La CNN procesa los píxeles y devuelve un vector de probabilidad, por ejemplo: \[0.1, 0.2, 0.7\]. El argmax nos da el índice 2, que corresponde a **"Lleno"**.  
3. **Lógica de Negocio (Q-Learning):** El servidor consulta la fila 2 de la Q\_table (la fila de "Lleno"). Si la tabla fue entrenada correctamente, el valor más alto estará en la columna de **"Enviar\_Refuerzo"** o **"Saltar\_Parada"**.  
4. **Respuesta:** Devuelve un JSON estructurado que una pantalla en el autobús o en la central de control podría mostrar fácilmente.

### **Instrucciones para probarlo:**

1. Asegúrate de que los archivos modelo\_cnn.keras y pipeline\_qlearning.joblib están en la carpeta /Resultados/.  
2. Ejecuta primero el código del **Servidor**.  
3. Una vez que el servidor diga "Running on...", ejecuta el código del **Cliente**.  
4. Verás en la consola del cliente cómo se toman las decisiones de ruteo dinámico en tiempo real basadas en las fotos reales de tu dataset.
