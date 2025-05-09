from typing import Optional
from models.outlet_model import OutletModel
from models.outlet_scraping_request import OutletScrapingRequest
from pydantic import BaseModel

class OutletScrapingResult(BaseModel):
    outlet_scraping_request: Optional[OutletScrapingRequest]
    outlet_model: Optional[OutletModel]
    error_msg: Optional[str]
