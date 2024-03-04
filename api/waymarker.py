from fastapi import APIRouter, Request, UploadFile, HTTPException, Depends
from fastapi.templating import Jinja2Templates

import yaml
import logging
from sqlalchemy.orm import Session

from services.bulk_upload.waymarkers import bulk_upload_waymarkers
from database.db import get_db

router = APIRouter(
    prefix="/waymarkers",
    tags=["waymarkers"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def upload_landing_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload")
async def upload_file(
    request: Request, file: UploadFile, db: Session = Depends(get_db)
):
    if file.content_type != "application/x-yaml":
        raise HTTPException(status_code=415, detail="Only YAML files")

    try:
        contents = await file.read()
        data = yaml.safe_load(contents)
        logger.info(f"Data from file: {data}")
        logger.info(f"keys: {data.keys()}")
        errors, results = await bulk_upload_waymarkers(db, data["waymarkers"])
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    return templates.TemplateResponse("bulk_upload_results.html", 
                                      {"request": request,
                                       "errors": errors, 
                                       "results": results})
