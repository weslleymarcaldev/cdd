# cdd/views/notes.py
import streamlit as st
from pathlib import Path

NOTES_FILE = Path("notes.md")
from core.state import ss_get, save_state


def page():
    st.title("Anotações")
    st.write("Conteúdo inicial da página **Anotações**. Edite em `views/notes.py`.")
    st.header("Anotações (Markdown)")
    if "notes_md" not in st.session_state:
        if NOTES_FILE.exists():
            st.session_state["notes_md"] = NOTES_FILE.read_text(encoding="utf-8")
        else:
            st.session_state["notes_md"] = (
                "# Notas de estudo\n\n- Use este espaço para rascunhos, fórmulas, links…"
            )

    st.caption("Dica: use cabeçalhos (##), listas, código (```python).")
    st.session_state["notes_md"] = st.text_area(
        "Editor", value=st.session_state["notes_md"], height=400
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Salvar notes.md no disco"):
            NOTES_FILE.write_text(st.session_state["notes_md"], encoding="utf-8")
            st.toast("Notas salvas em notes.md", icon="📝")
    with col2:
        st.download_button(
            "Baixar notes.md",
            data=st.session_state["notes_md"].encode("utf-8"),
            file_name="notes.md",
            mime="text/markdown",
        )
    with col3:
        st.toggle("Pré-visualizar abaixo", key="show_preview", value=True)

    if ss_get("show_preview", True):
        st.markdown("---")
        st.subheader("Preview")
        st.markdown(st.session_state["notes_md"])
