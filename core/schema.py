# cdd/core/schema.py esquema
from typing import List, Dict, Optional, TypedDict


class Material(TypedDict, total=False):
    titulo: str
    url: str


class Disciplina(TypedDict, total=False):
    codigo: str
    nome: str
    creditos: int
    teor: int
    prat: int
    total: int
    prereq: str
    done: bool
    link: str  # um link principal
    materiais: List[Material]  # vários links (vídeo, PDF, livro, playlist)
    notas: str  # anotações curtas
