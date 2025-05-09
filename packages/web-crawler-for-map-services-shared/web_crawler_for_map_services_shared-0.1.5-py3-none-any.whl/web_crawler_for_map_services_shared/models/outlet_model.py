from pydantic import BaseModel
from typing import List

from .legal_information_model import LegalInformationModel

class OutletModel(BaseModel):
    signboard: str
    address: str
    activity_types: List[str]
    contact_phones: List[str]
    review_keywords: List[str]
    legal_information: LegalInformationModel