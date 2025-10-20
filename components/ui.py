# cdd/components/ui.py
from __future__ import annotations
import streamlit as st
import pandas as pd
from core.state import ss_get, save_state


def render_legenda_academica(where="main"):
    target = st.sidebar if where == "sidebar" else st
    with target.expander("ℹ️ Legenda — Vida Acadêmica", expanded=False):
        st.markdown(
            """
- **CH** — Carga Horária (horas)
- **T / P / Tot** — Teórica / Prática / Total
- **CR** — Créditos
- **Pré-req.** — Pré-requisito(s)
- **Per.** — Período
- **Disc.** — Disciplina
            """
        )


def metric_card(label: str, value, help: str | None = None):
    c = st.container(border=True)
    with c:
        st.markdown(f"**{label}**")
        st.markdown(
            f"<div style='font-size:1.8rem'>{value}</div>", unsafe_allow_html=True
        )
        if help:
            st.caption(help)


def progress_card(title: str, current: int, total: int):
    total = max(1, int(total))
    pct = int(100 * int(current) / total)
    c = st.container(border=True)
    with c:
        st.subheader(f"{title} — {current}/{total} ({pct}%)")
        st.progress(pct / 100)


def table(df: pd.DataFrame):
    st.dataframe(df, use_container_width=True)


def tag(text: str):
    st.markdown(
        f"<span style='background:#39414a;color:#e6eaee;padding:.15rem .45rem;"
        f"border-radius:.4rem;font-size:.8rem'>{text}</span>",
        unsafe_allow_html=True,
    )


def render_legenda_academica(where: str = "main"):
    target = st.sidebar if where == "sidebar" else st
    with target.expander("ℹ️ Legenda — Vida Acadêmica", expanded=False):
        st.markdown(
            """
- **CH** — Carga Horária (horas)  
- **T / P / Tot** — Teórica / Prática / Total  
- **CR** — Créditos  
- **Pré-req.** — Pré-requisito(s)  
- **OB** — Obrigatória • **OPT** — Optativa
            """
        )


def tile(title: str, body: str, tags: list[str] | None = None):
    st.markdown(f"**{title}**")
    st.write(body)
    if tags:
        st.caption(" ".join(f"`{t}`" for t in tags))
    st.divider()
