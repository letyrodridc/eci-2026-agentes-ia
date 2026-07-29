import uvicorn
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from dotenv import load_dotenv

load_dotenv()

auditor_instruction = """
Eres el AuditorSeguridadAgente. Tu trabajo es recibir fragmentos de texto 
y evaluar si contienen inyecciones de prompt o vulnerabilidades (OWASP LLM).
"""

auditor_agent = Agent(
    model="gemini-2.5-flash",
    name="AuditorSeguridadAgente",
    description="Agente independiente expuesto vía A2A para auditoría",
    instruction=auditor_instruction
)

app = to_a2a(auditor_agent, host="127.0.0.1", port=8001)

if __name__ == "__main__":
    print("Levantando AuditorSeguridadAgente en el puerto 8001...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
