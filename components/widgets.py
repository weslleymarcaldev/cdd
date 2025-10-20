# cdd/components/widgets.py
from __future__ import annotations
import streamlit as st
from typing import Iterable, Tuple, List, Dict, Any


def section(title: str, help: str | None = None):
    st.markdown(f"### {title}")
    if help:
        st.caption(help)


def input_3nums(
    label_a: str,
    label_b: str,
    label_c: str,
    a: int = 0,
    b: int = 0,
    c: int = 0,
    step: int = 1,
    key: str = "",
) -> Tuple[int, int, int]:
    c1, c2, c3 = st.columns(3)
    with c1:
        va = st.number_input(label_a, 0, 10000, a, step=step, key=f"{key}_a")
    with c2:
        vb = st.number_input(label_b, 0, 10000, b, step=step, key=f"{key}_b")
    with c3:
        vc = st.number_input(label_c, 0, 10000, c, step=step, key=f"{key}_c")
    return int(va), int(vb), int(vc)


def pill(text: str):
    st.markdown(
        f"<span style='display:inline-block;padding:.2rem .5rem;border-radius:999px;"
        f"background:#2b2f33;color:#dfe3e6;font-size:.85rem'>{text}</span>",
        unsafe_allow_html=True,
    )


def link_list(items: Iterable[Dict[str, str]]):
    """items: [{'titulo': 'Aula 1', 'url': 'https://...'}, ...]"""
    for it in items or []:
        t = it.get("titulo") or it.get("url", "")
        u = it.get("url", "")
        st.write(f"- [{t}]({u})")
