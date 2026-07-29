# Clase 3 - Frameworks y ADK

Esta carpeta contiene los materiales para la tercera clase del curso **ECI 2026 - Construyendo Agentes de Inteligencia Artificial (UBA)**.

## 📂 Contenido

- **`ECI 2026 - Agentes de IA - Clase 3.pdf`**: Diapositivas de la clase teórica sobre Tool Use, conectando agentes a APIs, y patrones clave de frameworks y Kits de Desarrollo (ADKs).
- **`notebooks/`**:
  - `clase-3-1-seguridad-en-prompts.ipynb`: Notebook práctico enfocado en estrategias de seguridad en los prompts para mitigar ataques y vulnerabilidades comunes en modelos de lenguaje.
- **`agentes/`**:
  - `helloworld_sample/`: Un agente de Google ADK básico (Hello World) para introducir el framework.
  - `a2a_simple_cliente_servidor/`: Ejemplo de interacción simple agente-a-agente (Cliente/Servidor) utilizando Google ADK.
  - `a2a_multi_agent_system/`: Sistema multi-agente más complejo (A2A) desarrollado con Google ADK.
  *(Puedes encontrar más detalles en el README dentro de la carpeta `agentes`)*.

## 🚀 Cómo usar este material

1. **Notebooks**: Puedes abrir el notebook de forma local usando Jupyter Notebook, o subirlo a Google Colab. Recuerda configurar la variable de entorno `GOOGLE_API_KEY` para que las celdas puedan interactuar con la API de Gemini.
2. **Agentes**: Ingresa al directorio del agente que desees explorar y ejecuta el proyecto localmente (recuerda instalar las dependencias previas listadas en `requirements.txt`):
   ```bash
   cd agentes/helloworld_sample
   # Configura las dependencias y tu API Key
   adk run .
   ```
