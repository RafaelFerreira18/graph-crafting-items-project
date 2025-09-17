"""
Script de teste para verificar a Lista de Adjacência no frontend
Execute este script para popular o sistema com dados de exemplo
"""

import requests
import json

# URL da API (ajuste se necessário)
API_BASE = "http://localhost:8000"

def criar_dados_exemplo():
    """Cria dados de exemplo para demonstrar a Lista de Adjacência"""
    
    # Itens básicos
    itens_basicos = [
        {"nome": "Madeira", "eh_basico": True},
        {"nome": "Ferro", "eh_basico": True},
        {"nome": "Pedra", "eh_basico": True},
        {"nome": "Couro", "eh_basico": True}
    ]
    
    # Itens craftáveis
    itens_craftaveis = [
        {"nome": "Tábua", "eh_basico": False},
        {"nome": "Cabo de Madeira", "eh_basico": False},
        {"nome": "Lâmina de Ferro", "eh_basico": False},
        {"nome": "Espada de Ferro", "eh_basico": False},
        {"nome": "Escudo", "eh_basico": False},
        {"nome": "Armadura", "eh_basico": False}
    ]
    
    # Receitas
    receitas = [
        {
            "resultado_nome": "Tábua",
            "quantidade_resultado": 4,
            "ingredientes": [{"item_nome": "Madeira", "quantidade": 1}]
        },
        {
            "resultado_nome": "Cabo de Madeira", 
            "quantidade_resultado": 2,
            "ingredientes": [{"item_nome": "Tábua", "quantidade": 2}]
        },
        {
            "resultado_nome": "Lâmina de Ferro",
            "quantidade_resultado": 1,
            "ingredientes": [{"item_nome": "Ferro", "quantidade": 2}]
        },
        {
            "resultado_nome": "Espada de Ferro",
            "quantidade_resultado": 1,
            "ingredientes": [
                {"item_nome": "Lâmina de Ferro", "quantidade": 1},
                {"item_nome": "Cabo de Madeira", "quantidade": 1}
            ]
        },
        {
            "resultado_nome": "Escudo",
            "quantidade_resultado": 1,
            "ingredientes": [
                {"item_nome": "Madeira", "quantidade": 3},
                {"item_nome": "Ferro", "quantidade": 1}
            ]
        },
        {
            "resultado_nome": "Armadura",
            "quantidade_resultado": 1,
            "ingredientes": [
                {"item_nome": "Ferro", "quantidade": 5},
                {"item_nome": "Couro", "quantidade": 2}
            ]
        }
    ]
    
    print("🔧 Criando dados de exemplo para a Lista de Adjacência...")
    
    # Criar itens
    for item in itens_basicos + itens_craftaveis:
        try:
            response = requests.post(f"{API_BASE}/items/", json=item)
            if response.status_code == 200:
                print(f"✅ Item criado: {item['nome']}")
            else:
                print(f"⚠️  Item já existe ou erro: {item['nome']}")
        except Exception as e:
            print(f"❌ Erro ao criar item {item['nome']}: {e}")
    
    # Criar receitas
    for receita in receitas:
        try:
            response = requests.post(f"{API_BASE}/recipes/", json=receita)
            if response.status_code == 200:
                print(f"✅ Receita criada: {receita['resultado_nome']}")
            else:
                print(f"⚠️  Receita já existe ou erro: {receita['resultado_nome']}")
        except Exception as e:
            print(f"❌ Erro ao criar receita {receita['resultado_nome']}: {e}")
    
    print("\n🎓 Dados de exemplo criados! Agora você pode:")
    print("1. Abrir o frontend: frontend/index.html")
    print("2. Ir para a aba 'Lista de Adjacência'")
    print("3. Clicar em 'Atualizar Lista de Adjacência'")
    print("4. Explorar a estrutura de dados implementada!")
    
    print(f"\n📊 Para verificar via API:")
    print(f"GET {API_BASE}/graph/adjacency")

if __name__ == "__main__":
    criar_dados_exemplo()