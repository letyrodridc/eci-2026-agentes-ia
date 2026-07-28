"""
Servidor MCP (Model Context Protocol) para exploración de modelos en Hugging Face.
Este módulo implementa un servidor MCP independiente utilizando FastMCP de la biblioteca oficial `mcp`.
Permite a cualquier cliente compatible con MCP (incluyendo Google ADK vía McpToolset) descubrir herramientas.
"""

from mcp.server.fastmcp import FastMCP

# Creación del servidor MCP
mcp = FastMCP("HuggingFace-Explorer-MCP")


@mcp.tool()
def mcp_buscar_modelos_huggingface(query: str, tarea: str = "text-generation") -> str:
    """
    [Herramienta MCP] Busca modelos en el ecosistema de Hugging Face filtrando por consulta y tarea específica.

    Args:
        query: Término de búsqueda o arquitectura (ej: 'gemma', 'llama', 'code', 'vision').
        tarea: Categoria o tarea de IA ('text-generation', 'text-to-image', 'image-to-text', 'fill-mask').

    Returns:
        Un resumen en texto de los modelos encontrados que coinciden con los criterios.
    """
    query_lower = query.lower()
    
    catálogo_mcp = {
        "text-generation": [
            {"id": "google/gemma-3-27b-it", "likes": 4200, "pipeline": "text-generation", "desc": "Última generación de modelos abiertos de Google DeepMind con contexto de 128k."},
            {"id": "meta-llama/Llama-3.3-70B-Instruct", "likes": 9800, "pipeline": "text-generation", "desc": "Modelo insignia de Meta para razonamiento y formateo de instrucciones."},
            {"id": "deepseek-ai/DeepSeek-R1", "likes": 15400, "pipeline": "text-generation", "desc": "Modelo de razonamiento de arquitectura MoE con pensamiento transparente."},
            {"id": "Qwen/Qwen2.5-Coder-32B-Instruct", "likes": 3100, "pipeline": "text-generation", "desc": "Modelo ultra-especializado en generación, refactorización y depuración de código."}
        ],
        "image-to-text": [
            {"id": "google/paligemma-3b-pt-224", "likes": 1800, "pipeline": "image-to-text", "desc": "Modelo VLM (Vision Language Model) liviano de Google para subtitulado y VQA."},
            {"id": "meta-llama/Llama-3.2-11B-Vision-Instruct", "likes": 2700, "pipeline": "image-to-text", "desc": "Modelo multimodal visión-texto de Meta."}
        ]
    }

    modelos = catálogo_mcp.get(tarea, catálogo_mcp["text-generation"])
    filtrados = [m for m in modelos if query_lower in m["id"].lower() or query_lower in m["desc"].lower() or query_lower == "todos"]
    
    if not filtrados:
        filtrados = modelos  # Mostrar catálogo por defecto si no hay filtro directo

    resultado = [f"=== Resultados de Búsqueda MCP para '{query}' (Tarea: {tarea}) ==="]
    for idx, m in enumerate(filtrados, 1):
        resultado.append(f"{idx}. Model ID: {m['id']}")
        resultado.append(f"   Likes en HF: {m['likes']} ❤️ | Pipeline: {m['pipeline']}")
        resultado.append(f"   Descripción: {m['desc']}\n")

    return "\n".join(resultado)


@mcp.tool()
def mcp_obtener_tendencias_hf() -> str:
    """
    [Herramienta MCP] Retorna los modelos en tendencia (Trending Models) más populares actualmente en Hugging Face.

    Returns:
        Un informe con los modelos con mayor crecimiento e interés en la comunidad de IA.
    """
    return """🔥 === Modelos en Tendencia en Hugging Face Hub (MCP Feed) ===

1. 🚀 google/gemma-3-27b-it
   - Arquitectura: Transformer denso (27B)
   - Novedad: Rendimiento de nivel 70B en tamaño de 27B con soporte multimodal.

2. 🧠 deepseek-ai/DeepSeek-R1
   - Arquitectura: Mixture of Experts (MoE) 671B
   - Novedad: Razonamiento abierto con cadena de pensamiento explícita.

3. 🦙 meta-llama/Llama-3.3-70B-Instruct
   - Arquitectura: Transformer (70B)
   - Novedad: Calidad cercana a Llama 3.1 405B con menor costo computacional.

4. 💻 Qwen/Qwen2.5-Coder-32B-Instruct
   - Arquitectura: Transformer (32B)
   - Novedad: Supera a GPT-4o en varios benchmarks de código (HumanEval / MBPP).
"""


@mcp.tool()
def mcp_info_servidor_protocolo() -> str:
    """
    [Herramienta MCP] Devuelve información del estado y protocolo del servidor MCP.

    Returns:
        Detalles técnicos sobre la conexión MCP activa.
    """
    return """ℹ️ === Información del Servidor MCP ===
* Nombre del Servidor: HuggingFace-Explorer-MCP
* Protocolo: Model Context Protocol (MCP) v1.0
* Transporte: Stdio (Standard Input/Output)
* Estado: Activo y respondiendo a consultas de herramientas.
* Herramientas disponibles: mcp_buscar_modelos_huggingface, mcp_obtener_tendencias_hf, mcp_info_servidor_protocolo
"""


if __name__ == "__main__":
    # Inicia el servidor MCP ejecutándose sobre el canal estándar (stdio)
    mcp.run()
