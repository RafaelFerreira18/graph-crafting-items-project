# Sistema de Crafting (CLI)

Projeto reestruturado para permitir cadastro de itens e receitas (craftings) e visualização do grafo via linha de comando.

## Requisitos

- Python 3.10+
- Dependências:
```
pip install -r requirements.txt
```

## Como executar

No Windows PowerShell:
```
python main.py
```

## Funcionalidades

- Adicionar item (marcando se é básico)
- Adicionar receita (ingredientes, quantidades e resultado)
- Listar itens e receitas
- Calcular itens possíveis com BFS a partir de recursos iniciais
- Estimar custo mínimo em etapas (Dijkstra simplificado)
- Exibir caminho de crafting até um item alvo
- Plotar grafo dos craftings

## Estrutura

- `crafting/models.py`: classes `ItemCrafting` e `Receita`
- `crafting/system.py`: lógica do grafo e algoritmos
- `crafting/plot.py`: função `visualizar_grafo`
- `cli.py`: menu interativo
- `main.py`: ponto de entrada

## API (FastAPI) + Frontend

### Backend

- Requisitos:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

- Configure `DATABASE_URL` (ou use padrão):
```
postgresql+psycopg2://postgres:postgres@localhost:5432/crafting
```

- Rodar API:
```
uvicorn backend.app.main:app --reload
```

Endpoints principais:
- `POST /items/` { nome, eh_basico }
- `GET  /items/`
- `POST /recipes/` { resultado_nome, quantidade_resultado, ingredientes: [{item_nome, quantidade}] }
- `GET  /recipes/`
- `GET  /graph/` -> { nodes: string[], edges: [from, to][] }
- `POST /algorithms/bfs` { recursos_iniciais }
- `POST /algorithms/cost` { item_alvo, recursos_basicos }
- `POST /algorithms/path` { item_alvo, recursos_basicos }

### Frontend

Abra `frontend/index.html` no navegador. Configure a URL da API definindo no `localStorage`:
Abra o console do navegador (F12) e execute:
```
localStorage.setItem('API_URL','http://localhost:8000')
```
Então recarregue a página.

