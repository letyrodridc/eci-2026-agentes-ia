import asyncio
import httpx

async def main():
    server_url = "http://127.0.0.1:8002"
    
    print(f"1. Obteniendo la AgentCard de {server_url}/.well-known/agent.json ...")
    async with httpx.AsyncClient() as client:
        try:
            card_response = await client.get(f"{server_url}/.well-known/agent.json")
            card_response.raise_for_status()
            agent_card = card_response.json()
            print(f"✅ AgentCard obtenida para el agente: {agent_card.get('name', 'Desconocido')}")
            
            # 2. Enviar un mensaje al endpoint A2A (típicamente /a2a/v1/message)
            message_endpoint = f"{server_url}/a2a/v1/message"
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "parts": [{"text": "¿Qué es el patrón Supervisor-Trabajador en ADK?"}]
                    }
                ]
            }
            
            print(f"\n2. Enviando mensaje al agente en {message_endpoint} ...")
            # Nota: usamos un timeout largo porque el modelo puede tardar en responder
            response = await client.post(message_endpoint, json=payload, timeout=60.0)
            response.raise_for_status()
            
            # 3. Procesar la respuesta
            # Dependiendo de si la respuesta es streaming o no, se parsea. 
            # asumiendo respuesta JSON estándar A2A:
            data = response.json()
            print("\n🤖 Respuesta del Agente:")
            for msg in data.get('messages', []):
                if msg.get('role') == 'model':
                    for part in msg.get('parts', []):
                        if 'text' in part:
                            print(part['text'])
                            
        except httpx.ConnectError:
            print(f"❌ Error de conexión: ¿Está corriendo el servidor en {server_url}?")
            print("Asegúrate de ejecutar primero: python clases/clase-3/agentes/a2a_simple_cliente_servidor/demo_simple_to_a2a.py")
        except httpx.HTTPStatusError as e:
            print(f"❌ Error HTTP: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(main())
