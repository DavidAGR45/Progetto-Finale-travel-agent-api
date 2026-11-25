# services/agent_service.py
import time
from datetime import datetime
from langgraph.prebuilt import create_react_agent

from travel_agent_api.services.llm_factory import get_llm
from travel_agent_api.tools.flights_finder import flights_finder
from travel_agent_api.tools.hotels_finder import hotels_finder
from travel_agent_api.tools.chain_historical_expert import chain_historical_expert
from travel_agent_api.tools.chain_travel_plan import chain_travel_plan

FLIGHTS_OUTPUT = """
format: markdown 
    ## Miglior Opzione 
    ### Andata:
    - Compagnia aerea: Ryanair
    - Data di partenza: 2024-12-13
    - Ora di partenza: 10:00
    - Durata del volo: 1h 30m
    ### Ritorno:
    - Compagnia aerea: Ryanair
    - Data di ritorno: 2024-12-19
    - Ora di ritorno: 14:30
    - Durata del volo: 1h 30m
    Inserisci il link di Google per la prenotazione se possibile.

    #### Altri opzioni disponibili:
    - Compagnia aerea: Ryanair
    - Data di partenza: 2024-12-13
    - Ora di partenza: 10:00
    - Durata del volo: 1h 30m
    - Compagnia aerea: Ryanair
    - Data di ritorno: 2024-12-19
    - Ora di ritorno: 14:30
    - Durata del volo: 1h 30m
    ...
"""

HOTELS_OUTPUT = """
format: markdown 
    #### Hotel 1
    Inserisci la foto dell'hotel se disponibile. 
    *Descrizione:* Camere e suite eleganti, a volte con vista sulla città, in hotel esclusivo con piscina panoramica e spa.
    *Prezzo per notte:* €296 (prima delle tasse e spese: €260)
    *Prezzo totale:* €2,660 (prima delle tasse e spese: €2,336)
    *Check-in:* 15:00, Check-out: 12:00
    *Valutazione complessiva:* 4.5 su 5
    *Servizi Inclusi:* Spa, Piscina, Parcheggio gratuito
    #### Hotel 2
    Inserisci la foto dell'hotel se disponibile. 
    Descrizione: Hotel in stile Liberty con alloggi arredati in maniera artistica, ristorante elegante, bar e spa.
    *Prezzo per notte:* €380 (prima delle tasse e spese: €333)
    *Prezzo totale:* €3,418 (prima delle tasse e spese: €3,000)
    *Check-in:* 15:00, Check-out: 12:00
    *Valutazione complessiva:* 4.5 su 5
    *Servizi Inclusi:* Spa, Piscina, Parcheggio gratuito
"""

TRAVEL_PLAN_OUTPUT = """
format: markdown 
    ### Itinerario: 
    ### Giorno 1 - 2024-12-13:
    *Mattina:* Descrizione dell'attivita' da svolgere la mattina
    *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
    *Sera:* Descrizione dell'attivita' da svolgere la sera
    ### Giorno 2 - 2024-12-14:
    *Mattina:* Descrizione dell'attivita' da svolgere la mattina
    *Pomeriggio:* Descrizione dell'attivita' da svolgere il pomeriggio
    *Sera:* Descrizione dell'attivita' da svolgere la sera
    
    ...
"""


class Agent:
    def __init__(self):
        self.current_datetime = datetime.now()
        self.model = get_llm()
        self.tools = [
            chain_historical_expert,
            flights_finder,
            hotels_finder,
            chain_travel_plan,
        ]
        tool_names = [t.name for t in self.tools]
        print(f"[TRACE][Agent] Inizializzazione ReAct Agent | Tools registrati: {tool_names}")
        self.agent_executor = create_react_agent(self.model, self.tools)

    def run(self, messages: list):
        SYSTEM_PROMPT = f"""
            Sei un travel planner. Il tuo compito e' organizzare il viaggio per l'utente. 
            Aggiungi delle emojis per rendere il tuo output piu' interessante.
            La data di oggi e' {self.current_datetime}
            Usa le seguenti istruzioni per creare un output:
            Esempio Ouput Voli: 
            {FLIGHTS_OUTPUT}
            Esempio Output Hotel:
            {HOTELS_OUTPUT}
            Esempio di Output Viaggio:
            {TRAVEL_PLAN_OUTPUT}
        """
        conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        print(f"[TRACE][Agent] Avvio esecuzione grafo ReAct ({len(messages)} messaggi nella storia)...")
        start_time = time.perf_counter()

        response = self.agent_executor.invoke({"messages": conversation_history})

        elapsed = time.perf_counter() - start_time
        output_messages = response["messages"][1:]
        print(f"[TRACE][Agent] Esecuzione completata in {elapsed:.2f}s | Messaggi generati: {len(output_messages)}")
        return output_messages
