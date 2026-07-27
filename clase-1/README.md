# Clase 1 - Introducción a Agentes y Prompt Engineering

Esta carpeta contiene los materiales para la primera clase del curso **ECI 2026 - Construyendo Agentes de Inteligencia Artificial (UBA)**.

Impartido por **Leticia L. Rodriguez** | [teg-consulting.ai](https://teg-consulting.ai)

## 📂 Contenido

- **`ECI 2026 - Agentes de IA - Clase 1.pdf`**: Diapositivas de la clase teórica donde introducimos el concepto de agentes, modelos fundacionales y estrategias de prompting.
- **`notebooks/`**:
  - `clase-1-1-prompt-engineering.ipynb`: Notebook práctico con ejercicios paso a paso sobre Prompt Engineering (zero-shot, few-shot, chain-of-thought, etc). *(Las celdas de output han sido limpiadas para que puedas resolver los ejercicios)*.
- **`agentes/`**:
  - `eci_curso_agente/`: Nuestro primer agente construido con Google ADK. Es un Asistente de Voz configurado para responder dudas sobre el cronograma y modalidad del curso utilizando `gemini-3.1-flash-live-preview`.

## 🚀 Cómo usar este material

1. **Notebooks**: Abre los notebooks utilizando Jupyter o Google Colab. Recuerda configurar tu API Key de Gemini en tu entorno.
2. **Agente Asistente**: Ve al directorio del agente y ejecútalo mediante terminal o web, según las instrucciones generales del curso:
   ```bash
   cd agentes/eci_curso_agente
   # Configura tu archivo .env antes de ejecutar
   adk web .
   ```
