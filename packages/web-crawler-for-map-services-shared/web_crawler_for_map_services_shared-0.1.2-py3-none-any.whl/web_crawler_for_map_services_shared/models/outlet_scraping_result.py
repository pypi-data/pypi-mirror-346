from pydantic import BaseModel
from typing import Optional

from .outlet_model import OutletModel
from .outlet_scraping_request import OutletScrapingRequest

class OutletScrapingResult(BaseModel):
    outlet_scraping_request: Optional[OutletScrapingRequest]
    outlet_model: Optional[OutletModel]
    error_msg: Optional[str]
