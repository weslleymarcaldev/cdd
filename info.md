# Estrutura do Projeto CDD (Streamlit) — Guia Rápido

Este documento explica o que é cada pasta/arquivo, o que pode editar/apagar e como rodar o app.

1) 🧩 Principais Arquivos (essenciais)

- app.py
App Streamlit (ponto de entrada). Contém páginas, navegação e lógica.
Rodar: python -m streamlit run app.py

- requirements.txt
Dependências Python (streamlit, pandas, numpy, scikit-learn).
Edite quando adicionar/remover libs.
Instalação: pip install -r requirements.txt

- styles.css (opcional, recomendado)
CSS para melhorar o visual do Streamlit.
Edite à vontade. Se remover, o app funciona sem o estilo extra.

- README.txt
Instruções de instalação/execução. Edite se o fluxo mudar.

- info.md
Notas, links e referências do projeto. Edite livremente.

- cdd_state.json (gerado pelo app)
Persistência de estado: metas, checklist, to-dos.
Não precisa editar manualmente. Se apagar, apenas perde o progresso salvo; o app recria.

- .gitignore
Regras do Git para ignorar arquivos (ex.: .venv, caches, estado). Mantenha.

- .env (opcional)
Variáveis de ambiente (tokens, URLs). O app atual não depende dele. Pode apagar se não usar.

2) 🐍 Ambiente Virtual Python

.venv/
Ambiente isolado (Python + pacotes).

Lib/site-packages/: bibliotecas instaladas

Scripts/: python.exe, pip.exe, activate.bat etc.

pyvenv.cfg: metadados

Dicas

Não versionar .venv no Git.

Pode apagar para “resetar” o ambiente (recrie com python -m venv .venv).

2) 🟨 Artefatos do BOLT/Node (não necessários p/ Streamlit)

index.js, package.json, package-lock.json

project-bolt-*.zip

Pode apagar com segurança se não houver nada Node/JS no projeto.

3) ✅ O que posso remover sem quebrar o app

index.js, package.json, package-lock.json, project-bolt-*.zip

.env (se não usa)

cdd_state.json (app recria; você só perde o estado salvo)

.venv/ (se quiser recriar o ambiente do zero)

4) 🔒 O que é essencial manter

app.py

requirements.txt

styles.css (opcional, mas útil)

README.txt e/ou info.md (documentação)

.gitignore (se usar Git)

5) ▶️ Como rodar (passo a passo)
# dentro da pasta cdd/
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python -m streamlit run app.py

6) ✍️ O que normalmente você vai editar

app.py: páginas novas (checklist, to-do, EDA, ML demo), widgets, navegação.

requirements.txt: adicionar libs quando necessário.

styles.css: ajustes de UI/UX.

README.txt / info.md: documentação e links.

7) 🧹 Checklist de “faxina segura”

 Apagar artefatos do BOLT/Node: index.js, package*.json, project-bolt-*.zip

 Apagar .env (se não usa)

 Opcional: apagar cdd_state.json (recria; perde estado salvo)

 Opcional: apagar .venv/ e recriar (python -m venv .venv + pip install -r requirements.txt)

8) 🆘 Notas rápidas

Se algo “sumir” do app (ex.: tarefas, checklist), verifique o cdd_state.json.

Problemas ao rodar? Recrie o .venv e reinstale o requirements.txt.

styles.css é só cosmético: pode ajustar sem medo.


# dentro de /c/workspace/DataScience/cdd
python -3.12 -m venv .venv       # só se ainda não existir
source .venv/Scripts/activate    # ativa no Git Bash
python -m pip install -r requirements.txt
python -c "import sys, streamlit as s; print(sys.executable); print(s.__version__, hasattr(s,'session_state'))"
python -m streamlit run app.py


./.venv/Scripts/python.exe -c "import bcrypt, getpass; print(bcrypt.hashpw(getpass.getpass('Senha: ').encode(), bcrypt.gensalt()).decode())"

Como saber se está no venv certo

which python (Git Bash) ou where python (PowerShell/CMD) deve apontar para ...\cdd\.venv\Scripts\python.exe.

O teste:
python -c "import sys, streamlit as s; print(sys.executable); print(s.__version__, hasattr(s,'session_state'))"
deve mostrar o executável dentro do .venv e True no final.

# (1) sair de qualquer venv atual
deactivate  # ignore se der erro
# (2) criar venv com o Python 3.12
py -3.12 -m venv .venv
# (3) ativar
.\.venv\Scripts\Activate.ps1   # PowerShell
# ou, no Git Bash:
source .venv/Scripts/activate
# (4) instalar deps
python -m pip install -r requirements.txt
# (5) rodar
python -m streamlit run app.py

# Dicas úteis
- Ver versões instaladas do Python (via launcher):
py -0p
(mostra todas as versões e caminhos)

- Sem o launcher (usar o python que estiver no PATH)
Se py não funcionar no seu terminal, crie o venv com o python atual:
deactivate || true
python -V                       # confira a versão
python -m venv .venv
source .venv/Scripts/activate   # PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py


# Teste rápido (em Python no terminal)
python - << 'PY'
from core.paths import ROOT, ASSETS, STORAGE, PERIODOS_JSON, SEEDS
print("ROOT:", ROOT)
print("ASSETS exists:", ASSETS.exists())
print("STORAGE exists:", STORAGE.exists())
print("PERIODOS_JSON:", PERIODOS_JSON)
print("SEEDS:", SEEDS)
PY