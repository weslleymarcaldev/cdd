# cdd/views/resumo.py
import streamlit as st
from core.state import ss_get, save_state, render_legenda_academica
from core.paths import PERIODOS_JSON
from core.io import read_json


def page():
    st.title("Guia de Transição para Ciência de Dados — Wes")
    render_legenda_academica(where="main")
    st.markdown("> Foco em **aplicação real**, **deploy** e **comunicação**.")
    st.write(
        "Este hub reúne fundamentos, ferramentas, roadmap, projetos de portfólio, datasets, "
        "checklists, anotações, to-dos, Data Lab e uma demo de ML, tudo em um só lugar."
    )

    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Meta de estudos/semana (h)", ss_get("weekly_goal_h", 6))
            st.slider("Ajustar meta semanal (h)", 2, 20, key="weekly_goal_h")
            done = int(ss_get("study_done_h", 0) or 0)

        with col2:
            st.metric("Horas estudadas (semana)", done)
            st.number_input(
                "Atualizar horas estudadas",
                min_value=0,
                max_value=200,
                key="study_done_h",
            )

        with col3:
            if st.button("Salvar metas no estado"):
                save_state(["weekly_goal_h", "study_done_h"])

    st.divider()
    st.subheader("O que faz um Cientista de Dados (curto e grosso)")
    st.markdown(
        """
        - **Coleta** dados (bancos, APIs, logs), **organiza** (ETL/ELT, limpeza, *feature engineering*),
        - **Analisa/Explora** (estatística, visualização), **modela** (ML clássico / DL, validação e métricas) e
        - **Entrega** valor (dashboards, relatórios, **APIs**, automações, decisões).
        """
    )
    st.info(
        "Sugestão: comece pelo **Roadmap**, use o **To-do** para planejar e o **Data Lab** para praticar."
    )

    st.divider()
    st.subheader("Períodos — visão rápida")

    obj = read_json(PERIODOS_JSON) or {}
    periodos = obj.get("periodos", {})
    notas = obj.get("notas", {})

    # Estatísticas rápidas
    total_disc = 0
    concluidas = 0
    soma_cred = 0
    for disciplinas in periodos.values():
        # disciplinas pode ser [] (ok)
        for d in disciplinas:
            total_disc += 1
            if d.get("done"):
                concluidas += 1
            soma_cred += int(d.get("creditos") or 0)

    c1, c2, c3 = st.columns(3)
    c1.metric("Disciplinas cadastradas", total_disc)
    c2.metric("Concluídas", concluidas)
    c3.metric("Créditos somados", soma_cred)

    # Prévia por período (só código e nome)
    with st.expander("Ver prévia por período"):
        for per in [str(i) for i in range(1, 10)] + ["OPT"]:
            disciplinas = periodos.get(per, [])
            if not disciplinas:
                continue
            st.markdown(
                f"**{per if per!='OPT' else 'Optativas'}** — {len(disciplinas)} disciplinas"
            )
            for d in disciplinas[:6]:  # mostra só as 6 primeiras por período
                cod = d.get("codigo", "?")
                nome = d.get("nome", "?")
                chk = "✅" if d.get("done") else "▫️"
                st.write(f"{chk} {cod} — {nome}")
            if len(disciplinas) > 6:
                st.caption(f"... e mais {len(disciplinas) - 6} neste período.")

    st.info(
        "Edite/consolide tudo na página **Períodos do Curso**; este painel é apenas um resumo."
    )
