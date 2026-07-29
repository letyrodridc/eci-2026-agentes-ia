import uvicorn
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Cargar variables de entorno (como GOOGLE_API_KEY) desde el archivo .env
load_dotenv()

instruction = """
Eres el Experto en Google ADK (Agent Development Kit).
Tu objetivo es explicar de forma clara y didáctica qué es Google ADK y cuáles son 
los patrones principales para construir agentes.

Cuando te pregunten sobre ADK o patrones de agentes, debes explicar los siguientes:
1. Agentes de Flujo Único (Single/Sequential Agent): Un solo agente o una cadena simple.
2. Patrón de Supervisor-Trabajador (Supervisor-Worker): Un agente orquestador delega tareas a sub-agentes especializados.
3. Herramientas (Tools): Integración de llamadas a funciones locales (Function Calling).
4. Model Context Protocol (MCP): Integración con servidores MCP para acceder a herramientas y recursos externos de forma estandarizada.
5. Agent-to-Agent (A2A): Comunicación estructurada entre agentes independientes usando AgentCards y un formato estándar de mensajes.

Responde siempre en español, con un tono profesional pero amigable, y utiliza viñetas o listas para organizar la información si es pertinente.
"""

# 1. Definimos el Agente experto en ADK
agente_adk = Agent(
    model="gemini-2.5-flash",
    name="ExpertoADK",
    description="Agente especializado en explicar Google ADK y sus patrones de diseño",
    instruction=instruction
)

# 2. Utilizamos to_a2a nativo del ADK para convertirlo en una app ASGI/Starlette
app = to_a2a(agente_adk, host="127.0.0.1", port=8002)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Iniciando el Agente Experto en ADK con to_a2a()")
    print("📍 URL de la AgentCard: http://127.0.0.1:8002/.well-known/agent.json")
    print("📩 Endpoint de mensajes: http://127.0.0.1:8002/a2a/v1/message")
    print("=" * 60)
    
    # 3. Ejecutamos la app con uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
