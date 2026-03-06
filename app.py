import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# 1. Configuração de Conexão (O que estava faltando)
if not firebase_admin._apps:
    try:
        cred_dict = st.secrets["firebase"]
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'SUA_URL_AQUI'
        })
    except Exception as e:
        st.error(f"Erro na configuração do Firebase: {e}")

# 2. Título do Painel
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>PAINEL DO GESTOR</h1>", unsafe_allow_html=True)
st.divider()

# 3. Busca de Dados e Exibição
st.subheader("Histórico de Batidas (Tempo Real)")

try:
    # Busca os dados no nó 'batidas'
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
        
        # Botão de Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 BAIXAR RELATÓRIO (CSV)",
            data=csv,
            file_name="relatorio_ponto.csv",
            mime="text/csv",
        )

        # Exibe a tabela
        st.dataframe(df, use_container_width=True)

        # Métricas rápidas
        c1, c2 = st.columns(2)
        c1.metric("Total de Registros", len(df))
        c2.metric("Funcionários Ativos", len(df["Matrícula"].unique()))
    else:
        st.info("Aguardando os primeiros registros no banco de dados...")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
