from pydantic import BaseModel, ConfigDict
from typing import Union
from enum import Enum


class Market(str, Enum):
    SEATTLE = "Seattle"
    RICHMOND = "Richmond"
    HAMPTON_ROADS = "Hampton Roads"
    TIDEWATER = "Tidewater"


class WaymarkerTitle(str, Enum):
    CARE_COORDINATOR = "CARE_COORDINATOR"
    CHW = "CHW"
    CHW_LEAD = "CHW_LEAD"
    THERAPIST = "THERAPIST"
    THERAPIST_LEAD = "THERAPIST_LEAD"
    PHARMACIST = "PHARMACIST"
    PHARMACIST_LEAD = "PHARMACIST_LEAD"
    PHARMACY_TECH = "PHARMACY_TECH"
    MARKET_LEAD = "MARKET_LEAD"
    NATIONAL_CHW_LEAD = "NATIONAL_CHW_LEAD"
    HEAD_OF_CLINICAL = "HEAD_OF_CLINICAL"
    HEAD_OF_CARE_OPS = "HEAD_OF_CARE_OPS"
    ANALYTICS_LEAD = "ANALYTICS_LEAD"


class Waymarker(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    firstName: Union[str, None] = None
    lastName: Union[str, None] = None
    email: Union[str, None] = None
    title: Union[str, None] = None
    market: Union[Market, None] = None
    phone_number: Union[str, None] = None

    # used for authentication purposes
    active: Union[bool, None] = None
    apiKey: Union[str, None] = None
