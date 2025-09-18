class ItemCrafting:
    def __init__(self, nome, eh_basico=False):
        self.nome = nome
        self.eh_basico = eh_basico
        self.quantidade = 0


class Receita:
    def __init__(self, ingredientes, resultado, quantidade_resultado=1):
        self.ingredientes = ingredientes  # [(item, quantidade), ...]
        self.resultado = resultado
        self.quantidade_resultado = quantidade_resultado


