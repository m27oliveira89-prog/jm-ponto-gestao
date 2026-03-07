import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# CONEXÃO REFORÇADA
if not firebase_admin._apps:
    try:
        # Pega a chave dos Secrets e limpa qualquer erro de formatação
        pk = st.secrets["firebase"]["private_key"]
        if "\\n" in pk:
            pk = pk.replace("\\n", "\n")
        
        cred_dict = {
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
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://jm-ponto-gestao-default-rtdb.firebaseio.com/'})
    except Exception as e:
        st.error(f"Erro Crítico: {e}")
