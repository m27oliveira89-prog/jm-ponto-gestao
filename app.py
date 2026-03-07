import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="JM Ponto", layout="centered")

# CONEXÃO FIREBASE
if not firebase_admin._apps:
    try:
        pk = st.secrets["firebase"]["private_key"].replace('\\n', '\n')
        cred = credentials.Certificate({
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": pk,
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        })
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://jm-ponto-gestao-default-rtdb.firebaseio.com/'})
    except Exception as e:
        st.error(f"Erro: {e}")

st.title("💡 JM Ponto & Gestão")

# ABAS SIMPLES
aba1, aba2 = st.tabs(["📲 REGISTRAR", "📊 VER PAINEL"])

with aba1:
    matricula = st.text_input("Matrícula:")
    if st.button("BATER PONTO"):
        if matricula:
            try:
                from datetime import datetime
                agora = datetime.now().strftime("%H:%M:%S")
                data = datetime.now().strftime("%Y-%m-%d")
                db.reference(f'batidas/{matricula}/{data}').push({'hora': agora})
                st.success(f"Feito! {agora}")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

with aba2:
    if st.button("ATUALIZAR TABELA"):
        dados = db.reference('batidas').get()
        if dados:
            st.write(dados)
        else:
            st.info("Sem dados.")
