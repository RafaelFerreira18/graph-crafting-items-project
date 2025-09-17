from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas


router = APIRouter()


@router.get("/", response_model=schemas.GraphOut)
def get_graph(db: Session = Depends(get_db)):
    nodes, edges = crud.graph_data(db)
    # Convert nodes to GraphNode objects
    graph_nodes = [schemas.GraphNode(id=node["id"], label=node["label"], eh_basico=node["eh_basico"]) for node in nodes]
    return schemas.GraphOut(nodes=graph_nodes, edges=edges)


@router.get("/adjacency", response_model=dict)
def get_adjacency_list(db: Session = Depends(get_db)):
    """
    Retorna a estrutura da Lista de Adjacência para visualização no frontend.
    
    ESTRUTURA DE DADOS: Lista de Adjacência
    Uma das quatro estruturas para grafos estudadas em aula.
    """
    nodes, edges = crud.graph_data(db)
    
    # Constrói a Lista de Adjacência
    adjacency_list = {}
    
    # Inicializa todos os nós com listas vazias
    for node in nodes:
        adjacency_list[node["id"]] = []
    
    # Adiciona as arestas (dependências de crafting)
    for from_node, to_node in edges:
        if to_node not in adjacency_list[from_node]:
            adjacency_list[from_node].append(to_node)
    
    # Calcula estatísticas
    total_vertices = len(nodes)
    total_edges = len(edges)
    
    # Calcula graus
    graus_entrada = {node["id"]: 0 for node in nodes}
    graus_saida = {node["id"]: len(adjacency_list[node["id"]]) for node in nodes}
    
    for from_node, to_node in edges:
        graus_entrada[to_node] += 1
    
    return {
        "estrutura": "Lista de Adjacência",
        "descricao": "Cada item mantém uma lista de itens que podem ser craftados com ele",
        "adjacency_list": adjacency_list,
        "estatisticas": {
            "total_vertices": total_vertices,
            "total_arestas": total_edges,
            "graus_entrada": graus_entrada,
            "graus_saida": graus_saida
        },
        "nodes_info": {node["id"]: {"eh_basico": node["eh_basico"], "label": node["label"]} for node in nodes}
    }


