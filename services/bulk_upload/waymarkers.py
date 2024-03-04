from typing import List
import logging
from cuid import cuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from services.db_utils import create_waymarker, add_twilio_phone_number
from services.twilio import provision_new_phone_number

from models.waymarker import Waymarker as WaymarkerModel

logger = logging.getLogger(__name__)


async def bulk_upload_waymarkers(db: Session, waymarkers: List):
    if len(waymarkers) == 0:
        return "No waymarkers to upload"

    # limit the number of waymarkers to upload
    # - this is a temporary measure w/o batch-processing
    if len(waymarkers) > 20:
        return "Too many waymarkers to upload"

    created_waymarkers = []
    errors = []
    for waymarker_data in waymarkers:
        waymarker_model = WaymarkerModel(
            id=cuid(),
            firstName=waymarker_data["first_name"],
            lastName=waymarker_data["last_name"],
            market=waymarker_data["market"],
            email=waymarker_data["email"],
            title=waymarker_data["title"],
            phoneNumber=waymarker_data.get("phone_number"),
        )
        try:
            way_id, twilio_num = await create_waymarker_and_provision_number(
                db, waymarker_model
            )
            pixel_number = waymarker_data.get("phone_number")
            created_waymarker = {
                "id": way_id,
                "email": waymarker_data.get("email"),
                "first_name": waymarker_data.get("first_name"),
                "last_name": waymarker_data.get("last_name"),
                "market": waymarker_data.get("market"),
                "title": waymarker_data.get("title"),
                "pixel_number": pixel_number if pixel_number else "N/A",
                "twilio_number": twilio_num if twilio_num else "N/A",
            }
            created_waymarkers.append(created_waymarker)
        except Exception as e:
            logger.error(f"Error creating waymarker: {e}")
            errors.append(
                {"email": waymarker_data.get("email"),
                 "error": str(e)})

    return errors, created_waymarkers


async def create_waymarker_and_provision_number(db: Session, 
                                                waymarker: WaymarkerModel):
    # input validation
    WaymarkerModel.model_validate(waymarker)
    
    # try to add the Waymarker data into the database
    try: 
        created_waymarker = create_waymarker(db, waymarker)
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")
    
    logger.info(
        f"Created waymarker {created_waymarker.id} \
                with email {created_waymarker.email}"
    )

    # Provision the phone number if it is in the input data
    provisioned_phone_number = None
    if waymarker.phoneNumber is not None:
        friendly_name = f"{waymarker.firstName} \
            {waymarker.lastName} ({waymarker.title})"
        provisioned_phone_number = await (
            provision_new_phone_number.provision_new_waymarker_number(
                waymarker.market, friendly_name
            )
        )
        add_twilio_phone_number(db, str(waymarker.id),
                                provisioned_phone_number)
        logger.info(
            f"Provisioned phone number {provisioned_phone_number} \
                for waymarker {waymarker.id}"
        )

    return created_waymarker.id, provisioned_phone_number
