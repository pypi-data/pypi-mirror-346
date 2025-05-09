from pydantic import BaseModel

class LegalInformationModel(BaseModel):
    chain: str
    registration_country: str
    inn: str
    owner: str