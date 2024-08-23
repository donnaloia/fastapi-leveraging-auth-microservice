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
    prefix="/services",
    tags=["services"]
)

@router.post("/service", response_model=List[schemas.CreateService])
def test_services(db: Session = Depends(get_db)):
    applications = db.query(models.Service).all()
    return applications


@router.post(
    "/create", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.CreateService
)

def create_service(service: schemas.CreateService, db: Session = Depends(get_db)):
    new_service = models.Service(**service.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.get(
    "/{service_id}", 
    response_model=schemas.CreateService
)
def get_service(service_id: UUID, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == str(service_id)).first()
    db.commit()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


# Get first 10 items
@router.get(
    "/", 
    response_model=Page[schemas.ServiceDetailed]
)
def get_services(db: Session = Depends(get_db)) -> Page[models.Service]:
    return paginate(db, select(models.Service).order_by(models.Service.created_at))
