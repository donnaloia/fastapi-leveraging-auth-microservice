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
    prefix="/organizations",
    tags=["organizations"]
)


@router.post("/organization", response_model=List[schemas.CreateCategory])
def test_organizations(db: Session = Depends(get_db)):
    organizations = db.query(models.Organization).all()
    return organizations

@router.post(
    "/organization/create", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.CreateOrganization
)

def create_organization(organization: schemas.CreateOrganization, db: Session = Depends(get_db)):
    new_organization = models.Category(**organization.dict())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    return new_organization


@router.get(
    "/organization/{organization_id}", 
    response_model=schemas.CreateOrganization
)
def get_organization(category_id: UUID, db: Session = Depends(get_db)):
    organization = db.query(models.Organization).filter(models.Organization.id == str(organization_id)).first()
    db.commit()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.get(
    "/organization", 
    response_model=List[schemas.CreateOrganization]
)
def get_organization(db: Session = Depends(get_db)) -> Page[models.Organization]:
    return paginate(db, select(models.Organization).order_by(models.Organization.name))