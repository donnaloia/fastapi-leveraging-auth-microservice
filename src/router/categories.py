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
    prefix="/categories",
    tags=["categories"]
)


@router.post("/category", response_model=List[schemas.CreateCategory])
def test_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

@router.post(
    "/category/create", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.CreateCategory
)

def create_category(category: schemas.CreateCategory, db: Session = Depends(get_db)):
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get(
    "/category/{category_id}", 
    response_model=schemas.CreateCategory
)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == str(category_id)).first()
    db.commit()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get(
    "/category", 
    response_model=List[schemas.CreateCategory]
)
def get_categories(db: Session = Depends(get_db)) -> Page[models.Category]:
    return paginate(db, select(models.Category).order_by(models.Category.name))