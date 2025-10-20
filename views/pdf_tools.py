# cdd/views/pdf_tools.py
import streamlit as st
import os
from io import BytesIO
import pandas as pd
from pathlib import Path
from tabula import read_pdf

STORAGE = Path("storage")


def page():

    # PDF → CSV
    st.title("📄 PDF → CSV (beta)")
    st.caption("Extrai tabelas de PDFs usando tabula-py (requer Java).")

    up = st.file_uploader("Envie um PDF com tabelas", type=["pdf"], key="pdf2csv_up")
    flavor = st.radio(
        "Modo de detecção",
        ["lattice", "stream"],
        horizontal=True,
        index=0,
        key="pdf2csv_flavor",
    )

    # Import lazy (só aqui) para não quebrar o app
    if up and st.button("Extrair", key="pdf2csv_extract"):
        try:
            try:
                import tabula  # noqa: F401
            except ModuleNotFoundError:
                st.error(
                    "`tabula-py` não instalado. Rode: `pip install tabula-py` (e tenha Java no PATH)."
                )
                return

            # salva temporário
            tmp_dir = STORAGE if "STORAGE" in globals() else Path(".")
            tmp_pdf = tmp_dir / "tmp_pdf2csv.pdf"
            tmp_pdf.write_bytes(up.getbuffer())

            # tenta com o flavor escolhido
            st.info("Lendo tabelas… isso pode levar alguns segundos.")
            dfs = read_pdf(
                str(tmp_pdf),
                pages="all",
                multiple_tables=True,
                lattice=(flavor == "lattice"),
                stream=(flavor == "stream"),
            )

            # fallback automático se vier vazio
            if not dfs:
                alt = "stream" if flavor == "lattice" else "lattice"
                st.warning(
                    f"Nenhuma tabela detectada com '{flavor}'. Tentando '{alt}'…"
                )
                dfs = read_pdf(
                    str(tmp_pdf),
                    pages="all",
                    multiple_tables=True,
                    lattice=(alt == "lattice"),
                    stream=(alt == "stream"),
                )

            if not dfs:
                st.error("Não encontrei tabelas. Tente outro PDF ou ajuste o modo.")
                return

            st.success(f"Encontrei {len(dfs)} tabela(s).")
            idx = st.number_input("Escolha a tabela para visualizar", 1, len(dfs), 1)
            df_sel = dfs[int(idx) - 1]
            st.dataframe(df_sel.head(50), use_container_width=True)

            # Download único (tudo junto)
            big = pd.concat(dfs, ignore_index=True)
            buf = BytesIO()
            big.to_csv(buf, index=False, encoding="utf-8-sig")
            st.download_button(
                "⬇️ Baixar CSV (todas as tabelas)",
                data=buf.getvalue(),
                file_name="pdf_tabelas.csv",
                mime="text/csv",
            )

            # opção: baixar apenas a tabela atual
            buf_one = BytesIO()
            df_sel.to_csv(buf_one, index=False, encoding="utf-8-sig")
            st.download_button(
                f"⬇️ Baixar apenas a Tabela {idx}",
                data=buf_one.getvalue(),
                file_name=f"tabela_{idx}.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"Falhou ao ler tabelas: {e}")
        finally:
            # limpeza do temporário
            try:
                if "tmp_pdf" in locals() and Path(tmp_pdf).exists():
                    os.remove(tmp_pdf)
            except Exception:
                pass

    # PDF → XLSX
    st.title("PDF → XLSX (beta)")
    # checagens de dependências
    try:
        import tabula  # precisa de Java instalado
    except Exception:
        st.error("Falta o tabula-py. Instale no venv:  `pip install tabula-py`")
        return
    try:
        import openpyxl  # engine padrão para to_excel
    except Exception:
        st.error("Falta o openpyxl. Instale no venv:  `pip install openpyxl`")
        return

    up = st.file_uploader("Envie um PDF com tabelas", type=["pdf"], key="pdf2xlsx_up")
    c1, c2 = st.columns(2)
    with c1:
        flavor = st.radio(
            "Modo de detecção",
            ["lattice", "stream"],
            horizontal=True,
            key="pdf2xlsx_flavor",
        )
    with c2:
        multi_sheets = st.toggle(
            "Uma planilha por tabela", value=True, key="pdf2xlsx_multi_sheets"
        )

    if up and st.button("Extrair para XLSX", key="pdf2xlsx_extract"):
        # salva temporariamente para o tabula ler
        tmp_path = "tmp_pdf_upload.pdf"
        with open(tmp_path, "wb") as f:
            f.write(up.read())

        try:
            dfs = read_pdf(
                tmp_path,
                pages="all",
                multiple_tables=True,
                lattice=(flavor == "lattice"),
                stream=(flavor == "stream"),
            )
        except Exception as e:
            st.error(f"Falhou ao ler tabelas com tabula: {e}")
            return
        finally:
            # limpa arquivo temporário
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        if not dfs:
            st.warning(
                "Não encontrei tabelas. Tente trocar o modo (lattice/stream) ou use OCR antes."
            )
            return

        # preview rápido
        st.success(f"Extraídas {len(dfs)} tabela(s). Abaixo, prévia da primeira:")
        st.dataframe(dfs[0].head(50), use_container_width=True)

        # monta o XLSX em memória
        buf = BytesIO()
        try:
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                if multi_sheets:
                    for i, df in enumerate(dfs, start=1):
                        # normaliza índices/colunas para evitar erros
                        df = df.copy()
                        df.columns = [str(c) for c in df.columns]
                        df.to_excel(writer, index=False, sheet_name=f"Tabela_{i}")
                else:
                    # concatena tudo em uma única planilha
                    big = pd.concat([d.copy() for d in dfs], ignore_index=True)
                    big.columns = [str(c) for c in big.columns]
                    big.to_excel(writer, index=False, sheet_name="Tabelas")

            st.download_button(
                "⬇️ Baixar XLSX",
                data=buf.getvalue(),
                file_name="pdf_tabelas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.error(f"Falhou ao gerar XLSX: {e}")
