from pydantic import BaseModel
from typing import Union


class Waymarker(BaseModel):
    id: str
    active: Union[bool, None] = None
    apiKey: Union[str, None] = None
