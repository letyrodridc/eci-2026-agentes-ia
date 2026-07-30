# ECI 2026 - Clase 4: Agentes RAG (Retrieval-Augmented Generation)

Bienvenido a la **Clase 4** del curso *"Construyendo Agentes de Inteligencia Artificial"* de la **Escuela de Ciencias Informáticas (ECI 2026 - UBA)**.

---

## 🎯 Objetivos de la Clase

1. **Entender RAG**: Comprender conceptualmente cómo funciona el paradigma Retrieval-Augmented Generation.
2. **Bases Vectoriales locales**: Aprender a generar embeddings de texto y almacenarlos en **FAISS**.
3. **Integración con Agentes**: Desarrollar un agente utilizando **Google ADK** capaz de buscar contexto en la base de datos vectorial para responder de forma precisa.

---

## 🤖 El Agente: RAG Attention Agent (`rag_agent`)

Este agente tiene como objetivo demostrar un flujo de RAG puro en Python. Se alimenta de extractos del famoso paper *"Attention Is All You Need"*. Utiliza `text-embedding-004` para los embeddings, `FAISS` para la indexación y búsqueda rápida local, y se orquesta a través de **Google ADK**.

---

## 🖼️ Diagrama de Arquitectura del Agente

![Arquitectura del Agente de Clase 4](arquitectura_agente.png)

---

## 🏗️ Arquitectura del Proyecto

```text
clase-4/
├── README.md                          # La extracción de texto del `.pdf` usando `pypdf` y el *chunking*.
├── requirements.txt                   # Dependencias (google-adk, faiss, google-genai, pypdf)
├── arquitectura_agente.png            # Diagrama explicativo en formato PNG
└── rag_agent/                         # Módulo principal del agente en Google ADK
    ├── .env                           # Configuración de variables de entorno (API Key)
    ├── agent.py                       # Definición de root_agent y lógica RAG
    └── data/
        └── attention.pdf              # Base de conocimiento (Paper completo)
```

---

## 🛠️ Implementación de las Herramientas (Tools)

### 1. Function Calling (RAG)
* `consultar_paper_attention(pregunta: str)`: Esta función encapsula todo el proceso de Retrieval. Toma la pregunta del usuario, la vectoriza, busca en el índice local de **FAISS** los *chunks* de texto más similares, y finalmente llama a `gemini-2.5-flash` inyectando esos extractos en el prompt para asegurar una respuesta fundamentada. El agente de Google ADK tiene acceso a esta herramienta.

---

## 📦 Instalación de Dependencias

Ejecuta desde la raíz del directorio `agents/`:
```bash
pip install -r clase-4/requirements.txt
```

---

## 🔑 Configuración

Configura la clave de API de Gemini en el archivo `.env` del agente:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=tu_clave_api_aqui
```

---

## 🚀 Cómo Ejecutar el Agente

Ejecuta el agente mediante la CLI oficial de **Google ADK**:

### 1. Modo Interactivo en Terminal (CLI)
```bash
adk run clase-4/rag_agent
```

### 2. Interfaz Web (Browser GUI)
```bash
adk web clase-4/rag_agent
```
Luego navega a `http://localhost:8000`.

### 3. Ejemplos de Consultas para Probar el Agente

* 📌 **Probar RAG (Retrieval-Augmented Generation)**:
  > *"¿Qué tipo de arquitectura de red proponen en el documento en lugar de usar redes recurrentes?"*
  
* 📌 **Probar RAG (Atención)**:
  > *"¿Por qué dicen que la atención es útil en modelos de transducción?"*
