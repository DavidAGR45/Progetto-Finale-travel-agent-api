# services/llm_factory.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm():
    """
    Restituisce l'istanza del modello linguistico (LLM) configurata nell'ambiente.
    Se è configurato OLLAMA_BASE_URL e non è presente una chiave OpenAI valida,
    utilizza ChatOllama; altrimenti utilizza ChatOpenAI (gpt-4o).
    """
    openai_key = os.getenv("OPENAI_API_KEY", "")
    ollama_url = os.getenv("OLLAMA_BASE_URL")

    if ollama_url and (not openai_key or "YOUR_OPENAI_API_KEY" in openai_key):
        from langchain_ollama import ChatOllama

        model_name = os.getenv("OLLAMA_MODEL", "llama3.1")
        print(f"[TRACE][LLMFactory] Modello selezionato: Ollama ({model_name}) @ {ollama_url}")
        return ChatOllama(model=model_name, base_url=ollama_url)

    print("[TRACE][LLMFactory] Modello selezionato: OpenAI (gpt-4o)")
    return ChatOpenAI(model_name="gpt-4o")
