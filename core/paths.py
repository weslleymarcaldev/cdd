# cdd/core/paths.py caminhos
from pathlib import Path

# Raiz do projeto (pasta "cdd")
ROOT = Path(__file__).resolve().parents[1]

ASSETS = ROOT / "assets"
STORAGE = ROOT / "storage"
PERIODOS_DIR = ROOT / "periodos"
PERIODOS_JSON = PERIODOS_DIR / "periodos_curso.json"
SEEDS = ROOT / "data" / "seeds"

# Garante que pastas essenciais existam
STORAGE.mkdir(exist_ok=True, parents=True)
PERIODOS_DIR.mkdir(exist_ok=True, parents=True)
