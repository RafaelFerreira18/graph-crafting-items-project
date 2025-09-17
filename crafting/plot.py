import matplotlib.pyplot as plt
import networkx as nx


def visualizar_grafo(sistema):
    G = nx.DiGraph()

    for item in sistema.itens:
        G.add_node(
            item,
            color='lightgreen' if sistema.itens[item].eh_basico else 'lightblue',
        )

    for receita in sistema.receitas:
        for ingrediente, _ in receita.ingredientes:
            G.add_edge(ingrediente, receita.resultado)

    pos = nx.spring_layout(G)
    colors = [G.nodes[node]['color'] for node in G.nodes()]

    nx.draw(
        G,
        pos,
        node_color=colors,
        with_labels=True,
        node_size=1500,
        font_size=10,
        arrows=True,
    )
    plt.title("Grafo de Crafting")
    plt.show()


def visualizar_grafo_interativo(sistema, saida_html="grafo_interativo.html", abrir=True):
    try:
        from pyvis.network import Network
    except ImportError:
        raise RuntimeError("pyvis não está instalado. Instale com: pip install pyvis")

    net = Network(height="700px", width="100%", directed=True, notebook=False)
    net.toggle_physics(True)

    for nome, item in sistema.itens.items():
        cor = "#90EE90" if item.eh_basico else "#ADD8E6"
        net.add_node(nome, label=nome, color=cor)

    for receita in sistema.receitas:
        for ingrediente, _ in receita.ingredientes:
            net.add_edge(ingrediente, receita.resultado, arrows="to")

    # Evita usar show() (problema de template em algumas instalações do pyvis)
    net.write_html(saida_html, notebook=False)

    if abrir:
        import webbrowser
        webbrowser.open(saida_html)


