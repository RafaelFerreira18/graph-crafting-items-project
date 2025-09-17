from typing import List, Optional
from pydantic import BaseModel


class ItemCreate(BaseModel):
    nome: str
    eh_basico: bool = False


class ItemOut(BaseModel):
    id: int
    nome: str
    eh_basico: bool

    class Config:
        from_attributes = True


class IngredienteIn(BaseModel):
    item_nome: str
    quantidade: int = 1


class ReceitaCreate(BaseModel):
    resultado_nome: str
    quantidade_resultado: int = 1
    ingredientes: List[IngredienteIn]


class IngredienteOut(BaseModel):
    item_nome: str
    quantidade: int


class ReceitaOut(BaseModel):
    id: int
    resultado_nome: str
    quantidade_resultado: int
    ingredientes: List[IngredienteOut]

    class Config:
        from_attributes = True


class GraphOut(BaseModel):
    nodes: List[str]
    edges: List[tuple]


class BFSRequest(BaseModel):
    recursos_iniciais: dict


class CostRequest(BaseModel):
    item_alvo: str
    recursos_basicos: List[str]


class PathRequest(BaseModel):
    item_alvo: str
    recursos_basicos: List[str]


