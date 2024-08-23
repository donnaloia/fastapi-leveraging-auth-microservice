from typing import List
from fastapi import (
    HTTPException, 
    Depends, 
    status, 
    APIRouter
)
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate


from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from src.db import models, schemas
from src.db.database import get_db


router = APIRouter(
    prefix="/applications",
    tags=["applications"]
)

@router.post("/application", response_model=List[schemas.CreateApplication])
def test_items(db: Session = Depends(get_db)):
    applications = db.query(models.application).all()
    return applications


@router.post(
    "/create", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.CreateApplication
)
def create_application(application: schemas.CreateApplication, db: Session = Depends(get_db)):
    new_application = models.Application(**application.dict())
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get(
    "/{application_id}", 
    response_model=schemas.CreateApplication
)
def get_application(application_id: UUID, db: Session = Depends(get_db)):
    application = db.query(models.Application).filter(models.Application.id == str(application_id)).first()
    db.commit()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


# Get first 10 items
@router.get(
    "/", 
    response_model=Page[schemas.ApplicationDetailed]
)
def get_applications(db: Session = Depends(get_db)) -> Page[models.Application]:
    return paginate(db, select(models.Application).order_by(models.Application.created_at))
