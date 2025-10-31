# OmniDesk — quick start (dev)

This README covers the minimal steps to get a local development backend running for frontend integration and testing.

Prerequisites
- Python 3.11 (recommended). Python 3.10 should also work.
- Git
- MySQL / MariaDB (optional; you can point to an existing DB)
- Redis (optional)

Setup (PowerShell on Windows)

1) Create and activate a virtualenv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3) Copy example environment file and edit values

```powershell
Copy-Item .env.example .env
# then open .env and set DATABASE_*, JWT_SECRET, etc.
```

4) Start the dev server (assumes `python/api_server.py` exposes `app`)

```powershell
# if using the venv's python
.\.venv\Scripts\python -m uvicorn python.api_server:app --host 0.0.0.0 --port 8000 --reload
# or using uvicorn directly
uvicorn python.api_server:app --reload
```

5) Open API docs

Visit http://localhost:8000/docs for interactive OpenAPI docs once the server is running.

Run tests

```powershell
pytest -q
```

Notes
- The project expects several environment variables (see `.env.example`).
- JWT secret (`JWT_SECRET`) should be a sufficiently strong random string for local testing.
- In dev you can use a local MySQL instance or change `DATABASE_HOST` to point to a dev DB. Alternatively, modify repo code to use Sqlite for quick local runs.

Where to go next
- `API_CONTRACT.md` (root) — formalized API endpoints and curl examples for frontend consumption.
- `python/api_server.py` — (not yet present) FastAPI application scaffold; starting it will expose `/docs` and the endpoints described in `API_CONTRACT.md`.

