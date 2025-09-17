from collections import defaultdict, deque
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas


router = APIRouter()


def build_graph(db: Session):
    nodes, edges = crud.graph_data(db)
    g_direct = defaultdict(list)
    g_inverse = defaultdict(list)
    for u, v in edges:
        g_direct[u].append(v)
        g_inverse[v].append(u)
    return nodes, g_direct, g_inverse


@router.post("/bfs")
def bfs(req: schemas.BFSRequest, db: Session = Depends(get_db)):
    recursos = req.recursos_iniciais or {}
    nodes, g_direct, _ = build_graph(db)
    fila = deque()
    possiveis = set(recursos.keys())
    recursos_disponiveis = recursos.copy()

    for r in recursos.keys():
        fila.append(r)

    # Para verificar craft, precisamos das receitas completas
    receitas = crud.list_recipes(db)

    def pode_craftar(item):
        for r in receitas:
            if r.resultado_item.nome != item:
                continue
            ok = True
            for ing in r.ingredientes:
                if ing.item.nome not in recursos_disponiveis or recursos_disponiveis[ing.item.nome] < ing.quantidade:
                    ok = False
                    break
            if ok:
                return True
        return False

    while fila:
        atual = fila.popleft()
        for prox in g_direct.get(atual, []):
            if prox not in possiveis and pode_craftar(prox):
                possiveis.add(prox)
                fila.append(prox)
                recursos_disponiveis[prox] = float('inf')

    return sorted(list(possiveis))


@router.post("/cost")
def cost(req: schemas.CostRequest, db: Session = Depends(get_db)):
    alvo = req.item_alvo
    basicos = set(req.recursos_basicos or [])
    nodes, g_direct, _ = build_graph(db)
    dist = {n: float('inf') for n in nodes}
    for b in basicos:
        dist[b] = 0
    visit = set()
    while len(visit) < len(nodes):
        u = None
        best = float('inf')
        for n in nodes:
            if n not in visit and dist[n] < best:
                best = dist[n]
                u = n
        if u is None:
            break
        visit.add(u)
        for v in g_direct.get(u, []):
            nd = dist[u] + 1
            if nd < dist[v]:
                dist[v] = nd
    return {"custo": dist.get(alvo, float('inf'))}


@router.post("/path")
def path(req: schemas.PathRequest, db: Session = Depends(get_db)):
    alvo = req.item_alvo
    basicos = set(req.recursos_basicos or [])
    _, _, g_inverse = build_graph(db)
    from collections import deque as dq
    fila = dq([(alvo, [alvo])])
    vis = {alvo}

    receitas = crud.list_recipes(db)
    mapa_receitas = defaultdict(list)
    for r in receitas:
        mapa_receitas[r.resultado_item.nome].append(r)

    while fila:
        atual, caminho = fila.popleft()
        for r in mapa_receitas.get(atual, []):
            todos_basicos = True
            for ing in r.ingredientes:
                if ing.item.nome not in basicos:
                    todos_basicos = False
                    if ing.item.nome not in vis:
                        vis.add(ing.item.nome)
                        fila.append((ing.item.nome, [ing.item.nome] + caminho))
            if todos_basicos:
                return {"caminho": caminho}

    return {"caminho": None}


