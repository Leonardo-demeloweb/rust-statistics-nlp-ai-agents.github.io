import json
import logging
from openai import OpenAI
from crewai import Agent
from pydantic import PrivateAttr


class InsightsLLMAgent(Agent):
    """
    Agent responsável por interpretar métricas estatísticas e gerar insights estratégicos
    utilizando LLM (OpenAI).
    """

    _logger: logging.Logger = PrivateAttr()
    _openai_key: str = PrivateAttr()

    def __init__(self, openai_key: str):
        # ✅ Inicializa o Agent com atributos obrigatórios do CrewAI (pydantic model)
        super().__init__(
            role="Insights Generator",
            goal="Interpretar métricas estatísticas e gerar insights estratégicos",
            backstory=(
                "Especialista em análise e comunicação de resultados estatísticos, "
                "capaz de gerar insights claros e úteis para tomada de decisão."
            )
        )
        # ✅ Atributos privados para evitar conflito com Pydantic V2
        self._logger = logging.getLogger(__name__)
        self._openai_key = openai_key

    async def process(self, statistics: dict, context: str = None) -> dict:
        try:
            stats_text = json.dumps(statistics, indent=2)
            prompt = (
                f"Você é um analista de dados experiente.\n"
                f"Abaixo estão os resultados estatísticos de um conjunto de dados:\n{stats_text}\n\n"
                "Gere um insight técnico ou estratégico baseado nesses números.\n"
                "Utilize linguagem simples e objetiva.\n"
                "Destaque pontos de atenção se houver.\n"
            )
            if context:
                prompt += f"Contexto adicional: {context}\n"

            # 🚀 Cria o client localmente na execução
            client = OpenAI(api_key=self._openai_key)

            result = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            insight = result.choices[0].message.content.strip()

            self._logger.info(f"✅ Insight gerado com sucesso")
            return {"status": "success", "insight": insight}

        except Exception as e:
            self._logger.error(f"❌ Erro no InsightsLLMAgent: {str(e)}")
            return {"status": "error", "error": str(e)}
