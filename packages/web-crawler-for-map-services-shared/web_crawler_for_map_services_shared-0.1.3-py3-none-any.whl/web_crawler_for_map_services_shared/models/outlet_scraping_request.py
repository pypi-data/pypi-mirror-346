from pydantic import BaseModel

class OutletScrapingRequest(BaseModel):
    map_service: str
    search_query: str
    search_url: str
    session_id: str