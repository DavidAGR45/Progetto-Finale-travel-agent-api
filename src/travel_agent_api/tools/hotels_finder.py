# hotels_finder.py
import os
from enum import IntEnum
from typing import Optional
from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from serpapi import GoogleSearch

load_dotenv()


class HotelClassEnum(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class HotelsInput(BaseModel):
    q: str = Field(description="Location of the hotel.")
    check_in_date: str = Field(description="The outbound date (YYYY-MM-DD) e.g. 2024-12-13.")
    check_out_date: str = Field(description="The return date (YYYY-MM-DD) e.g. 2024-12-19.")
    adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")
    children: Optional[int] = Field(0, description="The number of children. Defaults to 0.")
    hotel_class: Optional[int] = Field(2, description="The hotel class available from 2 to 5. Defaults to 2.")


class HotelsInputSchema(BaseModel):
    params: HotelsInput


# Alias per compatibilità con eventuale typo presente nelle slide
HoltesInputSchema = HotelsInputSchema


@tool(args_schema=HotelsInputSchema)
def hotels_finder(params: HotelsInput):
    """
    This tool uses the SerpApi Google Hotels API to retrieve hotels info.

    Parameters:
        q (str): Location of the hotel.
        check_in_date (str): The outbound date (YYYY-MM-DD) e.g. 2024-12-13.
        check_out_date (str): The return date (YYYY-MM-DD) e.g. 2024-12-19.
        adults (int): The number of adults. Defaults to 1.
        children (int): The number of children. Defaults to 0.
        hotel_class (int): The hotel class available from 2 to 5. Defaults to 2.

    Returns:
        dict: A dictionary containing the hotels info. If the API call fails, it returns the
        error message as a string.
    """
    print("*" * 80)
    print(
        f"[TRACE][Tool: hotels_finder] Ricerca hotel a '{params.q}' "
        f"| Check-in: {params.check_in_date}, Check-out: {params.check_out_date} "
        f"| Adulti: {params.adults}, Bambini: {params.children}, Stelle: {params.hotel_class}"
    )

    search_params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google_hotels",
        "hl": "it",
        "gl": "it",
        "currency": "EUR",
        "q": params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "adults": params.adults,
        "children": params.children,
        "hotel_class": params.hotel_class,
        "num": 5,
    }
    try:
        search = GoogleSearch(search_params)
        results = search.get_dict()["properties"]
        print(f"[TRACE][Tool: hotels_finder] Estratti {len(results)} hotel")
    except Exception as e:
        print(f"[TRACE][Tool: hotels_finder][ERRORE] {e}")
        results = str(e)

    print("*" * 80)
    return results
