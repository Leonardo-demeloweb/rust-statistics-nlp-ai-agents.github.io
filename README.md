

# 📊 Stat Rust Engine — Business Insights Pipeline

Pipeline modular e escalável para ingestão, análise estatística vetorizada e geração de insights estratégicos utilizando Python, Rust (via WASM) e LLMs locais.

---

## 🚀 Arquitetura

```
stat-rust-engine/
├── api/
│   └── main.py                 # FastAPI para exposição dos endpoints
├── crew_agents/
│   ├── agents/                 # Agentes inteligentes
│   │   ├── data_ingestion_agent.py
│   │   ├── query_execution_agent.py
│   │   ├── nlp_to_sql_agent.py
│   │   └── insights_llm_agent.py
│   ├── orchestrator/
│   │   └── crew_orchestrator.py
│   └── services/
│       └── statistics_wasm_service.py
├── db.py                       # Conector DuckDB
├── rust_module/
│   ├── Cargo.toml
│   ├── src/
│   │   ├── main.rs             # Execução via stdin/stdout (WASI)
│   │   └── statistics.rs      # Lógica de cálculo estatístico
│   └── target/
│       └── wasm32-wasi/
│           └── release/
│               └── stat_rust_engine.wasm
├── requirements.txt            # Dependências Python
└── README.md                   # 📄 Você está aqui
```

---

## 🧩 Componentes e Fluxo

1️⃣ **Data Ingestion Agent**  
Ingestão de arquivos CSV, registrando dinamicamente tabelas no DuckDB.

2️⃣ **Query Execution Agent**  
Executa queries SQL simples e extrai vetores numéricos.

3️⃣ **NLP to SQL Agent (SLM Fine-tuned)**  
Converte perguntas em linguagem natural para consultas SQL simples utilizando o modelo local **Text2SQL-1.5B** fine-tuned:

- **Modelo utilizado:** [`yasserrmd/text2sql-1.5b`](https://ollama.com/yasserrmd/Text2SQL-1.5B)  
- 🚫 **Funções agregadas bloqueadas** (AVG, MIN, MAX, etc.) → cálculo sempre delegado ao módulo Rust.

4️⃣ **Statistics WASM Service**  
Processa vetores utilizando o módulo **Rust WASM** nativo, garantindo:

✅ Performance até **12x superior ao Pandas**  
✅ Execução vetorizada e mínima latência  
✅ Baixíssimo custo computacional (WASM)

5️⃣ **Insights LLM Agent**  
Recebe o output estatístico e gera insights automáticos em linguagem natural utilizando modelo LLM local ou remoto.

---

## 🔥 Exemplo de Pipeline

```bash
curl -X POST "http://localhost:8000/upload_and_analyze/" \
     -F "file=@/caminho/para/dataset.csv" \
     -F "question=Qual foi o nível de água registrado ao longo do tempo?"
```

**Resposta:**
```json
{
  "status": "success",
  "table": "leituras_sensores_csv",
  "query": "SELECT nivel_agua FROM leituras_sensores_csv;",
  "statistics": {
    "min": 23.4,
    "max": 98.7,
    "mean": 56.2,
    "median": 54.9,
    "q1": 45.1,
    "q3": 66.3,
    "std_dev": 12.4,
    "coef_var": 22.1
  },
  "insight": "Os dados indicam uma grande variação no nível de água, sugerindo..."
}
```

---

## ⚙️ Como rodar localmente

### 1. Instale o ambiente Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure o arquivo `.env`

Crie um arquivo `.env`:

```env
OPENAI_API_KEY=your_key_if_needed
```

*(Se estiver usando apenas modelo local não precisa dessa key)*

### 3. Instale e rode o Ollama + modelo Text2SQL

```bash
# Instale o Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Inicie o servidor Ollama
ollama serve

# Baixe o modelo Text2SQL
ollama pull yasserrmd/text2sql-1.5b:latest

# Valide o modelo
ollama list
```

---

## 🟢 Justificativa Arquitetural — Delegação do Processamento Estatístico

Apesar do DuckDB possuir suporte a funções agregadas básicas (`AVG()`, `STDDEV()`, `MAX()`, etc.), optamos por **não utilizar funções agregadas SQL** neste projeto, por decisão arquitetural estratégica:

✅ Garantir **segurança e previsibilidade** — Evitando queries maliciosas ou incorretas  
✅ Separar claramente responsabilidades — SQL apenas para projeção, filtro e schema discovery  
✅ Delegar cálculos vetorizados ao módulo **Rust + WASM** para obter:

- **Performance consistente e mínima latência**
- **Capacidade de expansão para cálculos complexos**
- **Execução controlada e auditável**

### Exemplos de Cálculos Não Viáveis no SQL:
- **Coeficiente de Variação ajustado para outliers**
- **Normalização vetorial por faixas dinâmicas**
- **Estatísticas condicionais (ex.: com masking ou censura)**
- **Cálculos com alto volume vetorizado em Edge Computing**

---

## ✅ Resultados Obtidos

Testes realizados com datasets reais demonstraram:

- 🔥 **Redução do tempo de análise em até 12x versus Pandas**
- ⏱️ **Latência mínima em consultas com até 1 milhão de registros (<100ms)**
- 🤖 **Interpretação automática e geração de insights via LLM**
- 🔀 **Pipeline modular, escalável e independente de ambiente**
- 🌐 **Alta portabilidade (Web, Backend ou Edge)**

---
Aqui está a versão traduzida para inglês do seu README, mantendo toda a estrutura, clareza e boas práticas de documentação:

---

English version:

# 📊 Stat Rust Engine — Business Insights Pipeline

A modular and scalable pipeline for ingestion, vectorized statistical analysis, and strategic insight generation using Python, Rust (via WASM), and local LLMs.

---

## 🚀 Architecture

```
stat-rust-engine/
├── api/
│   └── main.py                 # FastAPI to expose API endpoints
├── crew_agents/
│   ├── agents/                 # Intelligent agents
│   │   ├── data_ingestion_agent.py
│   │   ├── query_execution_agent.py
│   │   ├── nlp_to_sql_agent.py
│   │   └── insights_llm_agent.py
│   ├── orchestrator/
│   │   └── crew_orchestrator.py
│   └── services/
│       └── statistics_wasm_service.py
├── db.py                       # DuckDB connector
├── rust_module/
│   ├── Cargo.toml
│   ├── src/
│   │   ├── main.rs             # Execution via stdin/stdout (WASI)
│   │   └── statistics.rs      # Statistical calculation logic
│   └── target/
│       └── wasm32-wasi/
│           └── release/
│               └── stat_rust_engine.wasm
├── requirements.txt            # Python dependencies
└── README.md                   # 📄 You are here
```

---

## 🧩 Components & Workflow

1️⃣ **Data Ingestion Agent**  
Ingests CSV files, dynamically registering tables in DuckDB.

2️⃣ **Query Execution Agent**  
Executes simple SQL queries and extracts numerical vectors.

3️⃣ **NLP to SQL Agent (Fine-Tuned SLM)**  
Converts natural language questions into simple SQL queries using the local fine-tuned model **Text2SQL-1.5B**:

- **Model used:** [`yasserrmd/text2sql-1.5b`](https://ollama.com/yasserrmd/Text2SQL-1.5B)  
- 🚫 **Aggregate functions are blocked** (AVG, MIN, MAX, etc.) → all calculations are delegated to the Rust module.

4️⃣ **Statistics WASM Service**  
Processes numeric vectors using the native **Rust WASM** module, ensuring:

✅ Up to **12x better performance than Pandas**  
✅ Vectorized execution with minimal latency  
✅ Very low computational cost (WASM)

5️⃣ **Insights LLM Agent**  
Receives statistical output and automatically generates strategic insights in natural language using a local or remote LLM model.

---

## 🔥 Example Pipeline Execution

```bash
curl -X POST "http://localhost:8000/upload_and_analyze/" \
     -F "file=@/path/to/dataset.csv" \
     -F "question=What was the recorded water level over time?"
```

**Response:**
```json
{
  "status": "success",
  "table": "leituras_sensores_csv",
  "query": "SELECT nivel_agua FROM leituras_sensores_csv;",
  "statistics": {
    "min": 23.4,
    "max": 98.7,
    "mean": 56.2,
    "median": 54.9,
    "q1": 45.1,
    "q3": 66.3,
    "std_dev": 12.4,
    "coef_var": 22.1
  },
  "insight": "The data shows a large variation in water level, suggesting..."
}
```

---

## ⚙️ How to Run Locally

### 1. Set up the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure `.env` file

Create a `.env` file:

```env
OPENAI_API_KEY=your_key_if_needed
```

*(If using only local models, this key is optional)*

### 3. Install and run Ollama + Text2SQL model

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve

# Download the Text2SQL model
ollama pull yasserrmd/text2sql-1.5b:latest

# Validate available models
ollama list
```

---

## 🟢 Architectural Justification — Statistical Processing Delegation

Although DuckDB supports basic aggregate functions (`AVG()`, `STDDEV()`, `MAX()`, etc.), we chose **not to use aggregate SQL functions** in this project, as part of a deliberate architectural decision:

✅ Ensure **security and predictability** — Preventing malicious or incorrect queries  
✅ Clear separation of responsibilities — SQL is used only for projection, filtering, and schema discovery  
✅ Delegate vectorized calculations to the **Rust + WASM** module to achieve:

- **Consistent performance and minimal latency**
- **Scalability for complex calculations**
- **Controlled and auditable execution**

### Examples of Calculations Not Suitable for SQL:
- **Adjusted Coefficient of Variation for outliers**
- **Dynamic range-based vector normalization**
- **Conditional statistics (e.g., masking or data censoring)**
- **High-volume vectorized processing in Edge Computing**

---

## ✅ Results Achieved

Tests conducted with real datasets demonstrated:

- 🔥 **Up to 12x reduction in analysis time compared to Pandas**
- ⏱️ **Minimal latency on queries with up to 1 million records (<100ms)**
- 🤖 **Automatic interpretation and insight generation via LLM**
- 🔀 **Modular, scalable, and environment-independent pipeline**
- 🌐 **High portability (Web, Backend, or Edge)**

