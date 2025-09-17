from collections import deque, defaultdict

from .models import ItemCrafting, Receita
from .grafo import ListaAdjacencia


class SistemaCrafting:
    """
    Sistema de Crafting implementado usando Lista de Adjacência.
    
    ESTRUTURA DE DADOS UTILIZADA: Lista de Adjacência
    - Esta é uma das quatro estruturas para grafos estudadas em aula
    - Cada item mantém uma lista de itens que podem ser craftados com ele
    - Permite busca eficiente de dependências e caminhos de crafting
    """
    
    def __init__(self):
        self.itens = {}
        self.receitas = []
        
        # IMPLEMENTAÇÃO DA LISTA DE ADJACÊNCIA
        # Utilizamos duas listas para representar o grafo de crafting:
        self.grafo_direto = ListaAdjacencia()    # item -> itens que podem ser craftados
        self.grafo_inverso = defaultdict(list)   # item -> receitas que o produzem
        
        # Para fins acadêmicos, mantemos também uma versão mais simples:
        self._adjacencias_simples = defaultdict(list)  # Backup da estrutura básica

    def adicionar_item(self, nome, eh_basico=False):
        """Adiciona um item ao sistema e ao grafo (Lista de Adjacência)."""
        if nome not in self.itens:
            self.itens[nome] = ItemCrafting(nome, eh_basico)
            # Adiciona o vértice na Lista de Adjacência
            self.grafo_direto.adicionar_vertice(nome)

    def adicionar_receita(self, ingredientes, resultado, qtd_resultado=1):
        """
        Adiciona uma receita e atualiza a Lista de Adjacência.
        
        Para cada ingrediente -> resultado, cria uma aresta na Lista de Adjacência.
        """
        # Garante que todos os itens existem
        for item, _ in ingredientes:
            self.adicionar_item(item)
        self.adicionar_item(resultado)

        receita = Receita(ingredientes, resultado, qtd_resultado)
        self.receitas.append(receita)

        # Atualiza o grafo inverso (para busca de receitas)
        self.grafo_inverso[resultado].append(receita)

        # ATUALIZA A LISTA DE ADJACÊNCIA
        # Adiciona arestas: cada ingrediente pode levar ao resultado
        for item, _ in ingredientes:
            self.grafo_direto.adicionar_aresta(item, resultado)
            # Backup na estrutura simples
            if resultado not in self._adjacencias_simples[item]:
                self._adjacencias_simples[item].append(resultado)

    def bfs_itens_possiveis(self, recursos_iniciais):
        """
        Busca em Largura (BFS) usando a Lista de Adjacência.
        
        Demonstra o uso prático da Lista de Adjacência para explorar
        todos os itens que podem ser craftados a partir dos recursos iniciais.
        """
        fila = deque()
        recursos_disponiveis = recursos_iniciais.copy()
        itens_criados = set(recursos_iniciais.keys())

        for item in recursos_iniciais:
            fila.append(item)

        while fila:
            item_atual = fila.popleft()

            # USA A LISTA DE ADJACÊNCIA para obter itens craftáveis
            for proximo_item in self.grafo_direto.obter_adjacentes(item_atual):
                if proximo_item not in itens_criados:
                    if self._pode_craftar(proximo_item, recursos_disponiveis):
                        itens_criados.add(proximo_item)
                        fila.append(proximo_item)
                        recursos_disponiveis[proximo_item] = float('inf')

        return list(itens_criados)

    def _pode_craftar(self, item, recursos):
        for receita in self.grafo_inverso[item]:
            pode_fazer = True
            for ingrediente, qtd in receita.ingredientes:
                if ingrediente not in recursos or recursos[ingrediente] < qtd:
                    pode_fazer = False
                    break
            if pode_fazer:
                return True
        return False

    def dijkstra_custo_minimo(self, item_alvo, recursos_basicos):
        """
        Algoritmo de Dijkstra usando a Lista de Adjacência.
        
        Demonstra como a Lista de Adjacência facilita a exploração
        de vizinhos para calcular distâncias mínimas.
        """
        distancia = {item: float('inf') for item in self.itens}

        for recurso in recursos_basicos:
            distancia[recurso] = 0

        visitados = set()

        while len(visitados) < len(self.itens):
            min_dist = float('inf')
            min_item = None

            for item in self.itens:
                if item not in visitados and distancia[item] < min_dist:
                    min_dist = distancia[item]
                    min_item = item

            if min_item is None:
                break

            visitados.add(min_item)

            # USA A LISTA DE ADJACÊNCIA para obter vizinhos
            for vizinho in self.grafo_direto.obter_adjacentes(min_item):
                nova_distancia = distancia[min_item] + 1
                if nova_distancia < distancia[vizinho]:
                    distancia[vizinho] = nova_distancia

        return distancia.get(item_alvo, float('inf'))

    def caminho_crafting(self, item_alvo, recursos_basicos):
        if item_alvo in recursos_basicos:
            return []

        fila = deque([(item_alvo, [item_alvo])])
        visitados = {item_alvo}

        while fila:
            item_atual, caminho = fila.popleft()

            for receita in self.grafo_inverso[item_atual]:
                todos_basicos = True

                for ingrediente, _ in receita.ingredientes:
                    if ingrediente not in recursos_basicos:
                        todos_basicos = False
                        if ingrediente not in visitados:
                            visitados.add(ingrediente)
                            fila.append((ingrediente, [ingrediente] + caminho))

                if todos_basicos:
                    return caminho

        return None

    def detectar_ciclos(self):
        """
        Detecção de ciclos usando DFS na Lista de Adjacência.
        
        Demonstra como a Lista de Adjacência permite navegação
        eficiente para detectar dependências circulares.
        """
        cores = {item: 'branco' for item in self.itens}
        tem_ciclo = False

        def dfs(item):
            nonlocal tem_ciclo
            cores[item] = 'cinza'

            # USA A LISTA DE ADJACÊNCIA para obter vizinhos
            for vizinho in self.grafo_direto.obter_adjacentes(item):
                if cores[vizinho] == 'cinza':
                    tem_ciclo = True
                    return
                elif cores[vizinho] == 'branco':
                    dfs(vizinho)

            cores[item] = 'preto'

        for item in self.itens:
            if cores[item] == 'branco':
                dfs(item)

        return tem_ciclo
    
    def imprimir_estrutura_grafo(self):
        """
        Método para visualizar a Lista de Adjacência.
        Útil para fins educacionais e verificação da estrutura.
        """
        print("\n" + "="*60)
        print("🔧 ESTRUTURA DE DADOS: LISTA DE ADJACÊNCIA")
        print("="*60)
        print("Implementação utilizada para atender ao requisito acadêmico.")
        print("Cada item mantém uma lista de itens que podem ser craftados.")
        print("="*60)
        
        self.grafo_direto.imprimir_estrutura()
        
        print("\n📊 ESTATÍSTICAS DO GRAFO:")
        vertices = self.grafo_direto.obter_vertices()
        print(f"• Total de itens (vértices): {len(vertices)}")
        print(f"• Total de receitas: {len(self.receitas)}")
        
        if vertices:
            print(f"\n📋 ANÁLISE POR ITEM:")
            for item in sorted(vertices):
                grau_saida = self.grafo_direto.grau_saida(item)
                grau_entrada = self.grafo_direto.grau_entrada(item)
                eh_basico = self.itens[item].eh_basico if item in self.itens else False
                tipo = "BÁSICO" if eh_basico else "CRAFTÁVEL"
                print(f"  {item:15} | {tipo:10} | Saída: {grau_saida} | Entrada: {grau_entrada}")
        
        print("="*60)


