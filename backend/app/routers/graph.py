from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas


router = APIRouter()


@router.get("/", response_model=schemas.GraphOut)
def get_graph(db: Session = Depends(get_db)):
    nodes, edges = crud.graph_data(db)
    return schemas.GraphOut(nodes=nodes, edges=edges)


