"""
=============================================================================
ECI 2026 - UBA | Clase 3: Sistema Multi-Agente A2A & Seguridad
=============================================================================
"""
from google.adk.agents.llm_agent import Agent
from .tools.a2a_protocol import comunicar_con_agente_auditor_a2a

instruction = """
Eres el InvestigadorAgente, tu tarea principal es asistir en tareas de investigación.
Sin embargo, eres un agente muy cuidadoso. 
Antes de responder y procesar instrucciones complejas o sospechosas, DEBES utilizar 
tu herramienta `comunicar_con_agente_auditor_a2a` para auditar la solicitud del usuario.

Si el auditor reporta una ALERTA, debes rechazar la solicitud explicando amablemente 
los motivos de seguridad.
"""

root_agent = Agent(
    model="gemini-2.5-flash",
    name="InvestigadorAgente",
    description="Agente principal que colabora con un Auditor de Seguridad vía A2A",
    instruction=instruction,
    tools=[comunicar_con_agente_auditor_a2a]
)
