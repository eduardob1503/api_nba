# 🏀 NBA Stats API

API RESTful para consulta e gerenciamento de estatísticas de jogadores da NBA, com autenticação JWT, controle de acesso por roles e deploy em produção.

🌐 **Demo ao vivo:** [https://nba-stats-api-kfwn.onrender.com](https://nba-stats-api-kfwn.onrender.com)
> Serviço no plano gratuito do Render — pode levar ~30s na primeira requisição após inatividade.

---

## 🚀 Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| Python 3 + Flask | Framework web e roteamento |
| PostgreSQL + psycopg2 | Banco de dados relacional |
| PyJWT | Autenticação stateless com tokens |
| bcrypt | Hash seguro de senhas |
| gunicorn | Servidor WSGI para produção |
| python-dotenv | Gerenciamento de variáveis de ambiente |

---

## 📁 Estrutura do Projeto

```
nba-stats-api/
├── app.py                  # Inicialização do app e registro dos blueprints
├── config.py               # DATABASE_URL e SECRET_KEY via variáveis de ambiente
├── database.py             # Função conectar() com suporte a SSL em produção
├── Procfile                # Comando de start para o Render (gunicorn)
├── requirements.txt        # Dependências do projeto
├── .env.example            # Modelo de variáveis de ambiente
├── auths/
│   ├── __init__.py
│   └── routes.py           # POST /login  |  POST /cadastro
├── jogadores/
│   ├── __init__.py
│   └── routes.py           # CRUD /jogadores
├── middlewares/
│   ├── __init__.py
│   └── auth.py             # @login_required  |  @admin_required
└── README.md
```

---

## ⚙️ Como rodar localmente

### Pré-requisitos

- Python 3.10+
- PostgreSQL rodando localmente
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/eduardob1503/nba-stats-api.git
cd nba-stats-api
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o `.env`

Copie o modelo e preencha com suas credenciais:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/nba
SECRET_KEY=sua_chave_secreta_aqui
ENV=development
```

Gere uma SECRET_KEY segura com:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Configure o banco de dados

```sql
CREATE DATABASE nba;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    senha TEXT,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE jogadores (
    id SERIAL PRIMARY KEY,
    code_jogador VARCHAR(20) UNIQUE,
    nome VARCHAR(100)
);

CREATE TABLE ppg (
    id SERIAL PRIMARY KEY,
    id_jogador VARCHAR(20) REFERENCES jogadores(code_jogador),
    pontos NUMERIC
);
```

Para promover um usuário a admin:
```sql
UPDATE usuarios SET is_admin = TRUE WHERE email = 'seu@email.com';
```

### 5. Suba a API

```bash
python app.py
```

Disponível em `http://localhost:5000`.

---

## 🔐 Autenticação

A API usa **JWT Bearer Token**. Inclua o token no header de todas as rotas protegidas:

```
Authorization: Bearer <seu_token>
```

| Role | Rotas disponíveis |
|------|------------------|
| 🔓 Público | `POST /cadastro`, `POST /login` |
| 🔒 Usuário logado | `GET /jogadores`, `GET /jogadores/:code` |
| 👑 Admin | Todas as rotas + `POST /jogadores`, `POST /jogadores/:code`, `DELETE /jogadores/:code` |

---

## 📌 Endpoints

### Autenticação

#### `POST /cadastro`
Cria um novo usuário.

```json
// Body
{ "nome": "Eduardo Viana", "email": "eduardo@email.com", "senha": "minhasenha123" }

// Resposta 200
"usuario criado com sucesso"
```

#### `POST /login`
Retorna um token JWT válido por **1 hora**.

```json
// Body
{ "email": "eduardo@email.com", "senha": "minhasenha123" }

// Resposta 200
{ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
```

---

### Jogadores

#### `GET /jogadores` — 🔒 Login
Lista todos os jogadores cadastrados.

```json
// Resposta 200
[
  { "id": "jamesle01", "nome": "LeBron James" },
  { "id": "curryst01", "nome": "Stephen Curry" }
]
```

#### `GET /jogadores/<code>` — 🔒 Login
Retorna estatísticas de um jogador. Se não houver pontos, retorna dados básicos do cadastro.

```json
// Resposta 200 — com pontos registrados
{
  "id": "jamesle01",
  "pontos": [28, 31, 19, 24],
  "id_partida": [1, 2, 3, 4],
  "media": 25.5,
  "jogos": 4
}

// Resposta 200 — sem pontos ainda
{ "code": "jamesle01", "nome": "LeBron James" }
```

#### `POST /jogadores` — 👑 Admin
Cadastra um novo jogador. O `code` é gerado automaticamente a partir do nome.

```json
// Body
{ "nome": "LeBron James" }

// Resposta 201
{ "nome": "LeBron James", "code": "jamesle01" }
```

#### `POST /jogadores/<code>` — 👑 Admin
Adiciona registros de pontuação para um jogador.

```json
// Body
{ "pontos": [28, 31, 19] }

// Resposta 201
{ "pontos": [28, 31, 19] }
```

#### `DELETE /jogadores/<code>` — 👑 Admin
Remove o jogador e todos os seus registros de pontuação.

```json
// Resposta 200
{ "mensagem": "jogador deletado" }
```

---

## 🛡️ Segurança

- Senhas com **bcrypt** (hash + salt automático)
- Tokens JWT com **expiração de 1 hora** (`exp` + `iat` no payload)
- Credenciais em **variáveis de ambiente** — nunca no código
- Conexão com banco via **SSL em produção** (`sslmode=require`)
- Decorators reutilizáveis `@login_required` e `@admin_required`
- Erros JWT diferenciados: token expirado vs. token inválido vs. erro interno

---

## 📊 Roadmap

- [ ] Context manager para conexões automáticas com o banco
- [ ] Rate limiting no `/login` com Flask-Limiter
- [ ] Testes automatizados com pytest
- [ ] Stats avançadas: `max`, `min`, desvio padrão por jogador
- [ ] Endpoint `/jogadores/:code/tendencia` — média dos últimos 5/10/15 jogos
- [ ] Integração com dados reais via `nba_api` (PyPI)
- [ ] Documentação interativa com Swagger (Flask-RESTX)
- [ ] Docker Compose para ambiente de desenvolvimento

---

## 👨‍💻 Autor

**Eduardo Barcelos Viana**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-eduardo--viana1503-blue?style=flat&logo=linkedin)](https://linkedin.com/in/eduardo-viana1503)
[![GitHub](https://img.shields.io/badge/GitHub-eduardob1503-black?style=flat&logo=github)](https://github.com/eduardob1503)