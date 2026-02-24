from pydantic import BaseModel
from typing import List


class Summary(BaseModel):
    name: str
    summary: str
    category: str
    