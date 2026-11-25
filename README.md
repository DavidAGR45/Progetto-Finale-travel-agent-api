# 🌍 Travel Agent API

Backend REST API per un **Agente di Viaggio Intelligente (Travel Planner Agent)** autonomo, sviluppato con **FastAPI**, **LangChain**, **LangGraph** e **SerpApi**.

L'API permette di dialogare con un agente AI in grado di:
- 🛫 **Cercare voli in tempo reale** (tramite Google Flights / SerpApi).
- 🏨 **Trovare alloggi e hotel** (tramite Google Hotels / SerpApi).
- 🗺️ **Generare itinerari di viaggio personalizzati** suddivisi per giornata (mattina, pomeriggio, sera).
- 🏛️ **Fornire approfondimenti storici e culturali** sulle destinazioni.
- 🦙 **Eseguire in locale con Ollama** (es. `lfm3`, `llama3.1`) oppure su cloud con **OpenAI** (`gpt-4o`) con switch trasparente.

---

## 📋 Indice
1. [Requisiti di Sistema](#-requisiti-di-sistema)
2. [Installazione e Configurazione](#-installazione-e-configurazione)
3. [Avvio dell'Applicazione](#-avvio-dellapplicazione)
4. [Test delle API (Swagger UI)](#-test-delle-api-swagger-ui)
5. [Integrazione con il Front-End Laravel](#-integrazione-con-il-front-end-laravel)
6. [Passaggi Seguiti dalla Documentazione](#-passaggi-seguiti-dalla-documentazione)
7. [Dettaglio dei File del Progetto](#-dettaglio-dei-file-del-progetto)

---

## 💻 Requisiti di Sistema
- **Python**: `>= 3.13`
- **Poetry**: package and dependency manager per Python
- **Ollama** (per esecuzione locale gratuita) o chiave **OpenAI**
- **SerpApi API Key**: per consentire le ricerche reali di voli e hotel

---

## ⚙️ Installazione e Configurazione

### 1. Navigare nella cartella del backend
```powershell
cd travel-agent-api
```

### 2. Configurare la versione di Python in Poetry
```powershell
poetry env use 3.13
```

### 3. Installare le dipendenze del progetto
```powershell
poetry install
```

### 4. Configurare le variabili d'ambiente
Copia il file di esempio `.env.example` in `.env`:
```powershell
cp .env.example .env
```

Modifica il file `.env` inserendo le tue credenziali:
```ini
# Chiave API di OpenAI (lasciare il placeholder o vuoto se si usa solo Ollama)
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

# Chiave API SerpApi (per interrogare Google Flights e Google Hotels)
SERPAPI_API_KEY="la_tua_chiave_serpapi"

# Configurazione Ollama per esecuzione in locale
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_MODEL="lfm3:latest"
```

> **Nota sul supporto LLM**:  
> L'applicazione supporta sia Ollama che OpenAI in modo dinamico:
> - Se `OPENAI_API_KEY` non è configurata o contiene il valore placeholder, l'API instraderà le richieste verso **Ollama**.
> - Se inserisci una chiave OpenAI valida, utilizzerà in automatico **GPT-4o**.

---

## 🚀 Avvio dell'Applicazione

Avvia il server di sviluppo con Uvicorn sulla porta **8080** con hot-reload attivo:

```powershell
poetry run uvicorn travel_agent_api.main:app --reload --port 8080
```

Il server sarà attivo all'indirizzo: `http://127.0.0.1:8080`

---

## 🧪 Test delle API (Swagger UI)

FastAPI genera automaticamente la documentazione interattiva:
- **Swagger UI**: `http://127.0.0.1:8080/docs`
- **ReDoc**: `http://127.0.0.1:8080/redoc`

### Esempio di richiesta all'endpoint `POST /chat/travel-agent`
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Vorrei organizzare un viaggio a Roma dal 10 al 15 dicembre per 2 adulti. Trovami anche dei voli da Milano."
    }
  ]
}
```

---

## 🖥️ Integrazione con il Front-End Laravel

L'applicazione grafica si trova nella cartella `web_TravelAgent`. Per avviarla:
1. Apri un terminale nella cartella del front-end:
   ```powershell
   cd ../web_TravelAgent
   composer install
   npm install
   npm run dev
   ```
2. In un altro terminale avvia il server PHP:
   ```powershell
   php artisan serve
   ```
3. Visita `http://localhost:8000` nel browser per chattare con l'agente tramite l'interfaccia utente.

---

## 📝 Passaggi Seguiti dalla Documentazione

Lo sviluppo dell'API ha seguito passo dopo passo i 6 capitoli della documentazione ufficiale del corso:

### 1. Capitolo 1 & 2 - Setup del Progetto
- Inizializzazione del progetto tramite Poetry con vincolo Python `>=3.13`.
- Installazione di tutte le librerie essenziali: FastAPI, Uvicorn, LangChain, LangGraph, Pydantic, SerpApi (`google-search-results`), `python-dotenv` e `langchain-ollama`.
- Creazione dei file di ambiente (`.env.example` e `.env`) per la gestione sicura delle chiavi API (SerpApi, OpenAI/Ollama).
- Configurazione del file `.gitignore` per escludere file sensibili, virtualenv e cache di sistema.

### 2. Capitolo 3 - Creazione dell'API Base e Routing
- Creazione del punto di ingresso `main.py` con istanza `FastAPI()`.
- Configurazione del middleware CORS (`CORSMiddleware`) per consentire la comunicazione tra l'API (porta `8080`) e il front-end Laravel (porta `8000`).
- Creazione della cartella `routes/` e del file `chat_router.py`.
- Definizione del modello di validazione `ChatComplentionRequest` (con payload di esempio visibile in Swagger).
- Creazione dell'endpoint `POST /chat/travel-agent` collegato con prefisso `/chat`.

### 3. Capitolo 4 - Implementazione dei 4 Tool dell'Agente
- Creazione della cartella `tools/` con i relativi moduli:
  1. **5.1 Flights Finder (`flights_finder.py`)**: tool `@tool` con schema Pydantic per cercare voli in tempo reale tramite Google Flights (SerpApi).
  2. **5.2 Hotels Finder (`hotels_finder.py`)**: tool `@tool` con schema Pydantic ed enum classi hotel (2-5 stelle) per la ricerca strutture ricettive tramite Google Hotels (SerpApi).
  3. **5.3 Travel Plan Tool (`chain_travel_plan.py`)**: catena LCEL con `PydanticOutputParser` che genera un itinerario giornaliero strutturato (`morning`, `afternoon`, `evening`) in base al budget e allo stile di viaggio.
  4. **5.4 Historical Expert Tool (`chain_historical_expert.py`)**: tool con prompt personalizzato per fornire cenni storici e culturali arricchiti da emoji.

### 4. Capitolo 5 - Implementazione del Servizio Agent ReAct
- Creazione della cartella `services/` e del file `agent_service.py`.
- Definizione dei template di prompt Markdown (`FLIGHTS_OUTPUT`, `HOTELS_OUTPUT`, `TRAVEL_PLAN_OUTPUT`).
- Creazione della classe `Agent`:
  - Configurazione dinamica del modello (supporto sia a Ollama in locale che a OpenAI).
  - Registrazione dei 4 tool specializzati.
  - Creazione dell'agente esecutore basato su architettura ReAct tramite `create_react_agent` di LangGraph.
  - Metodo `run()` che inserisce data corrente e linee guida nel prompt di sistema e gestisce la cronologia dei messaggi.

### 5. Capitolo 6 - Esecuzione, Adattamento Ollama e Test
- Risoluzione dei vincoli di compatibilità per l'esecuzione con Ollama (switch automatico tra `ChatOllama` e `ChatOpenAI`).
- Aggiornamento degli import verso `langchain_core`.
- Test funzionale con esito positivo dei tool e della conversazione.
- Verifica dell'integrazione end-to-end con Swagger UI e client Laravel.

---

## 📂 Dettaglio dei File del Progetto

### File di Configurazione e Ambiente
- **`pyproject.toml`**: Configurazione del package `travel-agent-api`, dipendenze di produzione (FastAPI, Uvicorn, LangChain, LangGraph, Pydantic, SerpApi, Ollama) e vincoli di versione Python (`>=3.13,<4.0`).
- **`.gitignore`**: Esclude dal repository Git i file d'ambiente (`.env`), la cartella `.venv`, le cache Python (`__pycache__`), cache test e file generati dagli IDE.
- **`.env.example`**: Modello di esempio delle variabili d'ambiente necessarie all'esecuzione.
- **`.env`**: File locale con le credenziali e le configurazioni attive.

### Entrypoint e Routing
- **`src/travel_agent_api/main.py`**: Inizializza FastAPI, imposta il middleware CORS per abilitare le origini `http://127.0.0.1:8000` e `http://localhost:8000`, e registra il router `chat_router` con prefisso `/chat`.
- **`src/travel_agent_api/routes/chat_router.py`**: Definisce il modello Pydantic `ChatComplentionRequest` e l'endpoint `POST /chat/travel-agent` che riceve la cronologia dei messaggi, avvia l'elaborazione dell'agente e ne restituisce l'output.
- **`src/travel_agent_api/routes/__init__.py`**: Dichiara la directory come package Python.

### Servizio Core dell'Agente
- **`src/travel_agent_api/services/llm_factory.py`**: Modulo centralizzato per la creazione dell'istanza LLM (`get_llm()`). Seleziona automaticamente **Ollama** (`ChatOllama`) o **OpenAI** (`ChatOpenAI`) in base alle variabili `.env`, evitando duplicazioni di codice tra l'agente e i tool.
- **`src/travel_agent_api/services/agent_service.py`**: Cuore logico dell'applicazione. Contiene i template formattati per i voli, gli hotel e l'itinerario. La classe `Agent` istanzia il modello LLM tramite `get_llm()`, registra i quattro tool e compila il grafo ReAct tramite `create_react_agent` di LangGraph.
- **`src/travel_agent_api/services/__init__.py`**: Dichiara la directory come package Python.

### Strumenti (Tools)
- **`src/travel_agent_api/tools/flights_finder.py`**: Valida gli input (aeroporti di partenza/arrivo IATA, date andata/ritorno, passeggeri) e interroga l'engine `google_flights` di SerpApi restituendo i voli trovati.
- **`src/travel_agent_api/tools/hotels_finder.py`**: Valida i parametri di ricerca alloggio (località, date check-in/check-out, ospiti, stelle) e interroga l'engine `google_hotels` di SerpApi restituendo le strutture ricettive.
- **`src/travel_agent_api/tools/chain_travel_plan.py`**: Catena LangChain che elabora i vincoli di viaggio (date, stile, budget, cibo) e restituisce un output strutturato con attività mattina, pomeriggio e sera tramite `PydanticOutputParser`.
- **`src/travel_agent_api/tools/chain_historical_expert.py`**: Catena LangChain per generare contenuti e curiosità storiche sulla destinazione selezionata.
- **`src/travel_agent_api/tools/__init__.py`**: Dichiara la directory come package Python.


---

## 🛠️ Personalizzazioni, Refactoring e Tracing

Oltre all'implementazione base prevista dalla documentazione, il progetto è stato personalizzato e rifattorizzato per migliorarne la manutenibilità e l'osservabilità:

### 1. Refactoring e Pulizia del Codice
- **Centralizzazione LLM (`services/llm_factory.py`)**: La logica di scelta e inizializzazione del modello linguistico (precedentemente replicata in `agent_service.py`, `chain_travel_plan.py` e `chain_historical_expert.py`) è stata estratta nella funzione riutilizzabile `get_llm()`.
- **Gestione Errori HTTP (`routes/chat_router.py`)**: L'endpoint `/chat/travel-agent` intercetta eventuali eccezioni durante l'esecuzione dell'agente e restituisce un'eccezione HTTP `500` strutturata tramite `HTTPException`.
- **Pulizia Naming e Alias**: Corretti alcuni refusi nei nomi di classi e variabili (`ChatCompletionRequest` con alias retrocompatibile `ChatComplentionRequest`, `conversation_history`), oltre all'aggiornamento degli import su `langchain_core`.

### 2. Sistema di Tracing (`print`)
Sono state inserite istruzioni `print` strutturate con prefisso `[TRACE]` in ogni livello dell'applicazione per monitorare in tempo reale il flusso di esecuzione nel terminale:
- **`[TRACE][Router]`**: Registra la ricezione della richiesta POST, il numero di messaggi nella conversazione, un'anteprima dell'ultimo prompt e il tempo totale di risposta.
- **`[TRACE][LLMFactory]`**: Indica quale provider e modello viene istanziato (`Ollama` o `OpenAI`).
- **`[TRACE][Agent]`**: Mostra i tool registrati nell'agente ReAct, l'avvio del grafo e la durata dell'elaborazione.
- **`[TRACE][Tool: ...]`**: Ogni tool (`flights_finder`, `hotels_finder`, `chain_travel_plan`, `chain_historical_expert`) stampa i parametri ricevuti, l'esito della chiamata (es. numero di voli/hotel trovati o giorni dell'itinerario) ed eventuali errori.

#### Esempio di output di tracing in console:
```text
================================================================================
[TRACE][Router] POST /chat/travel-agent | Messaggi ricevuti: 1
[TRACE][Router] Ultimo messaggio (user): 'Vorrei organizzare un viaggio a Roma'
[TRACE][LLMFactory] Modello selezionato: Ollama (lfm3:latest) @ http://localhost:11434
[TRACE][Agent] Inizializzazione ReAct Agent | Tools registrati: ['chain_historical_expert', 'flights_finder', 'hotels_finder', 'chain_travel_plan']
[TRACE][Agent] Avvio esecuzione grafo ReAct (1 messaggi nella storia)...
********************************************************************************
[TRACE][Tool: chain_historical_expert] Argomento richiesto: 'Storia di Roma...'
[TRACE][LLMFactory] Modello selezionato: Ollama (lfm3:latest) @ http://localhost:11434
[TRACE][Tool: chain_historical_expert] Risposta generata (850 caratteri)
********************************************************************************
[TRACE][Agent] Esecuzione completata in 12.34s | Messaggi generati: 4
[TRACE][Router] Risposta restituita in 12.40s
================================================================================
```
