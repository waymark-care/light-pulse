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


class EligibilityStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    UNKNOWN = "UNKNOWN"


class PatientStatusTypes(str, Enum):
    ASSIGNED = "ASSIGNED"
    TARGETED = "TARGETED"
    OUTREACH = "OUTREACH"
    IN_CONTACT = "IN_CONTACT"
    ENROLLED = "ENROLLED"
    MAXIMUM = "MAXIMUM"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    MAINTENANCE = "MAINTENANCE"
    PREGRADUATION = "PREGRADUATION"
    GRADUATED = "GRADUATED"
    CLOSED = "CLOSED"
    CONSENTED = "CONSENTED"
    ONBOARDED = "ONBOARDED"
    REFUSED_MAYBE = "REFUSED_MAYBE"
    REFUSED_NO = "REFUSED_NO"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    DROPPED_OUT_OF_CONTACT = "DROPPED_OUT_OF_CONTACT"
    WITHDRAWN_PATIENT = "WITHDRAWN_PATIENT"
    WITHDRAWN_WAYMARK = "WITHDRAWN_WAYMARK"
    ACTIVATED = "ACTIVATED"


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
    isEligible: EligibilityStatus | None
    eligibilityStatusCategory: EligibilityStatusCategoryType | None
    eligibilityStatusUpdateDate: datetime | None
    birthDate: datetime
    source: str
    userUpdated: Union[bool, None]
    waymarkPatientNumber: Union[str, None]

    class Config:
        orm_mode = True


class AdmissionDischargeTransfer(BaseModel):
    id: str
    patientId: str
    visitNumber: Union[str, None]
    adtMasterId: Union[str, None]
    patientEpisode: Union[str, None]
    eventTypeCode: Union[str, None]
    triggerEvent: Union[str, None]
    eventDescription: Union[str, None]
    admitDate: Union[datetime, None]
    dischargedDate: Union[datetime, None]
    hospitalName: Union[str, None]
    phoneNumber: Union[str, None]
    address: Union[Json[Any], None]
    createdAt: datetime
    updatedAt: datetime
    dischargeDisposition: Union[str, None]
    patientClassCode: Union[str, None]
    hospitalServiceDescription: Union[str, None]
    asthmaEvent: Union[bool, None]
    behavioralHealthEvent: Union[bool, None]
    copdEvent: Union[bool, None]
    diabetesEvent: Union[bool, None]
    edAvoidable: Union[str, None]
    heartFailureEvent: Union[bool, None]
    hypertensionEvent: Union[bool, None]
    ipAvoidable: Union[str, None]
    maternityEvent: Union[bool, None]
    sudEvent: Union[bool, None]
    sudEvent: Union[bool, None]

    class Config:
        orm_mode = True
