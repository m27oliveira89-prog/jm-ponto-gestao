import streamlit as st
import pandas as pd
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>PAINEL DO GESTOR</h1>", unsafe_allow_html=True)
st.markdown("---")
st.subheader("Histórico de Batidas (Tempo Real)")
try:
        dados = db.reference('batidas').get()
        if dados:
            registros = []
            for mat, datas in dados.items():
                for dia, batidas in datas.items():
                    for id_b, info in batidas.items():
                        registros.append({
                            "Matrícula": mat,
                            "Data": dia,
                            "Hora": info['hora'],
                            "Status": info['status']
                        })
            
            df = pd.DataFrame(registros)
            
            # --- NOVO: Botão de Download ---
            col_data, col_btn = st.columns([3, 1])
            with col_btn:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 BAIXAR RELATÓRIO (CSV)",
                    data=csv,
                    file_name=f'relatorio_ponto_{datetime.datetime.now().strftime("%d_%m_%Y")}.csv',
                    mime='text/csv',
                )
            
            # Exibe a tabela
            st.dataframe(df, use_container_width=True)
            
            # Métricas
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Total de Registros", len(df))
            c2.metric("Funcionários Ativos", len(df['Matrícula'].unique()))
            
        else:
            st.info("Aguardando os primeiros registros...")
except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
