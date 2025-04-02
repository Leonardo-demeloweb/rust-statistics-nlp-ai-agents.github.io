import duckdb

class DuckDBConnector:
    def __init__(self, db_path=":memory:"):
        self.conn = duckdb.connect(database=db_path)

    def execute_query(self, query: str):
        try:
            result = self.conn.execute(query).fetchall()
            return result
        except Exception as e:
            raise Exception(f"Erro ao executar query: {e}")

    def execute_and_fetch_column(self, query: str) -> list[float]:
        try:
            result = self.conn.execute(query).fetchall()
            # Extrai apenas a primeira coluna como vetor
            vector = [row[0] for row in result]
            return vector
        except Exception as e:
            raise Exception(f"Erro ao extrair vetor: {e}")

    def register_table_from_csv(self, table_name: str, file_path: str):
        try:
            query = f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv_auto('{file_path}')
            """
            self.conn.execute(query)
        except Exception as e:
            raise Exception(f"Erro ao registrar tabela: {e}")

    def get_table_schema(self, table_name: str) -> list[str]:
        try:
            query = f"DESCRIBE {table_name}"
            result = self.conn.execute(query).fetchall()
            columns = [row[0] for row in result]
            return columns
        except Exception as e:
            raise Exception(f"Erro ao extrair schema: {e}")
