import os
import faiss
import numpy as np
from dotenv import load_dotenv
from google.genai import Client

# Asumimos que google_adk provee la clase Agent según la estructura del curso
from google_adk import Agent 

# ---------------------------------------------------------
# 1. CONFIGURACIÓN INICIAL
# ---------------------------------------------------------
load_dotenv()
client = Client()

# ---------------------------------------------------------
# 2. PREPARACIÓN DE DATOS (CHUNKING)
# ---------------------------------------------------------
from pypdf import PdfReader

def load_and_chunk_text(filepath, chunk_size=1000, overlap=200):
    """Lee el texto de un PDF y lo divide en chunks superpuestos."""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    
    chunks = []
    # Iteramos sobre el texto dando saltos de (chunk_size - overlap)
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# ---------------------------------------------------------
# 3. GENERACIÓN DE EMBEDDINGS
# ---------------------------------------------------------
def get_embeddings(texts):
    """Obtiene los embeddings usando text-embedding-004 de Google GenAI."""
    embeddings = []
    for text in texts:
        response = client.models.embed_content(
            model='text-embedding-004',
            contents=text,
        )
        # Extraemos los valores del vector
        embeddings.append(response.embeddings[0].values)
    return np.array(embeddings).astype('float32')

# ---------------------------------------------------------
# 4. CONSTRUCCIÓN DEL ÍNDICE FAISS
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'data', 'attention.pdf')

print("Cargando y procesando el paper...")
chunks = load_and_chunk_text(data_path)

print("Generando embeddings para los fragmentos de texto...")
chunk_embeddings = get_embeddings(chunks)
dimension = chunk_embeddings.shape[1]

print("Indexando vectores en FAISS...")
# Usamos IndexFlatL2 (distancia euclidiana) que es rápido y exacto
index = faiss.IndexFlatL2(dimension)
index.add(chunk_embeddings)
print(f"✅ Índice FAISS creado. Total de chunks indexados: {index.ntotal}")

# ---------------------------------------------------------
# 5. LÓGICA DE RECUPERACIÓN (RETRIEVER)
# ---------------------------------------------------------
def retrieve_context(query: str, k: int = 2) -> str:
    """Busca en FAISS los 'k' chunks más relevantes para la query."""
    print(f"Buscando contexto para la pregunta: '{query}'")
    
    # 1. Calculamos el embedding de la pregunta
    query_embedding = get_embeddings([query])
    
    # 2. Buscamos en FAISS los K vecinos más cercanos
    distances, indices = index.search(query_embedding, k)
    
    # 3. Recuperamos el texto original asociado a los índices devueltos
    retrieved_texts = [chunks[i] for i in indices[0]]
    
    # Unimos los fragmentos recuperados
    return "\n...\n".join(retrieved_texts)

# ---------------------------------------------------------
# 6. FUNCIÓN HERRAMIENTA RAG PARA EL AGENTE
# ---------------------------------------------------------
def consultar_paper_attention(pregunta: str) -> str:
    """
    Herramienta que recupera contexto del paper 'Attention Is All You Need' 
    y formula una respuesta basada en él.
    """
    # Recuperamos el contexto
    contexto = retrieve_context(pregunta)
    
    # Construimos el prompt inyectando el contexto
    prompt_final = f"""
    Eres un asistente experto en Inteligencia Artificial y arquitecturas de Redes Neuronales.
    Responde a la pregunta del usuario utilizando ÚNICAMENTE el siguiente contexto técnico:
    
    <contexto>
    {contexto}
    </contexto>
    
    Pregunta: {pregunta}
    
    Si el contexto no contiene la información para responder la pregunta, 
    di amablemente que no tienes la información en el documento.
    """
    
    # Generamos la respuesta con Gemini
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_final,
    )
    return response.text

# ---------------------------------------------------------
# 7. DEFINICIÓN DEL AGENTE (Google ADK)
# ---------------------------------------------------------
root_agent = Agent(
    name="RAG_Attention_Agent",
    description="Agente especializado en el paper Attention Is All You Need usando RAG y FAISS.",
    instructions="""
    Eres un asistente académico. Siempre que el usuario te pregunte algo sobre Transformers, 
    Atención o el paper 'Attention Is All You Need', utiliza la herramienta `consultar_paper_attention` 
    para buscar en la base de conocimientos antes de responder.
    """,
    tools=[consultar_paper_attention]
)
