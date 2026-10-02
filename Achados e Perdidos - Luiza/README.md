# Achados & Perdidos

Mini aplicação web para cadastrar e localizar itens perdidos/encontrados, com interface responsiva em tons violetas.

## Recursos
- Cadastro de item perdido ou encontrado, com nome, descrição, local e contato
- Mural com filtros Todos / Perdidos / Encontrados
- Busca por palavra-chave (nome, descrição e local)
- Upload opcional de imagem (PNG, JPG, GIF, WEBP; limite de 5 MB)
- Marcar como resolvido e reabrir
- Feedback visual e layout responsivo

## Tecnologias
Python 3.10+, Flask, SQLite, HTML, CSS e JavaScript.

## Executar localmente
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000

O banco `achados.db` é criado automaticamente. Para produção, defina `SECRET_KEY`, desative `debug` e configure armazenamento seguro para uploads.

## Estrutura
```text
achados-e-perdidos/
├── app.py
├── requirements.txt
├── README.md
├── templates/index.html
└── static/
    ├── css/style.css
    ├── js/app.js
    └── uploads/
```

## Publicar no GitHub
Crie um repositório vazio no GitHub e execute:
```bash
git init
git add .
git commit -m "feat: mini app Achados e Perdidos"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/achados-e-perdidos.git
git push -u origin main
```
Depois, envie o link do repositório para eduardo.hernandes@docente.senai.br.
