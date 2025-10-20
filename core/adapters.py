# core/adapters.py adaptadores
from typing import List, Dict
from core.schema import Disciplina


def periodos_to_grade(periodos: Dict[str, List[Disciplina]]) -> List[dict]:
    """
    Converte { "1":[disciplinas], "2":[...], ..., "OPT":[...] } em uma
    lista de módulos para a página 'Grade de Estudos'.
    """
    grade = []
    # Mantém ordem dos períodos (1..9, OPT no fim)
    ordem = [str(i) for i in range(1, 10)] + ["OPT"]
    mod_idx = 1

    for per in ordem:
        if per not in periodos:
            continue
        for d in periodos[per]:
            nome = f"{d.get('codigo','')} — {d.get('nome','')}".strip(" —")
            objetivos = [
                "Ler ementa e bibliografia",
                "Mapear escola(s) de administração relacionadas",
                "Fazer resumo (PODC, processos, decisões)",
            ]
            topicos = [
                "Escolas: clássica, científica, burocrática, relações humanas, sistêmica/contingencial",
                "Planejamento, Organização, Direção, Controle (PODC)",
                "Estratégia, qualidade, liderança, decisão",
            ]
            entregaveis = [
                "Resumo 1–2 páginas",
                "Mapa mental (escolas/temas)",
                "Lista de 5 questões discursivas",
            ]

            # Concatena materiais (link principal + lista 'materiais')
            links = {}
            if d.get("link"):
                links["Link principal"] = d["link"]
            for m in d.get("materiais", []) or []:
                if m.get("titulo") and m.get("url"):
                    links[m["titulo"]] = m["url"]

            grade.append(
                {
                    "mod": mod_idx,
                    "nome": nome,
                    "carga": f"{d.get('creditos',0)} créditos",
                    "objetivos": objetivos,
                    "topicos": topicos,
                    "entregaveis": entregaveis,
                    "links": links,
                    "tags": ["periodo", per, "cad", d.get("codigo", "").lower()],
                    # ponte: status/nota serão mantidos no session_state como hoje
                }
            )
            mod_idx += 1

    return grade


def build_grade_from_periodos(periodos: dict, buckets: dict[str, str] | None = None):
    """Converte disciplinas com tags em módulos da grade."""
    buckets = buckets or {}
    mods = {}
    for per, discs in (periodos or {}).items():
        for d in discs:
            for t in d.get("tags", []):
                nome_mod = buckets.get(t, f"Tópico: {t}")
                if nome_mod not in mods:
                    mods[nome_mod] = {
                        "mod": len(mods) + 1,
                        "nome": nome_mod,
                        "objetivos": [],
                        "topicos": [],
                        "entregaveis": [],
                        "links": {},
                        "tags": [t],
                    }
                if d.get("codigo") and d.get("link"):
                    mods[nome_mod]["links"][d["codigo"]] = d["link"]
    # volta como lista ordenada
    return [dict(m, mod=i + 1) for i, m in enumerate(mods.values())]
