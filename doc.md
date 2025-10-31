TECNOLOGIAS
Frontend: React (Create React App)
UI / Routing / estilos: react-router-dom, styled-components, react-beautiful-dnd, react-icons, boxicons
Backend: Python + FastAPI
ASGI server: Uvicorn
ORM / DB driver: SQLAlchemy + PyMySQL / aiomysql (MySQL/MariaDB)
Cache / pubsub: Redis
Auth / seguridad: passlib[bcrypt], bcrypt, PyJWT, email-validator, cryptography
Validación / modelos: Pydantic
LLM / IA: LangChain + paquetes relacionados, LangGraph, LangSmith
Utilidades / extras: xlsx (Excel), testing-libs (Testing Library / pytest equiv. en frontend/backend)





Revisión y especificación
Qué: inspeccionar el repo actual (models Pydantic, repos, DB access) y documentar el contrato API final.
Entregable: API_CONTRACT.md (endpoints, parámetros, respuestas de ejemplo).
Criterio de aceptación: el frontend developer puede implementar llamadas sin consultar el backend (ej.: tiene ejemplos curl/postman).
Tiempo estimado: 1–2 horas.

Poner entorno reproducible
Qué: crear/actualizar requirements.txt y .env.example, y extender README.md con pasos de setup (crear venv, instalar, variables env).
Entregable: requirements.txt, .env.example, README.md (start dev).

Criterio: otro dev puede clonar y levantar la app localmente en < 15 minutos siguiendo README.
Notas: incluir instrucciones de la versión de Python.

Implementar servidor FastAPI (sync)
Qué: crear python/api_server.py con FastAPI y endpoints mínimos:
POST /api/login
GET /api/summary
GET /api/events?start=&end=
GET /api/tickets
GET /api/users
Reusar: Classes.repos.* para la lógica de datos; serializar Pydantic a JSON con ISO datetimes.
Entregable: python/api_server.py
Criterio: /docs funciona y muestra endpoints; GET /api/events devuelve JSON con eventos.

Autenticación y seguridad
Qué: implementar JWT (PyJWT) para autenticación; endpoint /api/login devuelve token. Añadir dependencia get_current_user.
Entregable: auth utilities + protección de endpoints sensibles.
Criterio: el frontend puede autenticarse y usar token en Authorization header.
Serializadores y utilidades
Qué: helpers para convertir pydantic -> JSON (renombrar campos si hace falta), paginación, parsing de fechas en query params.
Entregable: python/utils/serializers.py (o util en api_server.py).
Criterio: las respuestas JSON entregan datetimes en ISO-8601 legible por JS.
Endpoints CRUD y pruebas
Qué: CRUD básico (list/get/create) para tickets y events; pruebas unitarias con pytest (endpoints simulan DB usando una DB de test o mocks).
Entregable: tests en python/tests/.
Criterio: tests principales pasan; endpoints cubiertos.
Página HTML simple de prueba
Qué: src/project-html-simple/dashboard/calendar_simple.html. Muy simple:
Hace fetch a /api/events?start=&end= y muestra una tabla o lista.
Muestra cómo incluir token (ejemplo Bearer).
Entregable: archivo HTML + pequeño JS inline.
Criterio: cargando la página y habiendo arrancado el backend, se ven los eventos.
Seed de datos y scripts de desarrollo
Qué: script python/scripts/seed_data.py para poblar DB con usuarios/tickets/events de ejemplo.
Entregable: script + instrucciones en README.
Criterio: tras ejecutar seed, endpoints devuelven datos útiles.
Documentación y OpenAPI
Qué: verificar /docs, generar API_CONTRACT.md si es necesario, y crear ejemplos curl/postman.
Entregable: API_CONTRACT.md, Postman collection o lista de curl.
Criterio: frontend dev prueba endpoints sin necesitar explicaciones adicionales.
CI, lint y tests
Qué: GitHub Actions pipeline:
Instala deps
Ejecuta linter (ruff/flake8)
Ejecuta pytest
Entregable: .github/workflows/ci.yml
Criterio: PRs requieren tests passing for merge.
Docker y despliegue
Qué: crear Dockerfile para la app y docker-compose.yml para desarrollo con MySQL/Redis opcional.
Entregable: Dockerfile, docker-compose.yml.
Criterio: docker-compose up levanta app y DB.
Paquete de entrega al front-dev
Qué: crear repositorio/zip con:
src (HTML simple)
python/api_server.py
requirements.txt
.env.example
API_CONTRACT.md
seed scripts y README con pasos rápidos
Entregable: deliverable.zip o branch preparado.
Criterio: front-dev puede correr la app local y consumir APIs.
Plan de migración a SQLAlchemy/async + Redis (opcional)
Qué: documento con pasos concretos y orden de trabajo para migración.
Entregable: MIGRATION_PLAN.md.
Criterio: plan aprobado y estimación para ejecución.
Handoff y checklist final
Qué: run final quality gates, confirmar comportamiento, enviar entrega con ticket/README y lista de endpoints listos.
Entregable: checklist completada.
Criterio: todo en verde y listo para front-dev.
Notas técnicas y recomendaciones puntuales

Mantén los endpoints síncronos por ahora: reduce riesgos y permite reusar Classes/repo.
Usa JWT para simplicidad con React; documenta el header Authorization y el tiempo de expiración.
Devuelve datetimes con .isoformat() y en UTC si es posible.
Para CORS en dev, permite el origen local del HTML o sirve el HTML estático desde FastAPI para evitar problemas.
Entregable mínimo viable (MVP) para entregar al frontend dev:
Endpoints: /api/events (list), /api/tickets (list), /api/users (list), /api/login
HTML simple que hace fetch y muestra los datos
README + .env.example + seed script
OpenAPI docs
Riesgos y consideraciones

Si migras DB a SQLAlchemy/async inmediatamente romperás compatibilidad con tus Repos; planifica en una branch y migración incremental.
Seguridad: no uses JWT sin HTTPS en producción; documenta la necesidad de certificados/HTTPS.
Tests: añade tests para evitar que refactorizaciones rompan el contrato API.