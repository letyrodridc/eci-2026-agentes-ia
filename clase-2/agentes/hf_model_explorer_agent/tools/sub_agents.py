"""
Sub-agentes como Herramientas (Agent as a Tool) para Google ADK.
Demuestra la delegación modular de tareas complejas (como generación de código) a sub-agentes
especializados envueltos en `AgentTool`.
"""

from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool

# Instrucción detallada para el sub-agente especialista en código
INSTRUCCION_CODIGO_EXPERTO = """
Eres un desarrollador experto en Python especializado en LLMs, Hugging Face `transformers`, `huggingface_hub`, `ollama` y SDKs oficiales (`google-genai`, `anthropic`).

Tu única tarea es generar ejemplos de código Python limpios, completos, comentados y listos para ejecutar cuando el usuario pida saber cómo usar un modelo específico.

Dependiendo del modelo solicitado:
1. Para modelos de Hugging Face u Open-Weights (ej: Gemma, Llama 3, DeepSeek, Qwen):
   - Proporciona un ejemplo usando `pipeline` o `AutoModelForCausalLM` de `transformers` (con `device_map="auto"` y `torch.bfloat16`).
   - Opcionalmente brinda el comando para ejecutarlo localmente vía `ollama run <modelo>`.

2. Para modelos propietarios vía API (ej: Gemini 2.5/3, Claude 3.5/3.7):
   - Proporciona el código utilizando la biblioteca cliente oficial (`google-genai` para Gemini o `anthropic` para Claude).

Asegúrate de incluir comentarios explicativos sobre la instalación de dependencias (`pip install transformers torch`, etc.) y el manejo seguro de claves de API.
"""

# Creación del sub-agente especialista
codigo_experto_agent = Agent(
    model="gemini-2.5-flash",
    name="codigo_experto_subagent",
    description="Sub-agente especializado en generar código Python completo y limpio para inferencia con Transformers, Ollama, Gemini SDK y Anthropic SDK.",
    instruction=INSTRUCCION_CODIGO_EXPERTO
)

# Envoltorio del sub-agente como Tool utilizable por el agente principal
codigo_experto_tool = AgentTool(agent=codigo_experto_agent)
