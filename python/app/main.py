from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth
from .routes import summary, events, tickets, users  # routers implemented below
from .routes import products, clients, orders, alerts, calendar, categories, catalogs, catalog_products
from .routes import carts
from fastapi.openapi.utils import get_openapi


app = FastAPI(title="Omnidesk API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    # Include both localhost and 127.0.0.1 variants (common when serving test files)
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(summary.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(tickets.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(users.router_admin, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(calendar.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(catalogs.router, prefix="/api")
app.include_router(catalog_products.router, prefix="/api")
app.include_router(carts.router, prefix="/api")
# app.include_router(ai.router, prefix="/api")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
    # Add a Bearer auth scheme so Swagger UI shows the Authorize button.
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


