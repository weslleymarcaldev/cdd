# cdd/views/data_lab.py
import streamlit as st


def page():
    st.title("Data Lab")
    st.write("Conteúdo inicial da página **Data Lab**. Edite em `views/data_lab.py`.")
    st.header("Data Lab — EDA rápido com CSV")
    up = st.file_uploader("Carregue um CSV", type=["csv"])

    if up is None:
        st.info("Carregue um CSV para começar.")
        return

    # 1) tenta leitura padrão
    try:
        df = pd.read_csv(up)
    except Exception:
        # 2) fallback: separador ';' + utf-8-sig
        try:
            up.seek(0)
            df = pd.read_csv(up, sep=";", encoding="utf-8-sig")
        except Exception as e:
            st.error(
                f"Não consegui ler o CSV (tente ajustar separador/encoding). Detalhe: {e}"
            )
            return

    # --- Daqui pra baixo SEMPRE roda se df foi carregado ---
    st.success(f"Linhas: {len(df):,} | Colunas: {df.shape[1]}")
    tabs = st.tabs(
        ["Amostra", "Info", "Describe", "Gráficos rápidos", "Query (pandas)"]
    )
