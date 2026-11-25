# flights_finder.py
import os
from typing import Optional
from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from serpapi import GoogleSearch

load_dotenv()


class FlightsInput(BaseModel):
    departure_airport: str = Field(description="The departure airport code (IATA).")
    arrival_airport: str = Field(description="The arrival airport code (IATA).")
    outbound_date: str = Field(description="The outbound date (YYYY-MM-DD) e.g. 2024-12-13.")
    return_date: str = Field(description="The return date (YYYY-MM-DD) e.g. 2024-12-19.")
    adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")
    children: Optional[int] = Field(0, description="The number of children. Defaults to 0.")


class FlightsInputSchema(BaseModel):
    params: FlightsInput


@tool(args_schema=FlightsInputSchema)
def flights_finder(params: FlightsInput):
    """
    This tool uses the SerpApi Google Flights API to retrieve flights info.

    Parameters:
        departure_airport (str): The departure airport code (IATA).
        arrival_airport (str): The arrival airport code (IATA).
        outbound_date (str): The outbound date (YYYY-MM-DD) e.g. 2024-12-13.
        return_date (str): The return date (YYYY-MM-DD) e.g. 2024-12-19.
        adults (int): The number of adults. Defaults to 1.
        children (int): The number of children. Defaults to 0.

    Returns:
        dict: A dictionary containing the flights info. If the API call fails, it returns the
        error message as a string.
    """
    print("*" * 80)
    print(
        f"[TRACE][Tool: flights_finder] Ricerca voli: {params.departure_airport} -> {params.arrival_airport} "
        f"| Andata: {params.outbound_date}, Ritorno: {params.return_date} "
        f"| Adulti: {params.adults}, Bambini: {params.children}"
    )

    try:
        search_params = {
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "engine": "google_flights",
            "hl": "it",
            "gl": "it",
            "currency": "EUR",
            "stops": "1",
            "departure_id": params.departure_airport,
            "arrival_id": params.arrival_airport,
            "outbound_date": params.outbound_date,
            "return_date": params.return_date,
            "adults": params.adults,
            "children": params.children,
        }
        search = GoogleSearch(search_params)
        results = search.get_dict()
        best_count = len(results.get("best_flights", []))
        other_count = len(results.get("other_flights", []))
        print(f"[TRACE][Tool: flights_finder] Trovati {best_count} best_flights e {other_count} other_flights")
        print("*" * 80)
        return results
    except Exception as e:
        print(f"[TRACE][Tool: flights_finder][ERRORE] {e}")
        print("*" * 80)
        return str(e)
