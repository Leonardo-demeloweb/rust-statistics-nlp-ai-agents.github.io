import logging
from openai import OpenAI
from crewai import Agent


class NLPtoSQLAgent:
    """
    Agent responsável por converter perguntas em linguagem natural para consultas SQL.
    """

    def __init__(self, openai_api_key: str):
        self.logger = logging.getLogger(__name__)
        self.agent = Agent(
            role="NLP-to-SQL Translator",
            goal="Converter perguntas em linguagem natural para consultas SQL simples",
            backstory=(
                "Especialista em converter perguntas de linguagem natural em consultas SQL básicas "
                "que retornem colunas específicas para posterior análise estatística."
            )
        )
        self.client = OpenAI(api_key=openai_api_key)

    async def process(self, question: str, table_name: str, columns: list) -> dict:
        try:
            # 📄 Monta prompt dinâmico
            col_names = ", ".join([col["name"] for col in columns])
            prompt = (
                f"Converta a seguinte pergunta em uma consulta SQL válida.\n"
                f"Pergunta: \"{question}\"\n"
                f"Tabela: \"{table_name}\"\n"
                f"Colunas disponíveis: {col_names}\n"
                "Restrições:\n"
                "- Use apenas instruções SELECT.\n"
                "- Não utilize funções agregadas (AVG, MIN, MAX, STDDEV, MEDIAN, etc).\n"
                "- A query deve retornar apenas os dados brutos para posterior análise.\n"
                "- Não utilize DELETE, DROP, UPDATE ou INSERT.\n"
                "- Não gere explicações, apenas a query."
                "Apenas retorne a query SQL pura, sem explicações, sem comentários."
            )

            # 🚀 Chamada ao LLM (OpenAI API 1.0+)
            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            query = completion.choices[0].message.content.strip()

            # ✅ Validação de segurança
            query_clean = query.lower().strip()
            if not query_clean.startswith("select"):
                raise ValueError(f"Query inválida, não começa com SELECT: {query}")
            if any(keyword in query.upper() for keyword in ["DROP", "DELETE", "UPDATE", "INSERT"]):
                raise ValueError(f"Query contém instruções perigosas: {query}")

            self.logger.info(f"✅ Query SQL gerada e validada: {query}")

            return {"status": "success", "query": query}

        except Exception as e:
            self.logger.error(f"❌ Erro no NLPtoSQLAgent: {str(e)}")
            return {"status": "error", "error": str(e)}
