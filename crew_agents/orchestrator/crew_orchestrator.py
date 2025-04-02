import logging
from crew_agents.agents.data_ingestion_agent import DataIngestionAgent
from crew_agents.agents.query_execution_agent import QueryExecutionAgent
from crew_agents.agents.nlp_to_sql_agent import NLPtoSQLAgent
from crew_agents.agents.insights_llm_agent import InsightsLLMAgent
from crew_agents.services.statistics_wasm_service import StatisticsWasmService


class CrewOrchestrator:
    """
    Orquestrador principal do pipeline de análise estatística vetorizada
    combinando NLP, SQL, WASM e LLM.
    """

    def __init__(self, db_path: str, wasm_path: str, openai_key: str):
        self.logger = logging.getLogger(__name__)

        # ✅ Agents
        self.data_ingestion_agent = DataIngestionAgent(db_path)
        self.query_execution_agent = QueryExecutionAgent(db_path)
        self.nlp_to_sql_agent = NLPtoSQLAgent(openai_key)
        self.insights_llm_agent = InsightsLLMAgent(openai_key)  # ✅ Corrigido

        # ✅ Service
        self.statistics_wasm_service = StatisticsWasmService(wasm_path)

    async def run_pipeline(self, file_path: str, question: str) -> dict:
        try:
            # 1️⃣ Ingestão de dados
            ingestion_result = await self.data_ingestion_agent.run(file_path)
            if ingestion_result["status"] != "success":
                return ingestion_result

            table_name = ingestion_result["table"]
            self.logger.info(f"✅ Dados ingeridos na tabela '{table_name}'.")

            # 2️⃣ Schema
            schema_result = await self.query_execution_agent.get_table_schema(table_name)
            if schema_result["status"] != "success":
                return schema_result

            schema = schema_result["schema"]

            # 3️⃣ NLP → SQL
            nlp_result = await self.nlp_to_sql_agent.process(question, table_name, schema)
            if nlp_result["status"] != "success":
                return nlp_result

            query = nlp_result["query"]
            self.logger.info(f"✅ Query SQL gerada: {query}")

            # 4️⃣ Executar query e extrair vetor
            query_result = await self.query_execution_agent.process(query)
            if query_result["status"] != "success":
                return query_result

            vector = query_result["vector"]

            # 5️⃣ Estatísticas via WASM
            stats_result = await self.statistics_wasm_service.process(vector)
            if stats_result["status"] != "success":
                return stats_result

            statistics = stats_result["statistics"]

            # 6️⃣ Insight via LLM
            insights_result = await self.insights_llm_agent.process(statistics)
            if insights_result["status"] != "success":
                return insights_result

            insight = insights_result["insight"]

            # ✅ Retorno final
            return {
                "status": "success",
                "table": table_name,
                "query": query,
                "statistics": statistics,
                "insight": insight
            }

        except Exception as e:
            self.logger.error(f"❌ Erro no CrewOrchestrator: {str(e)}")
            return {"status": "error", "error": str(e)}
