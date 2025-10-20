# views/periodos.py
from __future__ import annotations
from pathlib import Path
import json
import streamlit as st
from core.paths import PERIODOS_JSON, PERIODOS_DIR, SEEDS

SEED_FILE = SEEDS / "periodos_seed.json"  # data/seeds/periodos_seed.json


def _empty_structure() -> dict:
    return {"periodos": {str(i): [] for i in range(1, 10)} | {"OPT": []}, "notas": {}}


def _load_seed() -> dict:
    """Tenta carregar o seed; se falhar, volta vazio."""
    try:
        if SEED_FILE.exists():
            return json.loads(SEED_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return _empty_structure()


def _read_periodos() -> dict:
    """
    Carrega periodos/periodos_curso.json.
    Se não existir ou estiver inválido, tenta o seed; por fim, vazio.
    """
    # garante diretório
    PERIODOS_DIR.mkdir(exist_ok=True, parents=True)

    if PERIODOS_JSON.exists():
        try:
            return json.loads(PERIODOS_JSON.read_text(encoding="utf-8"))
        except Exception:
            st.warning(
                "Não consegui ler periodos/periodos_curso.json. Usando seed (se houver)."
            )

    # cai para o seed
    seed = _load_seed()

    # grava seed imediatamente para criar a fonte de verdade
    try:
        PERIODOS_JSON.write_text(
            json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        st.toast("Seed aplicado em periodos/periodos_curso.json", icon="✅")
    except Exception as e:
        st.error(f"Falha ao materializar o seed: {e}")

    return seed


def _write_periodos(obj: dict) -> None:
    PERIODOS_DIR.mkdir(exist_ok=True, parents=True)
    PERIODOS_JSON.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def page():
    st.title("🎓 Períodos do Curso — organização por disciplina")
    with st.expander("ℹ️ Legenda (siglas)"):
        st.markdown(
            "- **OB**: Obrigatória • **OPT/Optativa**: Optativa  \n"
            "- **CH**: Carga Horária (Teórica/Prática/Total)  \n"
            "- **Pré-requisitos**: códigos exigidos  "
        )

    data = _read_periodos()
    periodos: dict = data.get("periodos", {})
    notas: dict = data.get("notas", {})

    # Busca global
    q = st.text_input("Buscar por código, nome ou pré-requisito").strip().lower()
    if q:
        hits = []
        for per, disciplinas in periodos.items():
            for d in disciplinas:
                blob = " ".join(
                    [
                        str(d.get("codigo", "")),
                        str(d.get("nome", "")),
                        str(d.get("prereq", "")),
                        str(d.get("creditos", "")),
                    ]
                ).lower()
                if q in blob:
                    hits.append((per, d))
        with st.expander(f"Resultados ({len(hits)})", expanded=True):
            for per, d in hits:
                st.markdown(
                    f"**{d.get('codigo','?')} — {d.get('nome','?')}**  \n"
                    f"Período: **{per}** • Créditos: {d.get('creditos','?')} • "
                    f"CH T/P/T: {d.get('teor',0)}/{d.get('prat',0)}/{d.get('total',0)} • "
                    f"Pré-req.: {d.get('prereq','—') or '—'}"
                )
        st.divider()

    # Inclusão rápida
    with st.form("add_disc"):
        colA, colB = st.columns([1, 3])
        with colA:
            per = st.selectbox(
                "Período", [str(i) for i in range(1, 10)] + ["OPT"], index=0
            )
            cod = st.text_input("Código", placeholder="ex.: DCC205").strip()
            cred = st.number_input("Créditos", 0, 20, 4)
        with colB:
            nome = st.text_input(
                "Nome da disciplina", placeholder="Nome completo"
            ).strip()
            c1, c2, c3 = st.columns(3)
            with c1:
                teo = st.number_input("CH Teórica", 0, 300, 60, step=15)
            with c2:
                pra = st.number_input("CH Prática", 0, 300, 0, step=15)
            with c3:
                tot = st.number_input("CH Total", 0, 300, max(teo + pra, 60), step=15)
            prereq = st.text_input(
                "Pré-requisitos", placeholder="Ex.: DCC204, EST231"
            ).strip()
        if st.form_submit_button("Adicionar disciplina") and cod and nome:
            novo = {
                "codigo": cod,
                "nome": nome,
                "creditos": int(cred),
                "teor": int(teo),
                "prat": int(pra),
                "total": int(tot),
                "prereq": prereq,
                "done": False,
                "link": "",
                "materiais": [],
                "notas": "",
            }
            periodos.setdefault(per, []).append(novo)
            data["periodos"] = periodos
            _write_periodos(data)
            st.success(f"Disciplina {cod} adicionada ao período {per}.")
            st.experimental_rerun()

    # Renderização por período
    ordem = [str(i) for i in range(1, 10)] + ["OPT"]
    for per in ordem:
        disciplinas = periodos.get(per, [])
        done = sum(1 for d in disciplinas if d.get("done"))
        total = max(1, len(disciplinas))
        pct = int(100 * done / total) if total else 0

        with st.container(border=True):
            titulo = (
                f"{per}º Período" if per != "OPT" else "Optativas (catálogo pessoal)"
            )
            st.subheader(f"{titulo} — {done}/{len(disciplinas)} concluídas ({pct}%)")
            st.progress(pct / 100)

            if not disciplinas:
                st.caption("Nenhuma disciplina cadastrada neste período ainda.")
                continue

            for i, d in enumerate(list(disciplinas)):
                key_base = f"{per}-{i}"
                with st.expander(
                    f"{d.get('codigo','?')} — {d.get('nome','?')}", expanded=False
                ):
                    col1, col2, col3 = st.columns([3, 2, 2])
                    with col1:
                        st.write(f"**Créditos:** {d.get('creditos','?')}")
                        st.write(
                            f"**CH T/P/T:** {d.get('teor',0)}/{d.get('prat',0)}/{d.get('total',0)}"
                        )
                        st.write(f"**Pré-requisitos:** {d.get('prereq','—') or '—'}")
                    with col2:
                        d["done"] = st.toggle(
                            "Concluída?",
                            value=d.get("done", False),
                            key=f"done_{key_base}",
                        )
                        d["link"] = st.text_input(
                            "Link principal",
                            value=d.get("link", ""),
                            key=f"link_{key_base}",
                        )
                    with col3:
                        if st.button(
                            "Excluir", key=f"del_{key_base}", type="secondary"
                        ):
                            disciplinas.pop(i)
                            periodos[per] = disciplinas
                            data["periodos"] = periodos
                            _write_periodos(data)
                            st.experimental_rerun()

                    # Materiais extras
                    st.markdown("**Materiais**")
                    for j, m in enumerate(d.get("materiais", []) or []):
                        st.write(f"- [{m.get('titulo','link')}]({m.get('url','')})")

                    with st.form(f"add_mat_{key_base}"):
                        mt_t = st.text_input("Título do material")
                        mt_u = st.text_input("URL")
                        if (
                            st.form_submit_button("Adicionar material")
                            and mt_t
                            and mt_u
                        ):
                            d.setdefault("materiais", []).append(
                                {"titulo": mt_t.strip(), "url": mt_u.strip()}
                            )
                            disciplinas[i] = d
                            periodos[per] = disciplinas
                            data["periodos"] = periodos
                            _write_periodos(data)
                            st.experimental_rerun()

                    # Notas pessoais (por disciplina)
                    note_key = f"{per}-{d.get('codigo','')}"
                    notas[note_key] = st.text_area(
                        "Anotações / Conteúdo estudado",
                        value=notas.get(note_key, d.get("notas", "")),
                        key=f"note_{key_base}",
                        height=120,
                        placeholder="Resumo, tópicos vistos, dúvidas…",
                    )
                    d["notas"] = notas[note_key]
                    disciplinas[i] = d
                    periodos[per] = disciplinas

        st.divider()

    # Persistência
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Salvar"):
            data["periodos"] = periodos
            data["notas"] = notas
            _write_periodos(data)
            st.toast("Salvo em periodos/periodos_curso.json", icon="✅")
    with col2:
        st.download_button(
            "⬇️ Exportar JSON",
            data=json.dumps(
                {"periodos": periodos, "notas": notas}, ensure_ascii=False, indent=2
            ).encode("utf-8"),
            file_name="periodos_curso.json",
            mime="application/json",
        )
    with col3:
        up = st.file_uploader("⬆️ Importar JSON", type=["json"], key="imp_json_periodos")
        if up:
            try:
                obj = json.load(up)
                _write_periodos(obj)
                st.success("Importado com sucesso.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"JSON inválido: {e}")
