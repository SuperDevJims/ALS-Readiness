# Backend Setup Guide

## Prerequisites

- Python 3.12+
- PostgreSQL
- `uv`

## 0. Install `uv`

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: via pip
pip install uv
```

Verify installation:

```bash
uv --version
```

> Restart your terminal if `uv` isn't recognized after install.

## 1. Install Dependencies

```bash
cd backend
uv sync
```

## 2. Set Up `.env`

```bash
cp .env.example .env
```

Fill in:

```env
# Database
DB_PORT=5432
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=<your_pg_password>
DB_NAME=alsense_db

# JWT
ACCESS_TOKEN_SECRET_KEY=<generate-your-own-secret>
REFRESH_TOKEN_SECRET_KEY=<generate-your-own-secret>
```

> Generate a secret key with: `python -c "import secrets; print(secrets.token_hex(32))"`

## 3. Create the Database

```bash
psql -U postgres -c "CREATE DATABASE alsense_db;"
```

(Match `DB_USER` and `DB_NAME` to whatever you set in `.env`)

## 4. Run Migrations

```bash
uv run alembic upgrade head
```

## 5. Seed the Database

```bash
uv run python -m scripts.seed_all
```

> Admin credentials will be printed in the terminal — save them.

## 6. Run the Server

```bash
uv run uvicorn app.main:app --reload
```

API: `http://localhost:8000`

Docs: `http://localhost:8000/docs`

---

## Troubleshooting

- **Missing module** → `uv sync` again
- **DB connection error** → check `DATABASE_URL` in `.env`
- **Windows async errors on Alembic** → already handled in code, pull latest
- **Don't run `alembic revision --autogenerate`** unless you're intentionally changing the schema — pull latest first
