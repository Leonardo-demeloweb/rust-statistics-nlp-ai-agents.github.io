import json
import logging
import subprocess
import uuid


class StatisticsWasmService:
    """
    Serviço responsável por executar cálculo estatístico via módulo WASM (WASI).
    """

    def __init__(self, wasm_path: str):
        self.logger = logging.getLogger(__name__)
        self.wasm_path = wasm_path

    async def process(self, vector: list) -> dict:
        try:
            # Prepara JSON para enviar ao WASM
            input_data = json.dumps({"data": vector})

            # Executa o módulo WASM via subprocess
            result = subprocess.run(
                ["wasmtime", self.wasm_path],
                input=input_data.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if result.returncode != 0:
                raise RuntimeError(f"Erro WASM: {result.stderr.decode('utf-8')}")

            # Decodifica saída
            result_json = result.stdout.decode("utf-8").strip()
            statistics = json.loads(result_json)

            key = str(uuid.uuid4())
            self.logger.info(f"✅ Estatísticas calculadas para chave {key}")

            return {"status": "success", "statistics": statistics}

        except Exception as e:
            self.logger.error(f"❌ Erro no StatisticsWasmService: {str(e)}")
            return {"status": "error", "error": str(e)}
