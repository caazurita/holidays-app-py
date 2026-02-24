from pydantic import BaseModel, Field
from typing import Literal

class Holiday(BaseModel): 
    local_name: str = Field(alias="localName")
    date: str 
    country_code: str = Field(alias="countryCode")
    type: str
    summary: str
    category: Literal['national', 'religious', 'cultural'] | None = None
    