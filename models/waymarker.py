from pydantic import BaseModel, ConfigDict
from typing import Union


class Waymarker(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    active: Union[bool, None] = None
    apiKey: Union[str, None] = None
