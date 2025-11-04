#!/usr/bin/env python3
"""
Seed script para poblar la base de datos OmniDesk con datos realistas y amplios:
usuarios, clientes, categorías, productos, catálogos y asociaciones.
"""

from __future__ import annotations
import argparse
from datetime import datetime, timedelta
from decimal import Decimal
from random import randint, sample
from typing import List
from python.app.repos.app_user_repo import AppUserRepo
from python.app.repos.client_repo import ClientRepo
from python.app.repos.category_repo import CategoryRepo
from python.app.repos.product_repo import ProductRepo
from python.app.repos.catalog_repo import CatalogRepo
from python.app.repos.catalog_product_repo import CatalogProductRepo
from python.app.core.security import hash_password, create_access_token


# =========================================================
# Datos base
# =========================================================
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "adminpass",
    "full_name": "Administrador General",
    "email": "admin@omnidesk.com",
    "role": "admin",
}
EMPLOYEE_CREDENTIALS = {
    # Tests expect an 'employee' user with password 'employeepass'. Keep
    # these values in English to match the test suite.
    "username": "employee",
    "password": "employeepass",
    "full_name": "Empleado de Ventas",
    "email": "empleado@omnidesk.com",
    "role": "empleado",
}

# =========================================================
# Categorías jerárquicas
# =========================================================
CATEGORIES = [
    {"name": "Electrónica", "children": [
        "Computadoras", "Smartphones", "Accesorios", "Redes", "Audio y Video"
    ]},
    {"name": "Hogar y Oficina", "children": [
        "Muebles", "Electrodomésticos", "Papelería", "Decoración"
    ]},
    {"name": "Moda", "children": [
        "Ropa", "Zapatos", "Accesorios de Moda"
    ]},
    {"name": "Deportes", "children": [
        "Fitness", "Ciclismo", "Natación", "Senderismo"
    ]},
]

# =========================================================
# Productos (realistas)
# =========================================================
PRODUCTS = [
    # Electrónica
    {"sku": "EL-1001", "name": "Laptop HP Pavilion 15", "description": "Intel i5, 8GB RAM, 512GB SSD", "price": Decimal("14500.00"), "stock": 25, "category": "Computadoras"},
    {"sku": "EL-1002", "name": "Apple iPhone 14 128GB", "description": "Pantalla OLED de 6.1 pulgadas, cámara dual", "price": Decimal("18500.00"), "stock": 15, "category": "Smartphones"},
    {"sku": "EL-1003", "name": "Audífonos Sony WH-1000XM5", "description": "Cancelación activa de ruido", "price": Decimal("6800.00"), "stock": 30, "category": "Audio y Video"},
    {"sku": "EL-1004", "name": "Teclado Mecánico Logitech G Pro", "description": "Switches GX Blue, RGB", "price": Decimal("2200.00"), "stock": 40, "category": "Accesorios"},
    {"sku": "EL-1005", "name": "Router TP-Link Archer AX50", "description": "Wi-Fi 6, Dual Band, 3 Gbps", "price": Decimal("2100.00"), "stock": 20, "category": "Redes"},
    {"sku": "EL-1006", "name": "Monitor Dell Ultrasharp 27\"", "description": "Resolución QHD, panel IPS", "price": Decimal("7200.00"), "stock": 18, "category": "Computadoras"},
    {"sku": "EL-1007", "name": "Disco Duro Externo Seagate 2TB", "description": "USB 3.0, portátil", "price": Decimal("1500.00"), "stock": 60, "category": "Accesorios"},
    {"sku": "EL-1008", "name": "Cable HDMI 2.1 2m", "description": "Soporta 8K UHD y HDR", "price": Decimal("180.00"), "stock": 200, "category": "Accesorios"},

    # Hogar y Oficina
    {"sku": "HO-2001", "name": "Silla Ergonómica de Oficina", "description": "Respaldo de malla, soporte lumbar", "price": Decimal("3200.00"), "stock": 12, "category": "Muebles"},
    {"sku": "HO-2002", "name": "Escritorio de Madera 120cm", "description": "Color nogal con estructura metálica", "price": Decimal("2800.00"), "stock": 10, "category": "Muebles"},
    {"sku": "HO-2003", "name": "Refrigerador LG Smart Inverter", "description": "Capacidad 420L, eficiencia A+", "price": Decimal("9800.00"), "stock": 8, "category": "Electrodomésticos"},
    {"sku": "HO-2004", "name": "Lámpara de Escritorio LED", "description": "Luz blanca cálida, regulable", "price": Decimal("450.00"), "stock": 100, "category": "Decoración"},
    {"sku": "HO-2005", "name": "Paquete de hojas tamaño carta", "description": "500 hojas blancas", "price": Decimal("95.00"), "stock": 400, "category": "Papelería"},

    # Moda
    {"sku": "MO-3001", "name": "Playera Nike Dri-FIT", "description": "Tela transpirable, color negro", "price": Decimal("550.00"), "stock": 80, "category": "Ropa"},
    {"sku": "MO-3002", "name": "Tenis Adidas Ultraboost 23", "description": "Amortiguación premium", "price": Decimal("2800.00"), "stock": 40, "category": "Zapatos"},
    {"sku": "MO-3003", "name": "Reloj Casio Vintage Dorado", "description": "Resistente al agua, estilo clásico", "price": Decimal("900.00"), "stock": 30, "category": "Accesorios de Moda"},

    # Deportes
    {"sku": "DE-4001", "name": "Mancuernas Ajustables 24kg", "description": "Set ajustable con selector rápido", "price": Decimal("3500.00"), "stock": 25, "category": "Fitness"},
    {"sku": "DE-4002", "name": "Bicicleta de Montaña Trek Marlin 7", "description": "Cuadro de aluminio, frenos de disco", "price": Decimal("15800.00"), "stock": 6, "category": "Ciclismo"},
    {"sku": "DE-4003", "name": "Gafas de Natación Speedo Aquapulse", "description": "Antivaho y protección UV", "price": Decimal("480.00"), "stock": 50, "category": "Natación"},
    {"sku": "DE-4004", "name": "Mochila de Senderismo 50L", "description": "Impermeable con soporte lumbar", "price": Decimal("1200.00"), "stock": 35, "category": "Senderismo"},
]

# =========================================================
# Catálogos de campaña
# =========================================================
CATALOGS = [
    {"name": "Black Friday", "description": "Descuentos especiales de temporada", "discount_percentage": Decimal("25.00"), "visible_to": "todos"},
    {"name": "Clientes Premium", "description": "Ofertas exclusivas para clientes premium", "discount_percentage": Decimal("15.00"), "visible_to": "premium"},
    {"name": "Verano Tech", "description": "Descuentos en electrónica y gadgets", "discount_percentage": Decimal("10.00"), "visible_to": "todos"},
]

# =========================================================
# Clientes simulados
# =========================================================
CLIENTS = [
    {"full_name": "María López", "email": "maria@example.com", "phone": "+5215512345678"},
    {"full_name": "Carlos Hernández", "email": "carlos@example.com", "phone": "+5215511111111"},
    {"full_name": "Ana Pérez", "email": "ana@example.com", "phone": "+5215522222222"},
    {"full_name": "Luis González", "email": "luis@example.com", "phone": "+5215533333333"},
    {"full_name": "Fernanda Castillo", "email": "fer@example.com", "phone": "+5215544444444"},
]


# =========================================================
# Ejecución
# =========================================================
def run(dry_run: bool = True, force: bool = False):
    actions: List[str] = []

    actions += [f"Usuario: {ADMIN_CREDENTIALS['username']}", f"Usuario: {EMPLOYEE_CREDENTIALS['username']}"]
    actions += [f"Categorías: {len(CATEGORIES)} grupos principales", f"Productos: {len(PRODUCTS)} elementos"]
    actions += [f"Catálogos: {len(CATALOGS)} campañas"]
    actions += [f"Clientes: {len(CLIENTS)} registros demo"]

    if dry_run:
        print("--- DRY RUN: acciones previstas ---")
        for a in actions:
            print(" -", a)
        print("--- fin del resumen ---")
        return

    print("Ejecutando seed ampliado...")

    # Usuarios
    urepo = AppUserRepo()
    for creds in (ADMIN_CREDENTIALS, EMPLOYEE_CREDENTIALS):
        data = {
            "full_name": creds["full_name"],
            "username": creds["username"],
            "email": creds["email"],
            "password_hash": hash_password(creds["password"]),
            "role": creds["role"],
            "active": True,
        }
        try:
            urepo.create(data)
            print(f"Usuario creado: {creds['username']}")
        except Exception as e:
            print("Usuario ya existente:", e)

    # Categorías
    catrepo = CategoryRepo()
    category_map = {}
    for group in CATEGORIES:
        parent_id = catrepo.create({"name": group["name"]})
        category_map[group["name"]] = parent_id
        for child in group["children"]:
            cid = catrepo.create({"name": child, "parent_id": parent_id})
            category_map[child] = cid
    print(f"{len(category_map)} categorías creadas.")

    # Clientes
    crepo = ClientRepo()
    client_ids = []
    for c in CLIENTS:
        cid = crepo.create(c)
        client_ids.append(cid)
        print("Cliente creado:", c["full_name"])
    print(f"{len(client_ids)} clientes insertados.")

    # Productos
    prepo = ProductRepo()
    product_ids = []
    for p in PRODUCTS:
        pid = prepo._legacy.create({
            "sku": p["sku"],
            "name": p["name"],
            "description": p["description"],
            "price": p["price"],
            "stock": p["stock"],
            "status": "active",
            "category_id": category_map.get(p["category"]),
        })
        product_ids.append(pid)
    print(f"{len(product_ids)} productos insertados.")

    # Catálogos
    cat_repo = CatalogRepo()
    catalog_ids = []
    for cat in CATALOGS:
        cid = cat_repo.create({
            "name": cat["name"],
            "description": cat["description"],
            "discount_percentage": cat["discount_percentage"],
            "visible_to": cat["visible_to"],
            "start_date": datetime.now().date(),
            "end_date": (datetime.now() + timedelta(days=30)).date(),
        })
        catalog_ids.append(cid)
    print(f"{len(catalog_ids)} catálogos creados.")

    # Asociaciones Catálogo-Producto (sin exceder stock)
    cp_repo = CatalogProductRepo()
    for cid in catalog_ids:
        selected = sample(product_ids, randint(5, 10))
        for pid in selected:
            try:
                product = prepo.get(pid)
                available_stock = int(getattr(product, "stock", 0))
            except Exception:
                available_stock = 0

            if available_stock <= 0:
                continue

            assigned = randint(1, max(1, available_stock // 2))
            try:
                cp_repo.create({
                    "catalog_id": cid,
                    "product_id": pid,
                    "special_price": None,
                    "assigned_stock": assigned,
                })
            except Exception as exc:
                print(f"⚠️ No se pudo asociar producto {pid} → catálogo {cid}: {exc}")

    print("Asociaciones catálogo-producto creadas sin exceder stock.")
    print("✅ Seed completado con éxito.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.dry_run or not args.force:
        run(dry_run=True)
    else:
        run(dry_run=False, force=True)
