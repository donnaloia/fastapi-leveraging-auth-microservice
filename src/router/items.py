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
    prefix="/items",
    tags=["items"]
)

@router.post("/item", response_model=List[schemas.CreateItem])
def test_items(db: Session = Depends(get_db)):
    items = db.query(models.item).all()
    return items


@router.post(
    "/create", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.CreateItem
)
def create_items(item: schemas.CreateItem, db: Session = Depends(get_db)):
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get(
    "/{item_id}", 
    response_model=schemas.CreateItem
)
def get_item(item_id: UUID, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == str(item_id)).first()
    db.commit()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Get first 10 items
@router.get(
    "/", 
    response_model=Page[schemas.ItemDetailed]
)
def get_items(db: Session = Depends(get_db)) -> Page[models.Item]:
    return paginate(db, select(models.Item).order_by(models.Item.created_at))


