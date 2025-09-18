from typing import List, Optional
from sqlalchemy.orm import Session

from . import models


def get_or_create_item(db: Session, nome: str, eh_basico: bool = False) -> models.Item:
    nome_norm = nome.strip()
    item = db.query(models.Item).filter(models.Item.nome == nome_norm).first()
    if item:
        if eh_basico and not item.eh_basico:
            item.eh_basico = True
            db.add(item)
        return item
    item = models.Item(nome=nome_norm, eh_basico=eh_basico)
    db.add(item)
    db.flush()
    return item


def list_items(db: Session) -> List[models.Item]:
    return db.query(models.Item).order_by(models.Item.nome.asc()).all()


def create_recipe(
    db: Session,
    resultado_nome: str,
    quantidade_resultado: int,
    ingredientes: List[tuple],  # (nome, quantidade)
) -> models.Receita:
    resultado_item = get_or_create_item(db, resultado_nome)
    receita = models.Receita(
        resultado_item=resultado_item,
        quantidade_resultado=quantidade_resultado,
    )
    db.add(receita)
    db.flush()

    for nome, qtd in ingredientes:
        item = get_or_create_item(db, nome)
        db.add(
            models.IngredienteReceita(
                receita=receita, item=item, quantidade=int(qtd)
            )
        )
    db.flush()
    return receita


def list_recipes(db: Session) -> List[models.Receita]:
    return db.query(models.Receita).all()


def graph_data(db: Session):
    items = list_items(db)
    nodes = [{"id": i.nome, "label": i.nome, "eh_basico": i.eh_basico} for i in items]
    edges = []
    for r in list_recipes(db):
        for ing in r.ingredientes:
            edges.append((ing.item.nome, r.resultado_item.nome))
    return nodes, edges


