from typing import List
import logging
from cuid import cuid
from sqlalchemy.orm import Session

from services.db_utils import create_waymarker
from models.waymarker import Waymarker as WaymarkerModel

logger = logging.getLogger(__name__)


async def bulk_upload_waymarkers(db: Session, waymarkers: List):
    if len(waymarkers) == 0:
        return "No waymarkers to upload"

    created_waymarker_ids = []

    # TODO: implement batch uploads, in sectionf of 50 or 100
    for waymarker_data in waymarkers:
        waymarker = WaymarkerModel(
            id=cuid(),
            firstName=waymarker_data["first_name"],
            lastName=waymarker_data["last_name"],
            market=waymarker_data["market"],
            email=waymarker_data["email"],
            title=waymarker_data["title"],
        )
        logger.info(f"{waymarker} data input")

        waymarker = create_waymarker(db, waymarker)
        logger.info(
            f"Created waymarker {waymarker.id} \
                    with email {waymarker.email}"
        )
        created_waymarker_ids.append(waymarker.id)
    return created_waymarker_ids
