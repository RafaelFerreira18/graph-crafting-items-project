from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas


router = APIRouter()


@router.get("/", response_model=list[schemas.ItemOut])
def list_all(db: Session = Depends(get_db)):
    return crud.list_items(db)


@router.post("/", response_model=schemas.ItemOut)
def create(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    obj = crud.get_or_create_item(db, item.nome, item.eh_basico)
    db.commit()
    db.refresh(obj)
    return obj


