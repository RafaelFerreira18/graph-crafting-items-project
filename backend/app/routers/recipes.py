from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas


router = APIRouter()


@router.get("/", response_model=list[schemas.ReceitaOut])
def list_all(db: Session = Depends(get_db)):
    receitas = crud.list_recipes(db)
    saida: list[schemas.ReceitaOut] = []
    for r in receitas:
        saida.append(
            schemas.ReceitaOut(
                id=r.id,
                resultado_nome=r.resultado_item.nome,
                quantidade_resultado=r.quantidade_resultado,
                ingredientes=[
                    schemas.IngredienteOut(item_nome=ing.item.nome, quantidade=ing.quantidade)
                    for ing in r.ingredientes
                ],
            )
        )
    return saida


@router.post("/", response_model=schemas.ReceitaOut)
def create(receita: schemas.ReceitaCreate, db: Session = Depends(get_db)):
    obj = crud.create_recipe(
        db,
        resultado_nome=receita.resultado_nome,
        quantidade_resultado=receita.quantidade_resultado,
        ingredientes=[(i.item_nome, i.quantidade) for i in receita.ingredientes],
    )
    db.commit()
    db.refresh(obj)
    return schemas.ReceitaOut(
        id=obj.id,
        resultado_nome=obj.resultado_item.nome,
        quantidade_resultado=obj.quantidade_resultado,
        ingredientes=[
            schemas.IngredienteOut(item_nome=ing.item.nome, quantidade=ing.quantidade)
            for ing in obj.ingredientes
        ],
    )


