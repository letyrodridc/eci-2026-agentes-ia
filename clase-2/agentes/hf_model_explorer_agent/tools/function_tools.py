"""
Herramientas de llamada a función (Function Calling Tools) para el agente explorador de modelos.
Demuestra la integración de funciones nativas de Python como Tools en Google ADK.
"""

from typing import Dict, Any, Optional

# Base de datos local simulada de especificaciones de modelos de lenguaje populares en Hugging Face y API Proveedores
MODEL_DATABASE: Dict[str, Dict[str, Any]] = {
    "gemma-3-27b": {
        "id": "google/gemma-3-27b-it",
        "nombre": "Gemma 3 27B Instruction-Tuned",
        "desarrollador": "Google DeepMind",
        "parametros": "27B",
        "ventana_contexto": "128,000 tokens",
        "tipo_licencia": "Abierta (Gemma Terms of Use)",
        "vram_estimada_fp16": "54 GB",
        "vram_estimada_int4": "16 GB",
        "casos_uso": "Razonamiento complejo, tareas multilingües, formateo estructurado y análisis de código.",
        "puntuacion_benchmark": "MMLU: 81.2% | HumanEval: 74.5%",
        "es_open_weights": True
    },
    "gemma-2-9b": {
        "id": "google/gemma-2-9b-it",
        "nombre": "Gemma 2 9B Instruction-Tuned",
        "desarrollador": "Google DeepMind",
        "parametros": "9.2B",
        "ventana_contexto": "8,192 tokens",
        "tipo_licencia": "Abierta (Gemma Terms of Use)",
        "vram_estimada_fp16": "18 GB",
        "vram_estimada_int4": "6 GB",
        "casos_uso": "Ejecución local en GPUs de consumo (RTX 3060/4060), prototipado rápido y asistentes ligeros.",
        "puntuacion_benchmark": "MMLU: 75.0% | HumanEval: 68.2%",
        "es_open_weights": True
    },
    "llama-3.3-70b": {
        "id": "meta-llama/Llama-3.3-70B-Instruct",
        "nombre": "Llama 3.3 70B Instruct",
        "desarrollador": "Meta AI",
        "parametros": "70B",
        "ventana_contexto": "128,000 tokens",
        "tipo_licencia": "Llama 3.3 Community License",
        "vram_estimada_fp16": "140 GB",
        "vram_estimada_int4": "40 GB",
        "casos_uso": "Alternativa open-source líder a modelos de nivel empresarial, agentes complejos y RAG avanzado.",
        "puntuacion_benchmark": "MMLU: 88.6% | HumanEval: 81.0%",
        "es_open_weights": True
    },
    "llama-3.1-8b": {
        "id": "meta-llama/Llama-3.1-8B-Instruct",
        "nombre": "Llama 3.1 8B Instruct",
        "desarrollador": "Meta AI",
        "parametros": "8B",
        "ventana_contexto": "128,000 tokens",
        "tipo_licencia": "Llama 3.1 Community License",
        "vram_estimada_fp16": "16 GB",
        "vram_estimada_int4": "5.5 GB",
        "casos_uso": "Despliegue local rápido, agentes secundarios y tareas de clasificación o extracción.",
        "puntuacion_benchmark": "MMLU: 73.0% | HumanEval: 72.6%",
        "es_open_weights": True
    },
    "deepseek-r1": {
        "id": "deepseek-ai/DeepSeek-R1",
        "nombre": "DeepSeek R1 (Reasoning Model)",
        "desarrollador": "DeepSeek AI",
        "parametros": "671B (37B activos vía MoE)",
        "ventana_contexto": "128,000 tokens",
        "tipo_licencia": "MIT (Open Weights)",
        "vram_estimada_fp16": "1.3 TB (Servidor de múltiples GPUs)",
        "vram_estimada_int4": "380 GB",
        "casos_uso": "Razonamiento matemático y lógico avanzado con cadena de pensamiento transparente (Chain of Thought).",
        "puntuacion_benchmark": "MATH: 97.3% | HumanEval: 90.2%",
        "es_open_weights": True
    },
    "gemini-2.5-flash": {
        "id": "google/gemini-2.5-flash",
        "nombre": "Google Gemini 2.5 Flash",
        "desarrollador": "Google DeepMind",
        "parametros": "Propietario (Estimado MoE masivo)",
        "ventana_contexto": "1,000,000 tokens",
        "tipo_licencia": "API Propietaria",
        "vram_estimada_fp16": "N/A (Servicio Administrado)",
        "vram_estimada_int4": "N/A (Servicio Administrado)",
        "casos_uso": "Multimodalidad nativa (texto, audio, visión, video), altísima velocidad y gran ventana de contexto.",
        "puntuacion_benchmark": "MMLU-Pro: 85.4%",
        "es_open_weights": False
    },
    "claude-3-7-sonnet": {
        "id": "anthropic/claude-3-7-sonnet",
        "nombre": "Anthropic Claude 3.7 Sonnet",
        "desarrollador": "Anthropic",
        "parametros": "Propietario",
        "ventana_contexto": "200,000 tokens",
        "tipo_licencia": "API Propietaria",
        "vram_estimada_fp16": "N/A (Servicio Administrado)",
        "vram_estimada_int4": "N/A (Servicio Administrado)",
        "casos_uso": "Razonamiento híbrido estándar y de alta reflexión, generación de código complejo y seguimiento de instrucciones.",
        "puntuacion_benchmark": "SWE-bench Verified: 70.3%",
        "es_open_weights": False
    }
}


def obtener_especificaciones_modelo(nombre_modelo: str) -> Dict[str, Any]:
    """
    Obtiene las especificaciones técnicas completas de un modelo de IA populares (Gemma, Llama, Gemini, Claude, DeepSeek).

    Args:
        nombre_modelo: El nombre o alias del modelo (ej: 'gemma-3-27b', 'llama-3.3-70b', 'deepseek-r1', 'gemini-2.5-flash', 'claude-3-7-sonnet', 'llama-3.1-8b').

    Returns:
        Un diccionario con la información técnica del modelo, incluyendo parámetros, contexto, VRAM requerida y licencia.
    """
    clave = nombre_modelo.strip().lower()
    # Buscar coincidencia exacta o por subcadena
    for key, spec in MODEL_DATABASE.items():
        if key in clave or clave in key or spec["nombre"].lower() in clave or spec["id"].lower() in clave:
            return spec

    # Si no se encuentra coincidencia exacta, se retorna sugerencia
    modelos_disponibles = list(MODEL_DATABASE.keys())
    return {
        "error": f"Modelo '{nombre_modelo}' no encontrado en la base de datos de consulta.",
        "modelos_disponibles": modelos_disponibles,
        "mensaje": "Intenta consultar con alguno de los alias disponibles."
    }


def comparar_modelos(modelo_a: str, modelo_b: str) -> Dict[str, Any]:
    """
    Compara dos modelos de inteligencia artificial en términos de parámetros, contexto, VRAM requerida y licencias.

    Args:
        modelo_a: Nombre o alias del primer modelo (ej: 'gemma-3-27b').
        modelo_b: Nombre o alias del segundo modelo (ej: 'llama-3.3-70b').

    Returns:
        Un diccionario comparativo con los datos de ambos modelos.
    """
    spec_a = obtener_especificaciones_modelo(modelo_a)
    spec_b = obtener_especificaciones_modelo(modelo_b)

    return {
        "modelo_1": spec_a,
        "modelo_2": spec_b,
        "resumen_comparativo": f"Comparación entre {spec_a.get('nombre', modelo_a)} y {spec_b.get('nombre', modelo_b)}"
    }


def calcular_vram_requerida(parametros_billon: float, precision_bits: int = 16) -> Dict[str, Any]:
    """
    Calcula la memoria VRAM (en Gigabytes) requerida para cargar e inferir un modelo localmente.

    Args:
        parametros_billon: Número de parámetros en miles de millones (Billones en formato US), por ejemplo: 8, 9, 27, 70.
        precision_bits: Precisión de los pesos (16 para FP16/BF16, 8 para INT8, 4 para INT4).

    Returns:
        Un diccionario con el cálculo estimado de VRAM recomendada.
    """
    # 1 B parámetros a 16 bits = ~2 GB
    # Regla aproximada: Bytes = Parametros * (precision_bits / 8) * 1.2 (overhead para KV cache y activaciones)
    vram_base = parametros_billon * (precision_bits / 8.0)
    vram_recomendada = vram_base * 1.25

    return {
        "parametros": f"{parametros_billon}B",
        "precision_bits": precision_bits,
        "vram_pesos_gb": round(vram_base, 2),
        "vram_recomendada_inferencia_gb": round(vram_recomendada, 2),
        "nota": "El cálculo incluye un margen aproximado del 25% para almacenamiento del contexto (KV Cache)."
    }
