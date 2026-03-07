import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# 1. CONEXÃO FIREBASE (SÓ UMA VEZ)
if not firebase_admin._apps:
    try:
        cred_dict = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://jm-ponto-gestao-default-rtdb.firebaseio.com/'})
    except Exception as e:
        st.error(f"Erro de conexão: {e}")

# 2. INTERFACE SIMPLIFICADA (SEM LOGIN)
st.set_page_config(page_title="JM Ponto & Gestão", layout="centered")

aba1, aba2 = st.tabs(["📲 BATER PONTO", "📊 PAINEL DO GESTOR"])

with aba1:
    st.header("Registro de Ponto")
    matricula = st.text_input("Digite sua Matrícula")
    if st.button("REGISTRAR AGORA"):
        if matricula:
            from datetime import datetime
            agora = datetime.now()
            data_hoje = agora.strftime("%Y-%m-%d")
            hora_agora = agora.strftime("%H:%M:%S")
            ref = db.reference(f'batidas/{matricula}/{data_hoje}')
            ref.push({'hora': hora_agora, 'status': 'Registrado'})
            st.success(f"Ponto registrado! {hora_agora}")
        else:
            st.warning("Insira a matrícula.")

with aba2:
    st.header("Histórico de Batidas")
    try:
        dados = db.reference('batidas').get()
        if dados:
            regs = []
            for mat, datas in dados.items():
                for dia, batidas in datas.items():
                    for id_b, info in batidas.items():
                        regs.append({"Matrícula": mat, "Data": dia, "Hora": info.get('hora'), "Status": info.get('status')})
            st.table(pd.DataFrame(regs))
        else:
            st.info("Nenhum registro encontrado.")
    except:
        st.write("Carregando painel...")
