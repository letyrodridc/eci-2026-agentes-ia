"""
=============================================================================
ECI 2026 - UBA | Clase 2: Herramientas (Tools) y Model Context Protocol (MCP)
=============================================================================
Agente Explorador de Modelos de Inteligencia Artificial desarrollado con Google ADK.

Este agente integra de forma didáctica los 3 paradigmas principales de Herramientas:
 1. Llamada a Función (Function Calling): Funciones nativas de Python para especificaciones y VRAM.
 2. Protocolo de Contexto de Modelo (MCP): Servidor MCP FastMCP conectado a través de `McpToolset`.
 3. Agente como Herramienta (Agent as a Tool): Delegación a un sub-agente especializado en código.
"""

import os
import sys
from dotenv import load_dotenv

# Carga de variables de entorno (.env) del agente o del directorio raíz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))
load_dotenv(os.path.join(BASE_DIR, "..", "..", ".env"))

from google.adk.agents.llm_agent import Agent
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioConnectionParams, StdioServerParameters

# Importación de herramientas con fallback para módulo local y ejecución directa
try:
    from .tools.function_tools import (
        obtener_especificaciones_modelo,
        comparar_modelos,
        calcular_vram_requerida,
    )
    from .tools.sub_agents import codigo_experto_tool
except ImportError:
    from tools.function_tools import (
        obtener_especificaciones_modelo,
        comparar_modelos,
        calcular_vram_requerida,
    )
    from tools.sub_agents import codigo_experto_tool

# Configuración del servidor MCP independiente
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MCP_SERVER_PATH = os.path.join(BASE_DIR, "tools", "mcp_server.py")

# Conexión MCP utilizando el ejecutable actual de Python y Stdio
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[MCP_SERVER_PATH]
        )
    )
)

# Instrucciones del sistema para el agente principal
instruction = """
Eres el Asistente Educativo de la Clase 2 del curso "Construyendo Agentes de IA" (ECI 2026 - UBA).
Tu objetivo es ayudar a los estudiantes y profesores a explorar los modelos de lenguaje más populares (Gemma 3, Llama 3.3, Gemini 2.5/3, Claude 3.7, DeepSeek-R1, Qwen 2.5, etc.), entender sus especificaciones técnicas y aprender a utilizarlos en código.

Para cumplir tu objetivo, cuentas con tres familias de herramientas (Tools) integradas mediante Google ADK:

1. **Llamadas a Funciones de Python (Function Calling Tools)**:
   - `obtener_especificaciones_modelo`: Consulta detalles técnicos, contexto, VRAM requerida y licencia de un modelo.
   - `comparar_modelos`: Compara dos modelos lado a lado.
   - `calcular_vram_requerida`: Estima la memoria GPU necesaria para inferir un modelo localmente.

2. **Model Context Protocol (Herramientas MCP)**:
   - Conectadas mediante `McpToolset` a un servidor MCP independiente (`HuggingFace-Explorer-MCP`).
   - Puedes buscar modelos en el hub de Hugging Face y obtener las últimas tendencias (trending models).

3. **Sub-agente como Herramienta (AgentTool)**:
   - `codigo_experto_subagent`: Sub-agente especialista al que puedes delegar la generación de código Python (Transformers, Ollama, Google GenAI SDK, Anthropic SDK) cuando el usuario pida ejemplos prácticos de uso.

Pautas de respuesta:
- Sé didáctico, amable y riguroso en tus explicaciones.
- Cuando un usuario pregunte por un modelo, utiliza tus herramientas para obtener las especificaciones exactas antes de responder.
- Si el usuario pide ejemplos de código, delega la tarea a tu sub-agente de código para ofrecer ejemplos profesionales y listos para ejecutar.
- Si el usuario pregunta cómo están implementadas las herramientas en esta clase, explica con claridad la diferencia entre Function Calling, MCP y AgentTool en Google ADK.
"""

# Agente Principal exportado como root_agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="hf_model_explorer_agent",
    description="Agente educativo para la Clase 2 de ECI UBA 2026. Permite explorar modelos de IA (Gemma, Llama, Gemini, Claude, DeepSeek) usando llamadas a funciones, protocolo MCP y sub-agentes.",
    instruction=instruction,
    tools=[
        obtener_especificaciones_modelo,
        comparar_modelos,
        calcular_vram_requerida,
        mcp_toolset,
        codigo_experto_tool
    ]
)
