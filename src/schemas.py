from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Json
from typing import Union, Any


# note: these schemas are used for creating data, not for reading it it seems
class EligibilityStatusCategoryType(str, Enum):
    DROPPED_OUT_OF_ELIGIBILITY_FILE = "DROPPED_OUT_OF_ELIGIBILITY_FILE"
    EXPIRED_ELIGIBILITY_DATE = "EXPIRED_ELIGIBILITY_DATE"
    PCP_REFERRED = "PCP_REFERRED"
    OTHERS = "OTHERS"


class ElibilityStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    UNKNOWN = "UNKNOWN"


class Patient(BaseModel):
    id: str
    firstName: str
    middleName: Union[str, None]
    lastName: str
    gender: str
    preferredName: Union[str, None]
    pronunciation: Union[str, None]
    pronouns: Union[str, None]
    race: Union[list, None]
    primaryContactName: Union[str, None]
    primaryContactRelationship: Union[str, None]
    canShareProgramInfo: Union[bool, None]
    ethnicity: Union[str, None]
    languages: Json[Any]
    avatar: Union[str, None]
    bookmarked: Union[bool, None]
    region: str
    programs: Union[list, None]
    quickNote: Union[str, None]
    diagnoses: Union[list, None]
    socialDeterminants: Union[list, None]
    subscriberNumber: Union[str, None]
    medicaidNumber: Union[str, None]
    assignedMco: Union[str, None]
    createdAt: datetime
    updatedAt: datetime
    version: int
    status: Union[str, None]
    isEligible: ElibilityStatus | None
    eligibilityStatusCategory: EligibilityStatusCategoryType | None
    eligibilityStatusUpdateDate: datetime | None
    birthDate: datetime
    source: str
    userUpdated: Union[bool, None]
    waymarkPatientNumber: Union[str, None]

    class Config:
        orm_mode = True


class Waymarker(BaseModel):
    id: str
    active: Union[bool, None] = None
    apiKey: Union[str, None] = None
