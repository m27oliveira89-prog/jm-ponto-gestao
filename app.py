import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import time

# Limpa qualquer tentativa anterior travada
st.cache_resource.clear()

if not firebase_admin._apps:
    try:
        pk = st.secrets["firebase"]["private_key"].replace('\\n', '\n')
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": pk,
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        })
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://jm-ponto-gestao-default-rtdb.firebaseio.com/'})
    except Exception as e:
        st.error(f"Erro na Chave: {e}")

st.title("💡 JM Ponto & Gestão")

aba1, aba2 = st.tabs(["📲 REGISTRAR", "📊 VER PAINEL"])

with aba1:
    matricula = st.text_input("Matrícula:", placeholder="Digite aqui...")
    if st.button("REGISTRAR PONTO AGORA"):
        if matricula:
            try:
                agora = time.strftime("%H:%M:%S")
                data = time.strftime("%Y-%m-%d")
                # Salva direto no banco
                db.reference(f'batidas/{matricula}/{data}').push({'hora': agora, 'status': 'OK'})
                st.balloons() # Celebração!
                st.success(f"✅ SUCESSO! Ponto registrado às {agora}")
            except Exception as e:
                st.error("Erro ao salvar. Verifique a conexão.")
        else:
            st.warning("Digite a matrícula primeiro.")

with aba2:
    if st.button("BUSCAR REGISTROS"):
        try:
            dados = db.reference('batidas').get()
            if dados: st.json(dados)
            else: st.info("Banco de dados vazio.")
        except:
            st.error("Erro ao ler banco.")
