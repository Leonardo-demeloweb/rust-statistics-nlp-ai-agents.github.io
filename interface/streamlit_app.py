import streamlit as st
import requests

API_URL = "http://localhost:8000/upload_and_analyze/"

# ===== Layout =====

st.set_page_config(page_title="Análise Estatística com AI", layout="wide")

with st.sidebar:
    st.title("📊 Data Analyzer AI")
    st.markdown("**Pipeline:** NLP → SQL → Vetor → Rust → LLM Insights")

st.title("Análise Estatística Automática")
st.markdown("Faça upload de um arquivo tabular e envie sua pergunta em linguagem natural.")

uploaded_file = st.file_uploader("📂 Upload de arquivo", type=["csv", "xlsx", "json"])
question = st.text_input("❓ Pergunta sobre os dados:")

if st.button("Executar Análise"):
    if uploaded_file and question:
        with st.spinner("Processando..."):
            files = {"file": uploaded_file.getvalue()}
            data = {"question": question}
            response = requests.post(API_URL, files={"file": uploaded_file}, data=data)

            if response.status_code == 200:
                result = response.json()
                st.success("✅ Insight Gerado:")
                st.write(result.get("insight"))
                st.markdown("---")
                st.json(result)
            else:
                st.error("❌ Erro durante a análise.")
    else:
        st.warning("Por favor, envie um arquivo e escreva uma pergunta.")
