# app.py — Hub de Estudos em Ciência de Dados (organizado)
# Autor: Weslley Marçal
# Objetivo: centralizar estudo (conteúdo, links, checklist, to-do, anotações, testes, Data Lab e ML Demo)

from importlib import import_module
import streamlit as st
from core.state import load_state, save_state

st.set_page_config(
    page_title="CDD — Hub", layout="wide", initial_sidebar_state="expanded"
)

# Boot do estado
if "boot" not in st.session_state:
    load_state()
    st.session_state["boot"] = True

# Mapa: título -> módulo
PAGES = {
    "Resumo (Visão geral)": "views.resumo",
    "Fundamentos (Conceitos e teoria)": "views.fundamentos",
    "Ferramentas (Ambientes e bibliotecas)": "views.ferramentas",
    "Grade de Estudos": "views.grade",
    "Períodos do Curso": "views.periodos",
    "Data Lab": "views.data_lab",
    "ML Demo": "views.ml_demo",
    "Checklist": "views.checklist",
    "To-do": "views.todo",
    "Anotações": "views.notes",
    "PDF Tools": "views.pdf_tools",
}

# Categorias (garanta que o arquivo esteja em UTF-8)
CATEGORIES = {
    "🎓 Vida Acadêmica": ["Períodos do Curso", "Grade de Estudos"],
    "🧪 Prática & Portfólio": ["Data Lab", "ML Demo"],
    "📚 Conteúdo & Referência": [
        "Resumo (Visão geral)",
        "Fundamentos (Conceitos e teoria)",
        "Ferramentas (Ambientes e bibliotecas)",
    ],
    "🧭 Organização pessoal": ["Checklist", "To-do", "Anotações", "PDF Tools"],
}

# Saneia categorias (só itens existentes)
for k in list(CATEGORIES):
    CATEGORIES[k] = [p for p in CATEGORIES[k] if p in PAGES]

# -------- Navegação (sidebar) --------
st.sidebar.title("Navegação")

q = (
    st.sidebar.text_input("Buscar páginas", placeholder="ex.: SQL, projeto…")
    .strip()
    .lower()
)
if q:
    options = [p for p in PAGES if q in p.lower()] or list(PAGES.keys())
    choice = st.sidebar.radio("Seções (busca)", options, index=0, key="nav_search")
else:
    cats = [c for c in CATEGORIES if CATEGORIES[c]]
    cat = st.sidebar.selectbox("Categoria", cats, index=0)
    st.sidebar.markdown("---")
    choice = st.sidebar.radio("Seções", CATEGORIES[cat], index=0, key="nav_grouped")

# -------- Roteamento --------
module_name = PAGES[choice]
try:
    mod = import_module(module_name)
    # cada módulo deve expor uma função page()
    fn = None
    for cand in ("page", "render", "main"):
        if hasattr(mod, cand):
            fn = getattr(mod, cand)
            break
    if fn:
        fn()
    else:
        st.error(f"O módulo `{module_name}` não expõe `page()`/`render()`/`main()`.")
except Exception as e:
    # Mostra erro amigável na UI, sem derrubar a app
    st.error(f"Falha ao carregar `{module_name}`: {e}")

# -------- Estado / Persistência --------
with st.sidebar.expander("Estado / Persistência"):
    if st.button("Salvar estado"):
        # se quiser, troque pela lista de chaves que você realmente usa
        save_state(list(st.session_state.keys()))
        st.toast("Estado salvo.", icon="✅")
