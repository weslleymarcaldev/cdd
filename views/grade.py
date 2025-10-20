# views/grade.py
from core.io import read_json
import json
from core.common import st, pd, np, dt
from core.adapters import periodos_to_grade
from pathlib import Path
from core.state import (
    render_legenda_academica,
    ensure_check_state,
    ss_get,
    ss_set,
    ss_pop,
    save_state,
)


PERIODOS_JSON = Path("periodos/periodos_curso.json")


def load_grade_from_periodos():
    obj = read_json(PERIODOS_JSON) or {}
    periodos = obj.get("periodos", {})
    return periodos_to_grade(periodos)


def page():
    st.title("Grade de Estudos — Ciência de Dados (Wes)")
    render_legenda_academica(where="main")
    st.caption(
        "Trilha prática em 8 módulos com entregáveis, métricas e links. Foque em aplicar e publicar."
    )

    # --------- Definição da grade (pode editar livremente) ---------
    GRADE = [
        {
            "mod": 1,
            "nome": "Fundamentos de Python para Dados",
            "carga": "2–3 sem",
            "objetivos": [
                "Dominar pandas/NumPy para EDA",
                "Leitura de CSV/Excel/SQL; limpeza e junção",
            ],
            "topicos": [
                "pandas (index, loc/iloc, groupby, merge, pivot)",
                "NumPy (arrays, broadcasting)",
                "Datas/strings, tipos, valores ausentes",
                "Boas práticas de notebook e README",
            ],
            "entregaveis": [
                "Mini-EDA público (repo) com 3–5 gráficos e achados",
                "Arquivo `requirements.txt` e README de passo a passo",
            ],
            "links": {
                "pandas": "https://pandas.pydata.org/docs/",
                "NumPy": "https://numpy.org/doc/",
                "Matplotlib": "https://matplotlib.org/stable/",
            },
            "tags": ["python", "pandas", "numpy", "eda"],
        },
        {
            "mod": 2,
            "nome": "SQL Analítico",
            "carga": "2 sem",
            "objetivos": [
                "Escrever consultas com CTE e janelas",
                "Responder perguntas de negócio com SQL",
            ],
            "topicos": [
                "JOIN • GROUP BY/HAVING • CTE",
                "Window functions (ROW_NUMBER, LAG, SUM OVER)",
                "Coortes, funil, LTV simple",
                "Índices e performance básica",
            ],
            "entregaveis": [
                "Caderno SQL com 8–10 queries respondendo perguntas",
                "README com diagrama e explicações",
            ],
            "links": {
                "Mode SQL": "https://mode.com/sql-tutorial/",
                "PostgreSQL": "https://www.postgresql.org/docs/",
            },
            "tags": ["sql", "analytics", "janelas"],
        },
        {
            "mod": 3,
            "nome": "Estatística Aplicada",
            "carga": "2 sem",
            "objetivos": [
                "Entender variabilidade e inferência",
                "Saber escolher e reportar métricas",
            ],
            "topicos": [
                "Distribuições, amostragem, IC",
                "Testes A/B, p-valor, poder",
                "Regressão linear/logística (conceitos)",
                "Métricas: RMSE/MAE • AUC/F1/Recall",
            ],
            "entregaveis": [
                "Notebook A/B com simulação e interpretação",
                "Resumo 1-página com recomendações",
            ],
            "links": {
                "StatQuest": "https://www.youtube.com/@statquest",
            },
            "tags": ["estatistica", "abtest", "metricas"],
        },
        {
            "mod": 4,
            "nome": "ML Clássico com scikit-learn",
            "carga": "3 sem",
            "objetivos": [
                "Criar pipeline de pré-processamento + modelo",
                "Validar corretamente e evitar leakage",
            ],
            "topicos": [
                "train_test_split, CV, Grid/RandomSearch",
                "OneHotEncoder, StandardScaler, ColumnTransformer",
                "Desbalanceamento (class_weight/SMOTE)",
                "Feature importance e erros comuns",
            ],
            "entregaveis": [
                "Projeto Churn (AUC/F1) com pipeline sklearn",
                "README com decisões, métricas e limitações",
            ],
            "links": {
                "sklearn": "https://scikit-learn.org/stable/",
                "Imbalanced-learn": "https://imbalanced-learn.org/stable/",
            },
            "tags": ["sklearn", "ml", "pipeline"],
        },
        {
            "mod": 5,
            "nome": "Deploy Simples (API + App)",
            "carga": "2 sem",
            "objetivos": [
                "Servir modelo via API (FastAPI) e UI (Streamlit)",
                "Empacotar com Docker e documentar",
            ],
            "topicos": [
                "FastAPI (POST /predict) e pydantic",
                "Streamlit como cliente do modelo",
                "Dockerfile & reprodutibilidade",
                "Estratégia de versionamento (Git/GitHub)",
            ],
            "entregaveis": [
                "API do churn + app Streamlit cliente",
                "Dockerfile e instruções de execução",
            ],
            "links": {
                "FastAPI": "https://fastapi.tiangolo.com/",
                "Streamlit": "https://docs.streamlit.io/",
                "Docker": "https://docs.docker.com/",
            },
            "tags": ["deploy", "api", "docker", "streamlit"],
        },
        {
            "mod": 6,
            "nome": "Séries Temporais ou Forecast com Regressão",
            "carga": "2–3 sem",
            "objetivos": [
                "Comparar baseline vs modelo",
                "Construir dashboard de previsão",
            ],
            "topicos": [
                "Baselines (naive/seasonal naive)",
                "Prophet OU regressão com features (feriados, promo)",
                "MAE/RMSE e intervalo de confiança",
            ],
            "entregaveis": [
                "Dashboard Streamlit de forecast com upload CSV",
                "README com comparação com baseline",
            ],
            "links": {
                "Prophet": "https://facebook.github.io/prophet/docs/quick_start.html",
                "Pandas Time": "https://pandas.pydata.org/docs/user_guide/timeseries.html",
            },
            "tags": ["series", "forecast", "prophet"],
        },
        {
            "mod": 7,
            "nome": "NLP OU Visão (ramo opcional)",
            "carga": "2 sem",
            "objetivos": [
                "Dominar um caso de texto OU imagem de ponta a ponta",
            ],
            "topicos": [
                "NLP: classificação de reviews (transformers básicos)",
                "CV: classificação simples (torchvision/sklearn)",
                "Curadoria de dados e avaliação",
            ],
            "entregaveis": [
                "Projeto opcional com demo (Streamlit) e métricas claras",
            ],
            "links": {
                "Hugging Face": "https://huggingface.co/docs",
                "Torchvision": "https://pytorch.org/vision/stable/index.html",
            },
            "tags": ["nlp", "visao", "transformers", "cv"],
        },
        {
            "mod": 8,
            "nome": "Pipelines & Rastreamento (leve)",
            "carga": "2 sem",
            "objetivos": [
                "Automatizar ETL/treino simples e rastrear execuções",
            ],
            "topicos": [
                "Orquestração simples (GitHub Actions ou cron + script)",
                "MLflow para runs/params/metrics (local)",
                "Monitoramento: drift/métricas básicas",
            ],
            "entregaveis": [
                "ETL/treino agendado + tracking de métricas",
                "Post curto com lições aprendidas",
            ],
            "links": {
                "MLflow": "https://mlflow.org/",
                "GH Actions": "https://docs.github.com/actions",
            },
            "tags": ["mlops", "pipelines", "mlflow", "ci"],
        },
    ]

    # --------- Estado e filtros ----------
    if "grade_status" not in st.session_state:
        st.session_state.grade_status = {m["mod"]: False for m in GRADE}
    if "grade_notes" not in st.session_state:
        st.session_state.grade_notes = {m["mod"]: "" for m in GRADE}

    colf1, colf2 = st.columns([2, 1])
    with colf1:
        q = (
            st.text_input(
                "Filtrar por termo ou tag", placeholder="ex.: sql, deploy, sklearn…"
            )
            .strip()
            .lower()
        )
    with colf2:
        if st.button("Zerar progresso"):
            st.session_state.grade_status = {m["mod"]: False for m in GRADE}
            st.session_state.grade_notes = {m["mod"]: "" for m in GRADE}

    # aplica filtro
    vis = []
    for m in GRADE:
        blob = " ".join(
            [
                m["nome"],
                " ".join(m["tags"]),
                " ".join(m["topicos"]),
                " ".join(m["objetivos"]),
            ]
        ).lower()
        if q and q not in blob:
            continue
        vis.append(m)

    # --------- Progresso geral ----------
    if q:  # com filtro
        done = sum(1 for m in vis if st.session_state.grade_status.get(m["mod"], False))
        total = max(1, len(vis))
    else:  # sem filtro
        done = sum(
            1 for m in GRADE if st.session_state.grade_status.get(m["mod"], False)
        )
        total = max(1, len(GRADE))

    pct = int(100 * done / total)
    st.progress(pct / 100, text=f"{done}/{total} módulos concluídos ({pct}%)")

    # --------- Renderização ----------
    for m in vis:
        with st.container(border=True):
            top = st.columns([8, 2, 2])
            with top[0]:
                st.subheader(f"M{m['mod']}. {m['nome']}")
                st.caption(
                    f"Carga sugerida: {m['carga']} • Tags: {' | '.join(m['tags'])}"
                )
            with top[1]:
                st.toggle(
                    "Concluído",
                    key=f"g_done_{m['mod']}",
                    value=st.session_state.grade_status[m["mod"]],
                    on_change=lambda mm=m["mod"]: st.session_state.grade_status.update(
                        {mm: not st.session_state.grade_status[mm]}
                    ),
                )
            with top[2]:
                if st.button("Salvar módulo", key=f"save_{m['mod']}"):
                    save_state(["grade_status", "grade_notes"])
                    st.toast("Módulo salvo.", icon="✅")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Objetivos**")
                st.markdown("\n".join([f"- {x}" for x in m["objetivos"]]))
                st.markdown("**Tópicos**")
                st.markdown("\n".join([f"- {x}" for x in m["topicos"]]))
            with c2:
                st.markdown("**Entregáveis**")
                st.markdown("\n".join([f"- {x}" for x in m["entregaveis"]]))
                st.markdown("**Links úteis**")
                st.markdown("\n".join([f"- [{k}]({v})" for k, v in m["links"].items()]))

            st.text_area(
                "Anotações deste módulo",
                key=f"g_note_{m['mod']}",
                value=st.session_state.grade_notes[m["mod"]],
                placeholder="Resumos, dúvidas, melhorias…",
                height=120,
            )

            # ✅ sincroniza notas — precisa ficar DENTRO do for
            st.session_state.grade_notes[m["mod"]] = ss_get(f"g_note_{m['mod']}", "")

    st.divider()

    # --------- Exportar plano ---------
    colx1, colx2, colx3 = st.columns(3)
    with colx1:
        if st.button("Salvar progresso (estado)"):
            save_state(["grade_status", "grade_notes"])
            st.toast("Progresso salvo no estado.", icon="💾")

    with colx2:
        export = {
            "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
            "progress": st.session_state.grade_status,
            "notes": st.session_state.grade_notes,
            "grade": GRADE,
        }
        st.download_button(
            "Baixar progresso (.json)",
            data=json.dumps(export, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name="grade_progresso.json",
            mime="application/json",
        )

    with colx3:
        lines = [
            f"# Grade de Estudos — Ciência de Dados (export {dt.date.today().isoformat()})",
            "",
        ]
        for m in GRADE:
            checked = "x" if st.session_state.grade_status.get(m["mod"], False) else " "
            lines += [
                f"## M{m['mod']}. {m['nome']}  [{checked}]",
                f"**Carga**: {m['carga']}  ",
                "**Objetivos:**",
                *[f"- {x}" for x in m["objetivos"]],
                "**Tópicos:**",
                *[f"- {x}" for x in m["topicos"]],
                "**Entregáveis:**",
                *[f"- {x}" for x in m["entregaveis"]],
                "",
            ]
        md = "\n".join(lines)
        st.download_button(
            "Baixar grade (.md)",
            data=md.encode("utf-8"),
            file_name="grade_estudos.md",
            mime="text/markdown",
        )
