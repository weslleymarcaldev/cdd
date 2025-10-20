# cdd/views/todo.py
from core.common import st, pd, np  # utilidades “puras”
from core.state import ss_get, ss_set, ss_pop, save_state
from core.io import read_json, write_json  # IO vem daqui
from pathlib import Path
from core.state import download_json_button
from json import load


def page():
    st.write("Conteúdo inicial da página **To-do**. Edite em `views/todo.py`.")
    st.header("To-do (Kanban simples) — estudar e entregar")
    default = {"Backlog": [], "Fazendo": [], "Feito": []}
    todos = ss_get("todos", default)

    # Add novo
    with st.form("add_task"):
        col1, col2 = st.columns([3, 1])
        with col1:
            title = st.text_input(
                "Nova tarefa", placeholder="Ex.: Terminar EDA do churn"
            )
        with col2:
            status = st.selectbox("Status", ["Backlog", "Fazendo", "Feito"])
        desc = st.text_area("Descrição (opcional)", height=80)
        submitted = st.form_submit_button("Adicionar")
        if submitted and title.strip():
            todos[status].append({"title": title.strip(), "desc": desc.strip()})
            ss_set("todos", todos)
            st.rerun()

    st.divider()
    c1, c2, c3 = st.columns(3)
    cols = {"Backlog": c1, "Fazendo": c2, "Feito": c3}

    for lane, col in cols.items():
        with col:
            st.subheader(lane)
            remove_idx = st.empty()
            for i, t in enumerate(todos.get(lane, [])):
                with st.expander(f"{t['title']}", expanded=False):
                    st.write(t.get("desc", ""))
                    mcol1, mcol2, mcol3 = st.columns(3)
                    with mcol1:
                        dest = st.selectbox(
                            "Mover para",
                            ["--", "Backlog", "Fazendo", "Feito"],
                            key=f"mv_{lane}_{i}",
                        )
                    with mcol2:
                        if st.button("Mover", key=f"btnmv_{lane}_{i}") and dest != "--":
                            todos[dest].append(t)
                            del todos[lane][i]
                            ss_set("todos", todos)
                            st.rerun()
                    with mcol3:
                        if st.button("Excluir", key=f"del_{lane}_{i}"):
                            del todos[lane][i]
                            ss_set("todos", todos)
                            st.rerun()

    st.divider()
    left, right = st.columns([1, 1])
    with left:
        download_json_button(todos, "todos.json", "Exportar tarefas (.json)")
        if st.button("Salvar To-do no estado"):
            save_state(["todos"])
    with right:
        uploaded = st.file_uploader("Importar tarefas (.json)", type=["json"])
        if uploaded:
            try:
                todos = json.load(uploaded)
                ss_set("todos", todos)
                st.success("Tarefas importadas.")
                st.rerun()
            except Exception as e:
                st.error(f"JSON inválido: {e}")
