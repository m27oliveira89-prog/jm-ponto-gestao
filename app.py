import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# CONFIGURAÇÃO AUTOMÁTICA (NÃO MEXER AQUI)
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
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://jm-ponto-gestao-default-rtdb.firebaseio.com/'
        })
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")

# VISUAL DO SITE
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>PAINEL DO GESTOR</h1>", unsafe_allow_html=True)
st.divider()
st.subheader("Histórico de Batidas (Tempo Real)")

try:
    ref = db.reference('batidas')
    dados = ref.get()

    if dados:
        registros = []
        for mat, datas in dados.items():
            for dia, batidas in datas.items():
                for id_b, info in batidas.items():
                    registros.append({
                        "Matrícula": mat,
                        "Data": dia,
                        "Hora": info.get('hora', '-'),
                        "Status": info.get('status', '-')
                    })
        df = pd.DataFrame(registros)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 BAIXAR RELATÓRIO", csv, "ponto.csv", "text/csv")
    else:
        st.info("Aguardando registros...")
except:
    st.warning("Conectando ao banco de dados...")
