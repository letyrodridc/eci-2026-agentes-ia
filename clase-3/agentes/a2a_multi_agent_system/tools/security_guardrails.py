"""
=============================================================================
ECI 2026 - UBA | Clase 3: Herramientas de Seguridad y Guardrails para Agentes
=============================================================================
"""
import re

def evaluar_seguridad_prompt(prompt_texto: str) -> str:
    """Evalúa un prompt buscando inyecciones y vulnerabilidades comunes."""
    patrones = ["ignore all previous", "system prompt", "bypass", "jailbreak", "dan", "forget everything"]
    for p in patrones:
        if p in prompt_texto.lower():
            return f"ALERTA (OWASP LLM01): Posible inyección de prompt detectada (patrón: {p})"
    return "SEGURO: No se detectaron patrones maliciosos evidentes."

def sanitizar_entrada_pii(texto: str) -> str:
    """Enmascara PII básico como correos electrónicos y teléfonos antes de procesar."""
    # Enmascarar correos
    texto = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL PROTEGIDO]', texto)
    # Enmascarar teléfonos (muy básico)
    texto = re.sub(r'\+?\d{8,15}', '[TELÉFONO PROTEGIDO]', texto)
    return texto
