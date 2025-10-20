# CDD — Hub de Estudos (Streamlit)

Centraliza seus estudos de Ciência de Dados: **períodos do curso**, **grade de estudos**, **checklist**, **to-do**, **anotações**, mini **Data Lab**, **ML Demo** e **ferramentas de PDF**.
Arquitetado para ser fácil de manter: `app.py` apenas roteia; utilidades ficam em `core/` e componentes visuais em `components/`.

---

## 🔧 Instalação & Execução

### 1) Criar venv e instalar

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Executar

```bash
python -m streamlit run app.py
```

### 3) Persistência (arquivos locais)

* `storage/cdd_state.json`: metas, checklists e to-do
* `storage/notes.md`: anotações
* `storage/todos.json`: export/import manual de tarefas
* `periodos/periodos_curso.json`: **fonte de verdade** da organização por períodos

> Dica: versionar `periodos/periodos_curso.json` e manter `storage/` no `.gitignore` (dados pessoais).

---

## 🧭 Páginas (views)

* **Resumo (Visão geral)** — visão geral do hub
* **Fundamentos (Conceitos e teoria)** — anotações/links base
* **Ferramentas (Ambientes e bibliotecas)** — setup e referências
* **Grade de Estudos** — trilha prática por módulos, entregáveis e progresso
* **Períodos do Curso** — organização por período/disciplinas, pré-reqs, materiais e notas
* **Data Lab** — espaço para mini-experimentos
* **ML Demo** — demo de ML com `scikit-learn` (imports pesados carregam só nesta página)
* **Checklist** — checagens estruturadas
* **To-do** — tarefas pessoais
* **Anotações** — caderno rápido (`storage/notes.md`)
* **PDF Tools** — utilitários (ex.: PDF → CSV/XLSX; imports pesados locais)

> A navegação é categorizada na sidebar. O **app.py só roteia**, nada de lógica pesada nele.

---

## 🗂️ Estrutura do projeto

```
cdd/
├─ app.py                    # roteador (menu + import dinâmico da view)
├─ core/
│  ├─ state.py               # estado (session/persistência) e helpers
│  ├─ paths.py               # caminhos e criação de pastas
│  ├─ io.py                  # utilitários de I/O (read_json, write_json, to_int, to_str)
│  └─ adapters.py            # conversões (ex.: períodos ⇄ grade)
├─ components/
│  ├─ ui.py                  # componentes visuais reutilizáveis (legendas/cards)
│  └─ widgets.py             # (opcional) inputs customizados
├─ views/
│  ├─ periodos.py            # Períodos do Curso
│  ├─ grade.py               # Grade de Estudos
│  ├─ checklist.py           # Checklist
│  ├─ notes.py               # Anotações
│  ├─ pdf_tools.py           # PDF → CSV/XLSX (imports pesados dentro de page())
│  └─ ...                    # demais páginas
├─ periodos/
│  └─ periodos_curso.json    # fonte de verdade
├─ data/
│  └─ seeds/
│     └─ periodos_seed.json  # exemplo/seed inicial
├─ storage/
│  ├─ cdd_state.json         # estado persistido do usuário
│  └─ notes.md               # anotações
└─ assets/
   └─ styles.css             # (opcional) CSS
```

---

## 🧱 Convenções & Boas Práticas

* **`app.py` é só roteador**: `st.set_page_config`, carrega estado (`load_state`), monta sidebar e faz `import_module(...).page()`.
* **Infra**:

  * `core/state.py`: `ss_get`, `ss_set`, `ss_pop`, `load_state`, `save_state`, `ensure_check_state`.
  * **Sem UI** (nada de `st.markdown()` ou `expander`) dentro de `core/`.
* **Caminhos**: `core/paths.py` define `ROOT`, `ASSETS`, `STORAGE`, `PERIODOS_DIR`, `PERIODOS_JSON`, `SEEDS`.
* **I/O**: `core/io.py` centraliza `read_json()`, `write_json()`, `to_int()`, `to_str()`.
* **Componentes visuais**: `components/ui.py` (ex.: `render_legenda_academica(where="sidebar"|"main")`, `tile(title, body, tags=None)`).
* **Views**: cada arquivo em `views/` implementa **apenas** a lógica daquela página e expõe `page()`.

  * **Imports pesados** (ex.: `sklearn`, `tabula`) **dentro** de `page()` da view correspondente.

---

## 🔁 Sincronização Grade ⇄ Períodos

* **Fonte de verdade acadêmica**: `periodos/periodos_curso.json`.
* Para refletir conteúdos de **Períodos** na **Grade**, use um adapter em `core/adapters.py`:

  * `periodos_to_grade(periodos_dict) -> grade_dict/list`
* Na `views/grade.py`, carregue com:

  ```python
  from core.io import read_json
  from core.paths import PERIODOS_JSON
  from core.adapters import periodos_to_grade

  obj = read_json(PERIODOS_JSON) or {}
  grade = periodos_to_grade(obj.get("periodos", {}))
  ```
* **Onde colocar materiais?**
  Coloque **links/materiais por disciplina** em **Períodos** (mais natural e reusável).
  A **Grade** pode exibir um resumo agregando esses links via adapter.

---

## 🧪 PDF → CSV/XLSX (opcional)

A página `views/pdf_tools.py` traz mini-ferramentas. Para PDF com tabelas:

* Use `tabula-py` (requer Java) **ou** `camelot` (PDFs “digitais”, não escaneados).
* Instale apenas se for usar:

  ```bash
  pip install tabula-py  # (requer Java instalado)
  # ou
  pip install camelot-py[cv]
  ```

---

## 🆘 Troubleshooting

* **`cannot import name X from core.state`**
  Verifique se a função existe e o nome está igual; evite import circular.
* **`RecursionError` em `load_state`**
  Garanta que `load_state()` **não chama** `load_state()` novamente (sem loops).
* **`module 'datetime' has no attribute 'dt'`**
  Use `import datetime as dt` e chame `dt.datetime.now()`.
* **`ValueError: cannot convert float NaN to integer`**
  Use conversores seguros (`to_int`, `to_str`) ao importar CSVs.
* **Imports pesados deixando o app lento**
  Mova `sklearn`, `tabula`, etc. **para dentro da função `page()`** da view que usa.

---

## 🚀 Roadmap curto

* [ ] Adapter **períodos → grade** (e opcionalmente grade → períodos).
* [ ] Melhorar `components/ui.py` com cards/metrics reutilizáveis.
* [ ] Adicionar exportações convenientes (JSON/MD) padronizadas nas páginas.
* [ ] Testes leves de funções em `core/`.

---

## 📌 Comandos úteis (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

---

**Licença**: pessoal/educacional (ajuste conforme seu uso).
**Issues/Sugestões**: abra um issue no repositório.

---
