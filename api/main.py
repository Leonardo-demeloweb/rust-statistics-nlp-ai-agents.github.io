import os
import tempfile
import logging
import shutil
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from crew_agents.orchestrator.crew_orchestrator import CrewOrchestrator
from fastapi.middleware.cors import CORSMiddleware



# ────────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES
# ────────────────────────────────────────────────────────────────────────────────
load_dotenv()

DB_PATH = "data/analytics.db"
WASM_PATH = "rust_module/target/wasm32-wasi/release/stat_rust_engine.wasm"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    raise EnvironmentError("❌ Variável de ambiente OPENAI_API_KEY não encontrada. Verifique seu arquivo .env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────────────────────────
# FASTAPI + ORCHESTRATOR
# ────────────────────────────────────────────────────────────────────────────────
app = FastAPI(title="Stat Rust Engine API", version="1.0.0")

orchestrator = CrewOrchestrator(DB_PATH, WASM_PATH, OPENAI_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_and_analyze/")
async def upload_and_analyze(file: UploadFile = File(...), question: str = Form(...)):
    """
    Endpoint para upload de arquivo CSV e pergunta de análise.
    """
    try:
        # 📥 Salva arquivo temporário com extensão correta
        tmp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(tmp_dir, f"{file.filename}")

        with open(temp_file_path, "wb") as tmp:
            shutil.copyfileobj(file.file, tmp)

        logger.info(f"📄 Arquivo salvo temporariamente em: {temp_file_path}")

        # 🚀 Executa pipeline
        result = await orchestrator.run_pipeline(temp_file_path, question)

        # 🧹 Remove arquivo temporário
        os.remove(temp_file_path)
        logger.info(f"🧹 Arquivo temporário removido: {temp_file_path}")

        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"❌ Erro na análise: {str(e)}")
        return JSONResponse(content={"status": "error", "error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
