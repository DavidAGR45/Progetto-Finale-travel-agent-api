# Questa riga importa la classe FastAPI dal framework FastAPI. È l'elemento principale necessario per creare un'applicazione web API.
from fastapi import FastAPI

# Qui viene importato un router chiamato `chat_router` da un modulo locale (file)
# `app.routes`. I router in FastAPI sono utilizzati per organizzare le diverse route (endpoint)
# dell'API in modo modulare.
from travel_agent_api.routes import chat_router

# Questa riga importa il middleware CORS (Cross-Origin Resource Sharing). 
# CORS è un meccanismo di sicurezza che consente o blocca le richieste da domini diversi da quello dell'API.
from fastapi.middleware.cors import CORSMiddleware

# Qui viene creata un'istanza dell'applicazione FastAPI. Questo oggetto `app` sarà il punto
# principale dell'applicazione dove verranno registrate tutte le route e i middleware.
app = FastAPI()

origins = [
    "http://127.0.0.1:8000",  # Porta standard dell'applicazione front-end Laravel
    "http://localhost:8000",  # Alias per localhost e porta standard dell'applicazione front-end Laravel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Domini permessi
    allow_credentials=True,     # Permette l'invio di credenziali
    allow_methods=["*"],        # Permette tutti i metodi HTTP
    allow_headers=["*"],        # Permette tutti gli headers
)

app.include_router(
    chat_router.router,   # Il router definito in chat_router.py
    tags=["Chat"],        # Tag per la documentazione Swagger
    prefix="/chat",       # Prefisso per tutte le route del router
)
