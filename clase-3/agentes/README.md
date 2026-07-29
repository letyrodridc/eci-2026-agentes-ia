# ECI 2026 - Clase 3: Comunicación Agente a Agente (A2A)

Bienvenido a la **Clase 3** del curso *"Construyendo Agentes de Inteligencia Artificial"* de la **Escuela de Ciencias Informáticas (ECI 2026 - UBA)**.

---

## 🎯 Objetivos de la Clase

1. **Protocolo Agent-to-Agent (A2A)**: Aprender a exponer de manera sencilla un agente de Google ADK mediante A2A.
2. **Uso de `to_a2a`**: Convertir un agente en una aplicación ASGI/Starlette para servirla mediante un servidor web (`uvicorn`).
3. **Exploración de Patrones de ADK**: Proveer un agente experto para dialogar sobre los distintos patrones de construcción de agentes (Supervisor-Trabajador, Tools, MCP, A2A, etc).

---

## 🤖 El Agente: Experto en Google ADK

El archivo `demo_simple_to_a2a.py` define un agente cuyo objetivo es explicar de forma clara qué es Google ADK y cuáles son los patrones principales para construir agentes.

Este agente utiliza la función nativa `to_a2a` del SDK para exponer una API A2A:
- **AgentCard**: Metadata y endpoints del agente expuestos de manera estandarizada.
- **Endpoint de Mensajes**: Un endpoint POST diseñado para recibir mensajes bajo el estándar A2A.

---

## 🏗️ Arquitectura del Proyecto

```text
clase-3/
├── README.md                      # Documentación explicativa de la Clase 3
├── requirements.txt               # Dependencias (google-adk, a2a, uvicorn, etc.)
└── a2a_simple_cliente_servidor/
    ├── demo_simple_to_a2a.py      # Script principal: Servidor A2A
    └── demo_consumir_a2a.py       # Script cliente: Cómo consumir un agente A2A
```

---

## 📦 Instalación de Dependencias

Ejecuta desde el directorio raíz `agents/`:
```bash
pip install -r clase-3/requirements.txt
```

---

## 🔑 Configuración

Asegúrate de contar con tu clave de API de Gemini configurada. Puedes exportarla como variable de entorno o crear un archivo `.env`:

```bash
export GOOGLE_API_KEY="tu_clave_api_aqui"
```

---

## 🚀 Cómo Ejecutar la Demostración

Para levantar este agente como un servidor A2A y luego consumirlo, sigue estos pasos:

### 1. Iniciar el Agente Servidor

En una terminal, ejecuta:

```bash
python clase-3/a2a_simple_cliente_servidor/demo_simple_to_a2a.py
```

Al hacerlo, `uvicorn` iniciará un servidor web en el puerto `8002`. Podrás inspeccionar:
- **AgentCard**: `http://127.0.0.1:8002/.well-known/agent.json`
- **Endpoint A2A**: `http://127.0.0.1:8002/a2a/v1/message`

### 2. Consumir el Agente (Cliente)

En otra terminal, corre el script cliente que se conectará al servidor A2A y enviará una consulta (basado en el [quickstart-consuming](https://adk.dev/a2a/quickstart-consuming/) de ADK):

```bash
python clase-3/a2a_simple_cliente_servidor/demo_consumir_a2a.py
```

El script descargará la AgentCard pública y luego hará una petición HTTP POST al endpoint de mensajes del agente, mostrando su respuesta por consola.
