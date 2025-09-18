"""
Implementação de Grafo usando Lista de Adjacência
Estrutura de dados requisitada para o trabalho acadêmico.
"""

from typing import Dict, List, Set, Any
from collections import defaultdict


class ListaAdjacencia:
    """
    Implementação explícita de um grafo usando Lista de Adjacência.
    
    Esta é uma das quatro estruturas de dados para grafos estudadas:
    1. Lista de Adjacência ✅ (IMPLEMENTADA AQUI)
    2. Matriz de Adjacência
    3. Matriz de Incidência  
    4. Conjuntos
    
    A Lista de Adjacência armazena para cada vértice uma lista 
    de seus vértices adjacentes (vizinhos).
    """
    
    def __init__(self):
        """
        Inicializa a Lista de Adjacência.
        
        A estrutura interna usa um dicionário onde:
        - Chave: vértice (nome do item)
        - Valor: lista de vértices adjacentes (itens que podem ser craftados)
        """
        self._adjacencias: Dict[str, List[str]] = defaultdict(list)
        self._vertices: Set[str] = set()
    
    def adicionar_vertice(self, vertice: str) -> None:
        """Adiciona um vértice ao grafo."""
        self._vertices.add(vertice)
        if vertice not in self._adjacencias:
            self._adjacencias[vertice] = []
    
    def adicionar_aresta(self, origem: str, destino: str) -> None:
        """
        Adiciona uma aresta direcionada do vértice origem ao destino.
        No contexto de crafting: origem -> destino significa que 
        'origem' é usado para craftar 'destino'.
        """
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        
        if destino not in self._adjacencias[origem]:
            self._adjacencias[origem].append(destino)
    
    def obter_adjacentes(self, vertice: str) -> List[str]:
        """
        Retorna a lista de vértices adjacentes ao vértice dado.
        Esta é a operação fundamental da Lista de Adjacência.
        """
        return self._adjacencias.get(vertice, [])
    
    def obter_vertices(self) -> Set[str]:
        """Retorna todos os vértices do grafo."""
        return self._vertices.copy()
    
    def tem_aresta(self, origem: str, destino: str) -> bool:
        """Verifica se existe uma aresta entre origem e destino."""
        return destino in self._adjacencias.get(origem, [])
    
    def grau_saida(self, vertice: str) -> int:
        """Retorna o grau de saída do vértice (número de arestas saindo)."""
        return len(self._adjacencias.get(vertice, []))
    
    def grau_entrada(self, vertice: str) -> int:
        """Retorna o grau de entrada do vértice (número de arestas chegando)."""
        grau = 0
        for adj_list in self._adjacencias.values():
            if vertice in adj_list:
                grau += 1
        return grau
    
    def imprimir_estrutura(self) -> None:
        """
        Imprime a estrutura da Lista de Adjacência para visualização.
        Útil para fins educacionais e debugging.
        """
        print("\n=== ESTRUTURA DA LISTA DE ADJACÊNCIA ===")
        print("Formato: vértice -> [lista de adjacentes]")
        print("-" * 45)
        
        for vertice in sorted(self._vertices):
            adjacentes = self._adjacencias[vertice]
            print(f"{vertice:15} -> {adjacentes}")
        
        print(f"\nTotal de vértices: {len(self._vertices)}")
        total_arestas = sum(len(adj) for adj in self._adjacencias.values())
        print(f"Total de arestas: {total_arestas}")
        print("=" * 45)
    
    def exportar_para_dict(self) -> Dict[str, List[str]]:
        """
        Exporta a Lista de Adjacência como um dicionário Python.
        Útil para serialização e compatibilidade com código existente.
        """
        return dict(self._adjacencias)