# cdd/views/fundamentos.py
import streamlit as st


def page():
    st.title("Fundamentos (Conceitos e teoria)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Estatística & Probabilidade")
        st.markdown(
            "- Média/mediana/variância\n- Distribuições\n- Testes de hipótese & p-valor\n"
            "- Intervalos de confiança\n- Regressão linear/logística"
        )
    with col2:
        st.subheader("Álgebra & Cálculo")
        st.markdown(
            "- Vetores/matrizes, PCA\n- Derivada, gradiente descendente\n- Função de custo"
        )
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Engenharia de Dados")
        st.markdown(
            "- ETL/ELT, *data wrangling*, *pipelines*\n- SQL avançado, APIs/scraping"
        )
    with col4:
        st.subheader("ML, MLOps & Comunicação")
        st.markdown(
            "- Superv./Não-superv., métricas\n- Deploy (API), monitoramento, reprodutibilidade\n- Ética/LGPD"
        )
