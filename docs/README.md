.
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ .env.example
├─ README.md
├─ requirements.txt
├─ API_CONTRACT.md
├─ Dockerfile
├─ docker-compose.yml
├─ doc.md
├─ database/
│  ├─ DATABASE_DOCUMENTATION.md
│  ├─ db.py
│  ├─ data/
│  │  └─ data.sql
│  └─ init/
│     └─ init.sql
├─ python/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py                    # entrypoint (uvicorn python.app.main:app)
│  │  ├─ core/
│  │  │  ├─ __init__.py
│  │  │  ├─ config.py               # BaseSettings (.env)
│  │  │  ├─ security.py             # JWT + passlib
│  │  │  └─ deps.py                 # get_db, get_current_user, DI
│  │  ├─ routes/
│  │  │  ├─ __init__.py
│  │  │  ├─ auth.py                 # /api/login
│  │  │  ├─ summary.py              # /api/summary
│  │  │  ├─ events.py               # /api/events
│  │  │  ├─ tickets.py              # /api/tickets
│  │  │  ├─ users.py                # /api/users
│  │  │  └─ ai.py                   # /api/ai/* (uses ai.client)
│  │  ├─ models/                    # Pydantic models (mover desde Classes/models)
│  │  │  ├─ __init__.py
│  │  │  ├─ app_user.py
│  │  │  ├─ ticket.py
│  │  │  ├─ calendar.py
│  │  │  └─ ...
│  │  ├─ repos/                     # wrappers o adaptadores para acceso DB
│  │  │  ├─ __init__.py
│  │  │  ├─ app_user_repo.py
│  │  │  ├─ ticket_repo.py
│  │  │  └─ event_repo.py
│  │  ├─ utils/
│  │  │  ├─ __init__.py
│  │  │  ├─ serializers.py          # ISO datetimes, Decimal -> JSON
│  │  │  └─ helpers.py
│  │  ├─ ai/                        # LangGraph / LLM layer
│  │  │  ├─ __init__.py
│  │  │  ├─ client.py               # LangGraph adapter (sync/async)
│  │  │  ├─ prompts.py              # prompt templates / builders
│  │  │  ├─ cache.py                # caching wrapper (Redis)
│  │  │  └─ mock_client.py          # para tests
│  │  ├─ scripts/
│  │  │  └─ seed_data.py
│  │  └─ tests/
│  │     ├─ conftest.py
│  │     ├─ test_auth.py
│  │     ├─ test_events.py
│  │     └─ test_ai.py
│  └─ Classes/                      # opcional: dejar como legacy o eliminar después
│     ├─ models/
│     └─ repos/
├─ src/                             # frontend static site & examples
│  ├─ index.html
│  ├─ dashboard_servicio.html
│  ├─ login.html
│  ├─ logout.html
│  ├─ assets/
│  └─ dashboard/
│     └─ ...
└─ docs/                            # documentación adicional
   └─ README.md