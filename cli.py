from crafting.system import SistemaCrafting
from crafting.plot import visualizar_grafo, visualizar_grafo_interativo


def perguntar_bool(msg: str) -> bool:
    resp = input(msg + " (s/n): ").strip().lower()
    return resp in {"s", "sim", "y", "yes"}


def perguntar_int(msg: str, default: int = None) -> int:
    while True:
        valor = input(msg + (f" [{default}]" if default is not None else "") + ": ").strip()
        if not valor and default is not None:
            return default
        try:
            return int(valor)
        except ValueError:
            print("Por favor, digite um número inteiro válido.")


def adicionar_item_cli(sistema: SistemaCrafting):
    nome = input("Nome do item: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return
    eh_basico = perguntar_bool("É um recurso básico?")
    sistema.adicionar_item(nome, eh_basico=eh_basico)
    print(f"Item '{nome}' adicionado.")


def adicionar_receita_cli(sistema: SistemaCrafting):
    resultado = input("Nome do item resultante: ").strip()
    if not resultado:
        print("Resultado não pode ser vazio.")
        return
    qtd_resultado = perguntar_int("Quantidade resultante", default=1)

    ingredientes = []
    print("Adicione ingredientes (deixe o nome vazio para terminar):")
    while True:
        nome_ing = input("- Ingrediente: ").strip()
        if not nome_ing:
            break
        qtd = perguntar_int("  Quantidade", default=1)
        ingredientes.append((nome_ing, qtd))

    if not ingredientes:
        print("A receita precisa de pelo menos um ingrediente.")
        return

    sistema.adicionar_receita(ingredientes, resultado, qtd_resultado=qtd_resultado)
    print(f"Receita para '{resultado}' adicionada.")


def listar_itens_cli(sistema: SistemaCrafting):
    if not sistema.itens:
        print("Nenhum item cadastrado.")
        return
    print("Itens:")
    for nome, item in sistema.itens.items():
        tipo = "básico" if item.eh_basico else "craftável"
        print(f"- {nome} ({tipo})")


def listar_receitas_cli(sistema: SistemaCrafting):
    if not sistema.receitas:
        print("Nenhuma receita cadastrada.")
        return
    print("Receitas:")
    for r in sistema.receitas:
        ing_str = ", ".join(f"{n} x{q}" for n, q in r.ingredientes)
        print(f"- {ing_str} -> {r.resultado} x{r.quantidade_resultado}")


def calcular_bfs_cli(sistema: SistemaCrafting):
    print("Recursos iniciais (deixe o nome vazio para terminar):")
    recursos = {}
    while True:
        nome = input("- Recurso: ").strip()
        if not nome:
            break
        qtd = perguntar_int("  Quantidade", default=1)
        recursos[nome] = qtd
    possiveis = sistema.bfs_itens_possiveis(recursos)
    print("Itens possíveis:")
    for it in possiveis:
        print(f"- {it}")


def calcular_custo_cli(sistema: SistemaCrafting):
    alvo = input("Item alvo: ").strip()
    basicos = input("Recursos básicos (separados por vírgula): ").strip()
    lista = [s.strip() for s in basicos.split(",") if s.strip()]
    custo = sistema.dijkstra_custo_minimo(alvo, lista)
    if custo == float('inf'):
        print("Impossível craftar com os dados atuais.")
    else:
        print(f"Custo mínimo (em etapas): {custo}")


def caminho_cli(sistema: SistemaCrafting):
    alvo = input("Item alvo: ").strip()
    basicos = input("Recursos básicos (separados por vírgula): ").strip()
    lista = [s.strip() for s in basicos.split(",") if s.strip()]
    caminho = sistema.caminho_crafting(alvo, lista)
    if not caminho:
        print("Caminho não encontrado.")
    else:
        print(" -> ".join(caminho))


def menu():
    sistema = SistemaCrafting()
    acoes = {
        "1": ("Adicionar item", adicionar_item_cli),
        "2": ("Adicionar receita", adicionar_receita_cli),
        "3": ("Listar itens", listar_itens_cli),
        "4": ("Listar receitas", listar_receitas_cli),
        "5": ("Calcular itens possíveis (BFS)", calcular_bfs_cli),
        "6": ("Calcular custo mínimo (Dijkstra)", calcular_custo_cli),
        "7": ("Ver caminho de crafting", caminho_cli),
        "8": ("Plotar grafo (estático)", lambda s: visualizar_grafo(s)),
        "9": ("Plotar grafo (interativo)", lambda s: visualizar_grafo_interativo(s)),
        "0": ("Sair", None),
    }

    while True:
        print("\n=== Sistema de Crafting ===")
        for k in sorted(acoes.keys()):
            print(f"{k} - {acoes[k][0]}")
        escolha = input("Escolha: ").strip()

        if escolha == "0":
            print("Saindo...")
            break
        acao = acoes.get(escolha)
        if not acao:
            print("Opção inválida.")
            continue
        func = acao[1]
        if func:
            func(sistema)


if __name__ == "__main__":
    menu()


