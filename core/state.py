# cdd/core/state.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable, Dict, Any
import streamlit as st

# ---------- Persistência ----------
STORAGE = Path("storage")
STORAGE.mkdir(exist_ok=True, parents=True)
STATE_FILE = STORAGE / "cdd_state.json"


# ---------- Session-state helpers ----------
def ss_get(key: str, default: Any = None) -> Any:
    return st.session_state.get(key, default)


def ss_set(key: str, value: Any) -> Any:
    st.session_state[key] = value
    return value


def ss_pop(key: str, default: Any = None) -> Any:
    return st.session_state.pop(key, default)


# ---------- Carregar / Salvar estado ----------
def load_state() -> Dict[str, Any]:
    """Carrega storage/cdd_state.json para st.session_state (se existir)."""
    if not STATE_FILE.exists():
        return st.session_state
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        for k, v in data.items():
            if k not in st.session_state:
                st.session_state[k] = v
    except Exception as e:
        # usa sidebar para não poluir o layout principal
        st.sidebar.warning(f"Não consegui ler {STATE_FILE}: {e}")
    return st.session_state


def save_state(keys: Iterable[str]) -> None:
    """Salva apenas as chaves informadas do st.session_state no JSON."""
    data = {k: st.session_state[k] for k in keys if k in st.session_state}
    STATE_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------- Checklist util ----------
def ensure_check_state(section: str, items: Iterable[str]) -> None:
    """
    Garante chaves booleanas para os itens da checklist.
    Cria também chaves simples (compat): 'check_<section>_<slug_do_item>'
    """
    if "checklist" not in st.session_state:
        st.session_state["checklist"] = {}
    if section not in st.session_state["checklist"]:
        st.session_state["checklist"][section] = {}

    # dicionário por seção
    for raw in items:
        item = str(raw).strip()
        if item and item not in st.session_state["checklist"][section]:
            st.session_state["checklist"][section][item] = False

    # chaves simples compat
    def _slug(s: str) -> str:
        return "".join(ch.lower() if ch.isalnum() else "_" for ch in s).strip("_")

    for raw in items:
        k = f"check_{_slug(section)}_{_slug(str(raw))}"
        if k not in st.session_state:
            st.session_state[k] = False


# ---------- Aliases de compatibilidade ----------
def save_state(keys: Iterable[str]) -> None:
    return save_state(keys)


# ---------- Utilitário de download ----------
def download_json_button(
    data: dict | str,
    filename: str,
    label: str = "⬇️ Baixar JSON",
) -> None:
    """
    Renderiza um botão de download para baixar dados como JSON.
    Aceita tanto dict quanto string já serializada.
    """
    try:
        # Se já for string → converte para bytes; se for dict → faz dumps
        if isinstance(data, (dict, list)):
            payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        elif isinstance(data, str):
            payload = data.encode("utf-8")
        else:
            raise TypeError(f"Tipo inesperado: {type(data)}")

        st.download_button(
            label=label,
            data=payload,
            file_name=filename,
            mime="application/json",
        )
    except Exception as e:
        st.error(f"Não foi possível preparar o download: {e}")


# ---------- Legenda acadêmica (única definição) ----------
def render_legenda_academica(
    *,
    expanded: bool = False,
    where: str | None = None,
    note: str | None = None,
    **_ignored,
) -> None:
    """
    Legenda padrão das siglas acadêmicas.
    - expanded: abre o expander por padrão
    - where: sufixo opcional no título (ex.: "Grade", "Períodos")
    - note: linha adicional ao final
    Parâmetros extras são ignorados (compat com chamadas antigas).
    """
    title = "ℹ️ Legenda (siglas)" + (f" — {where}" if where else "")
    with st.expander(title, expanded=expanded):
        st.markdown(
            """
- **OB**: Obrigatória • **OPT/Optativa**: Optativa  
- **CH**: Carga Horária (Teórica / Prática / Total)  
- **Grupo**: agrupamento da matriz (uso interno / referência)  
- **Pré-requisitos**: códigos das disciplinas exigidas  
            """
        )
        if note:
            st.caption(str(note))


__all__ = [
    "ss_get",
    "ss_set",
    "ss_pop",
    "load_state",
    "save_state",
    "ensure_check_state",
    "download_json_button",
    "render_legenda_academica",
    "save_state",
]
