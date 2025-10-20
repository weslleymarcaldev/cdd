import streamlit as st
from core.state import (
    ensure_check_state,
    save_state,
    ss_get,
    ss_set,
    download_json_button,
)

SECOES = {
    "Ambientação": [
        "Instalar Python 3.12+",
        "Criar venv do projeto",
        "Rodar Streamlit",
    ],
    "Rotina": [
        "Estudar 30–60 min/dia",
        "Revisar anotações",
        "Praticar exercícios",
    ],
}


def page():
    st.title("Checklist")

    # Garante chaves no session_state
    for sec, itens in SECOES.items():
        ensure_check_state(sec, itens)

    # UI
    total = 0
    feitos = 0
    for sec, itens in SECOES.items():
        st.subheader(sec)
        for item in itens:
            key = f"checklist::{sec}::{item}"
            # chave centralizada: também espelha no dicionário 'checklist'
            current = ss_get(key, ss_get("checklist", {}).get(sec, {}).get(item, False))
            val = st.checkbox(item, value=current, key=key)
            total += 1
            feitos += int(val)
            # sincroniza nas duas “formas”
            d = ss_get("checklist", {})
            d.setdefault(sec, {})[item] = bool(val)
            ss_set("checklist", d)

    st.progress(0 if total == 0 else feitos / total)
    st.caption(f"Concluídos: {feitos}/{total}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Salvar estado"):
            save_state(list(st.session_state.keys()))
            st.toast("Estado salvo.", icon="✅")
    with col2:
        download_json_button(
            ss_get("checklist", {}), "checklist.json", "⬇️ Exportar checklist"
        )
