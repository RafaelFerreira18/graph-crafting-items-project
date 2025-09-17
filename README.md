# Sistema de Crafting de Itens

Um sistema completo para gerenciar itens e receitas de crafting, com visualização de grafos e algoritmos de otimização. O projeto oferece três formas de uso: CLI, API REST e interface web.

## 🎓 **Estrutura de Dados Implementada**

**✅ LISTA DE ADJACÊNCIA** - Uma das quatro estruturas de dados para grafos estudadas em aula:

1. **Lista de Adjacência** ✅ (IMPLEMENTADA)
2. Matriz de Adjacência
3. Matriz de Incidência  
4. Conjuntos

A **Lista de Adjacência** armazena para cada vértice (item) uma lista de seus vértices adjacentes (itens que podem ser craftados). Esta implementação permite:
- ✅ Busca eficiente de dependências
- ✅ Navegação pelos caminhos de crafting
- ✅ Algoritmos de grafos (BFS, DFS, Dijkstra)
- ✅ Detecção de ciclos em receitas

## 🚀 Como Executar

### Pré-requisitos

- **Python 3.10+**
- **PostgreSQL** (apenas para a API)

### 📋 Opção 1: Interface de Linha de Comando (CLI)

A forma mais simples de começar:

```powershell
# 1. Clone o repositório
git clone <url-do-repositorio>
cd graph-crafting-items-project

# 2. Crie um ambiente virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o programa
python main.py
```

### 🌐 Opção 2: API + Interface Web

Para usar a interface web completa:

#### Backend (API)

```powershell
# 1. Entre no diretório do backend
cd backend

# 2. Crie um ambiente virtual separado
python -m venv .venv
.venv\Scripts\activate

# 3. Instale as dependências do backend
pip install -r requirements.txt

# 4. Configure o banco de dados PostgreSQL
# Crie um banco chamado 'crafting' ou configure a variável DATABASE_URL
# Padrão: postgresql+psycopg2://postgres:postgres@localhost:5432/crafting

# 5. Execute a API
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`
Documentação automática: `http://localhost:8000/docs`

#### Frontend

```powershell
# 1. Abra o arquivo frontend/index.html no seu navegador
# Ou use um servidor local simples:
cd frontend
python -m http.server 3000
# Acesse: http://localhost:3000
```

**Configuração do Frontend:**
1. Abra o console do navegador (F12)
2. Execute: `localStorage.setItem('API_URL','http://localhost:8000')`
3. Recarregue a página

**🎓 Para testar a Lista de Adjacência:**
1. Acesse a aba "📊 Lista de Adjacência" no frontend
2. Adicione alguns itens e receitas primeiro (na aba "🔧 Sistema de Crafting")
3. Clique em "🔄 Atualizar Lista de Adjacência"
4. Explore a estrutura de dados implementada!

**Exemplo com dados prontos:**
```powershell
# Execute o script de exemplo (após iniciar a API)
python criar_exemplo.py
```

## ⚡ Início Rápido

### CLI
Após executar `python main.py`, você terá um menu interativo com opções para:
- ✅ Adicionar itens básicos e craftáveis
- 📝 Criar receitas de crafting
- 🔍 Listar itens e receitas
- 🎯 Calcular itens possíveis a partir de recursos
- 💰 Estimar custos de crafting
- 🗺️ Visualizar caminhos de crafting
- 📊 Gerar gráfico interativo
- **📊 Ver estrutura da Lista de Adjacência** (opção A)

### Interface Web
A interface web oferece todas as funcionalidades do CLI de forma visual e intuitiva, além de:
- 🎨 Visualização de grafos em tempo real
- **📊 Aba dedicada à Lista de Adjacência** com:
  - Estrutura completa da Lista de Adjacência
  - Estatísticas do grafo (vértices, arestas, graus)
  - Análise detalhada por item
  - Explicação acadêmica da estrutura de dados

## 🛠️ Funcionalidades

- **Gerenciamento de Itens**: Cadastro de itens básicos e craftáveis
- **Receitas de Crafting**: Definição de ingredientes e quantidades
- **Lista de Adjacência**: Implementação explícita da estrutura de dados acadêmica
- **Algoritmos de Otimização**:
  - BFS para calcular itens possíveis
  - Dijkstra para encontrar caminhos de menor custo
  - DFS para detecção de ciclos
  - Análise de dependências de crafting
- **Visualização**: Grafos interativos dos itens e receitas
- **API REST**: Endpoints completos para integração
- **Interface Web**: Dashboard visual para gerenciamento
- **Análise Acadêmica**: Visualização da estrutura da Lista de Adjacência

## 📁 Estrutura do Projeto

```
├── main.py              # Ponto de entrada do CLI
├── cli.py               # Interface de linha de comando
├── crafting/            # Módulo principal
│   ├── models.py        # Classes ItemCrafting e Receita
│   ├── system.py        # Sistema principal com Lista de Adjacência
│   ├── grafo.py         # ✅ Implementação explícita da Lista de Adjacência
│   └── plot.py          # Visualização de grafos
├── backend/             # API FastAPI
│   └── app/
│       ├── main.py      # Aplicação FastAPI
│       ├── models.py    # Modelos de banco de dados
│       ├── schemas.py   # Schemas Pydantic
│       ├── crud.py      # Operações de banco
│       └── routers/     # Endpoints da API
└── frontend/            # Interface web
    └── index.html       # Dashboard principal
```

## 📚 **Detalhes Acadêmicos**

### Estrutura de Dados: Lista de Adjacência

O arquivo `crafting/grafo.py` contém a implementação **explícita** da Lista de Adjacência com:

- **Representação**: Dicionário onde cada chave é um vértice e o valor é uma lista de vértices adjacentes
- **Operações básicas**: Adicionar vértice, adicionar aresta, obter adjacentes
- **Análise**: Cálculo de graus de entrada e saída
- **Visualização**: Método para imprimir a estrutura completa
- **Complexidade**: O(1) para inserção, O(grau) para busca de adjacentes

### Algoritmos Implementados

- **BFS (Busca em Largura)**: Exploração de itens craftáveis usando a Lista de Adjacência
- **DFS (Busca em Profundidade)**: Detecção de ciclos nas dependências
- **Dijkstra Modificado**: Cálculo de custos mínimos de crafting

## 🔌 API Endpoints

- `GET/POST /items/` - Gerenciar itens
- `GET/POST /recipes/` - Gerenciar receitas  
- `GET /graph/` - Obter estrutura do grafo
- **`GET /graph/adjacency`** - **Obter Lista de Adjacência completa** 🎓
- `POST /algorithms/bfs` - Calcular itens possíveis
- `POST /algorithms/cost` - Estimar custos
- `POST /algorithms/path` - Encontrar caminhos ótimos

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

