# chat_router.py
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from travel_agent_api.services.agent_service import Agent

# Creazione di un nuovo router FastAPI
router = APIRouter()


# Definizione del modello di dati per la richiesta di chat
class ChatCompletionRequest(BaseModel):
    # Il campo messages conterrà la lista dei messaggi che compongono la conversazione
    messages: list

    # Esempio mostrato nella schermata di test in /docs
    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Vorrei organizzare un viaggio a Roma",
                    }
                ]
            }
        }
    }


# Alias per retrocompatibilità con il nome originale delle slide
ChatComplentionRequest = ChatCompletionRequest


@router.post("/travel-agent")
def chat_completion(request: ChatCompletionRequest):
    """
    Endpoint per la gestione delle richieste di chat.
    Processa i messaggi ricevuti e restituisce una risposta dall'agente di viaggio.

    Args:
        request (ChatCompletionRequest): La richiesta contenente i messaggi della
            conversazione.

    Returns:
        list: La lista dei messaggi elaborati dall'agente di viaggio.

    Raises:
        HTTPException: In caso di errori durante l'elaborazione della richiesta.
    """
    print("=" * 80)
    print(f"[TRACE][Router] POST /chat/travel-agent | Messaggi ricevuti: {len(request.messages)}")
    if request.messages:
        last_msg = request.messages[-1]
        preview = str(last_msg.get("content", ""))[:100]
        print(f"[TRACE][Router] Ultimo messaggio ({last_msg.get('type', last_msg.get('role', 'unknown'))}): '{preview}'")

    start_time = time.perf_counter()
    try:
        agent = Agent()
        response = agent.run(messages=request.messages)
    except Exception as exc:
        print(f"[TRACE][Router][ERRORE] Eccezione durante l'elaborazione: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    elapsed = time.perf_counter() - start_time
    print(f"[TRACE][Router] Risposta restituita in {elapsed:.2f}s")
    print("=" * 80)

    return response
