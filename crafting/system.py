from collections import deque, defaultdict

from .models import ItemCrafting, Receita


class SistemaCrafting:
    def __init__(self):
        self.itens = {}
        self.receitas = []
        self.grafo_inverso = defaultdict(list)
        self.grafo_direto = defaultdict(list)

    def adicionar_item(self, nome, eh_basico=False):
        if nome not in self.itens:
            self.itens[nome] = ItemCrafting(nome, eh_basico)

    def adicionar_receita(self, ingredientes, resultado, qtd_resultado=1):
        for item, _ in ingredientes:
            self.adicionar_item(item)
        self.adicionar_item(resultado)

        receita = Receita(ingredientes, resultado, qtd_resultado)
        self.receitas.append(receita)

        self.grafo_inverso[resultado].append(receita)

        for item, _ in ingredientes:
            if resultado not in self.grafo_direto[item]:
                self.grafo_direto[item].append(resultado)

    def bfs_itens_possiveis(self, recursos_iniciais):
        fila = deque()
        recursos_disponiveis = recursos_iniciais.copy()
        itens_criados = set(recursos_iniciais.keys())

        for item in recursos_iniciais:
            fila.append(item)

        while fila:
            item_atual = fila.popleft()

            for proximo_item in self.grafo_direto[item_atual]:
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

            for vizinho in self.grafo_direto[min_item]:
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
        cores = {item: 'branco' for item in self.itens}
        tem_ciclo = False

        def dfs(item):
            nonlocal tem_ciclo
            cores[item] = 'cinza'

            for vizinho in self.grafo_direto[item]:
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


