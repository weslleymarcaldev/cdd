# cdd/views/ferramentas.py
from core.common import pd, st, np, read_json
from core.state import load_state
from core.io import read_json


def page():
    load_state()
    st.title("Ferramentas (Ambientes e bibliotecas)")
    st.write(
        "Conteúdo inicial da página **Ferramentas (Ambientes e bibliotecas)**. Edite em `views/ferramentas.py`."
    )
    st.header("Ferramentas — do Essencial ao Avançado")
    df = pd.DataFrame(
        [
            (
                "Essencial",
                "Python (pandas, NumPy, scikit-learn), SQL, Jupyter, Git, Matplotlib/Seaborn",
                "EDA, modelos clássicos, versionamento, comunicação",
            ),
            (
                "Intermediário",
                "Plotly/Streamlit, Power BI/Tableau, Docker, FastAPI/Flask",
                "Dashboards, deploy como API, empacotar soluções",
            ),
            (
                "Avançado",
                "PyTorch/TensorFlow, Spark/Dask, Airflow, MLflow, Kubernetes, Cloud, DW/Lake",
                "Deep Learning, big data, orquestração e escala",
            ),
        ],
        columns=["Nível", "Ferramentas", "Uso típico"],
    )
    st.dataframe(df, use_container_width=True)
    st.caption(
        "Prioridade: Python + SQL → Visualização → ML → Deploy (API+Docker) → Pipelines → Big Data/Cloud → MLOps."
    )
