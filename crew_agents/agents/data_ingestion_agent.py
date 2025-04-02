from crewai import Agent, Task
import duckdb
import os
import logging
import pandas as pd


class DataIngestionAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.agent = Agent(
            role="Data Ingestor",
            goal="Realizar ingestão de arquivos tabulares no DuckDB",
            backstory="Este agente é responsável por receber dados em formato CSV, XLSX ou JSON e armazená-los no banco DuckDB de forma dinâmica e eficiente."
        )

    async def run(self, file_path: str) -> dict:
        try:
            file_ext = file_path.split(".")[-1].lower()
            table_name = os.path.basename(file_path).replace(".", "_").lower()
            conn = duckdb.connect(self.db_path)

            if file_ext == "csv":
                conn.execute(f"""
                    CREATE OR REPLACE TABLE {table_name} AS
                    SELECT * FROM read_csv_auto('{file_path}')
                """)
            elif file_ext == "xlsx":
                conn.execute(f"""
                    CREATE OR REPLACE TABLE {table_name} AS
                    SELECT * FROM read_excel('{file_path}')
                """)
            elif file_ext == "json":
                df = pd.read_json(file_path)
                conn.register(table_name, df)
            else:
                raise ValueError(f"Formato {file_ext} não suportado.")

            conn.close()
            self.logger.info(f"✅ Ingestão concluída para tabela '{table_name}'")
            return {"status": "success", "table": table_name}

        except Exception as e:
            self.logger.error(f"❌ Erro na ingestão: {str(e)}")
            return {"status": "error", "error": str(e)}
