import duckdb
import numpy as np
import logging
from crewai import Agent


class QueryExecutionAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.agent = Agent(
            role="SQL Executor",
            goal="Executar query SQL, extrair vetor numérico e fornecer metadados da tabela",
            backstory="Agente especializado na execução de queries SQL no DuckDB, extração de vetores numéricos e recuperação dinâmica do schema."
        )

    async def process(self, query: str) -> dict:
        try:
            # Conexão e execução
            conn = duckdb.connect(self.db_path)
            self.logger.info(f"📄 Executando query: {query}")
            result = conn.execute(query).fetchall()
            conn.close()

            if not result:
                raise ValueError("Query não retornou resultados.")

            # Extração apenas de dados numéricos
            vector = []
            for row in result:
                try:
                    value = float(row[0])
                    vector.append(value)
                except (ValueError, TypeError):
                    continue  # Ignora valores não numéricos

            if not vector:
                raise ValueError("Nenhum valor numérico encontrado no resultado da query.")

            np_vector = np.array(vector, dtype=np.float64)

            self.logger.info(f"✅ Vetor extraído com {len(vector)} elementos numéricos.")

            return {"status": "success", "vector": np_vector.tolist()}

        except Exception as e:
            self.logger.error(f"❌ Erro ao executar query: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def get_table_schema(self, table_name: str) -> dict:
        """
        Retorna as colunas e tipos da tabela informada.
        """
        try:
            conn = duckdb.connect(self.db_path)
            self.logger.info(f"📄 Obtendo schema da tabela: {table_name}")

            query = f"PRAGMA table_info('{table_name}')"
            result = conn.execute(query).fetchall()
            conn.close()

            if not result:
                raise ValueError(f"Tabela '{table_name}' não encontrada.")

            schema = [{"name": row[1], "type": row[2]} for row in result]

            self.logger.info(f"✅ Schema extraído: {[col['name'] for col in schema]}")

            return {"status": "success", "schema": schema}

        except Exception as e:
            self.logger.error(f"❌ Erro ao obter schema: {str(e)}")
            return {"status": "error", "error": str(e)}
