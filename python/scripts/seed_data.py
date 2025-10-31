#!/usr/bin/env python3
"""Seed script to populate demo data (admin, employee, clients, products, orders).

Usage:
  python python/scripts/seed_data.py [--dry-run] [--force]

--dry-run prints planned actions. --force executes them using existing repo adapters.
"""
from __future__ import annotations
import argparse
from datetime import datetime
from decimal import Decimal
from typing import List

from python.app.repos.app_user_repo import AppUserRepo
from python.app.repos.client_repo import ClientRepo
from python.app.repos.product_repo import ProductRepo
from python.app.repos.order_repo import OrderRepo
from python.app.core.security import hash_password, create_access_token


ADMIN_CREDENTIALS = {"username": "admin", "password": "adminpass", "full_name": "Admin User", "email": "admin@example.com", "role": "admin"}
EMPLOYEE_CREDENTIALS = {"username": "employee", "password": "employeepass", "full_name": "Empleado", "email": "empleado@example.com", "role": "empleado"}

PRODUCTS = [
    {"sku": "P-100", "name": "Router X100", "description": "Router inalámbrico", "price": Decimal('1200.00'), "stock": 10},
    {"sku": "P-101", "name": "Switch S24", "description": "Switch 24 puertos", "price": Decimal('2500.00'), "stock": 5},
    {"sku": "P-102", "name": "Cable CAT6", "description": "Cable de red 1m", "price": Decimal('20.00'), "stock": 200},
]


def run(dry_run: bool = True, force: bool = False):
    actions: List[str] = []

    # admin
    actions.append(f"Create admin user: {ADMIN_CREDENTIALS['username']}")
    actions.append(f"Create employee user: {EMPLOYEE_CREDENTIALS['username']}")

    # clients
    actions.append("Create demo client: Maria Lopez")

    # products
    for p in PRODUCTS:
        actions.append(f"Create product: {p['sku']} - {p['name']} ({p['price']})")

    # sample order (will be created after products/clients exist)
    actions.append("Create sample order for demo client with 1x Router X100")

    if dry_run:
        print("--- DRY RUN: planned actions ---")
        for a in actions:
            print(" - ", a)
        print("--- end planned actions ---")
        return

    # Execute
    print("Executing seed (this will write to the configured DB)...")

    # create admin and employee
    urepo = AppUserRepo()
    for creds in (ADMIN_CREDENTIALS, EMPLOYEE_CREDENTIALS):
        data = {"full_name": creds['full_name'], "username": creds['username'], "email": creds['email'], "password_hash": hash_password(creds['password']), "role": creds['role'], "active": True}
        try:
            uid = urepo.create(data)
            print(f"Created user {creds['username']} id={uid}")
        except Exception as exc:
            print(f"Failed creating user {creds['username']}: {exc}")

    # create client
    crepo = ClientRepo()
    client = {"full_name": "María López", "email": "maria@example.com", "phone": "+5215512345678"}
    try:
        cid = crepo.create(client)
        print(f"Created client id={cid}")
        token = create_access_token({"client_id": cid, "type": "client"})
        print("Client token (use for API calls):", token)
    except Exception as exc:
        print("Failed creating client:", exc)
        cid = None

    # create products
    prepo = ProductRepo()
    prod_ids = []
    for p in PRODUCTS:
        try:
            pid = prepo._legacy.create({"sku": p['sku'], "name": p['name'], "description": p['description'], "price": p['price'], "stock": p['stock'], "status": 'active'})
            prod_ids.append(pid)
            print(f"Created product {p['sku']} id={pid}")
        except Exception as exc:
            print(f"Failed creating product {p['sku']}: {exc}")

    # create sample order if we have a client and a product
    if cid and prod_ids:
        orepo = OrderRepo()
        try:
            created = orepo.create({"client_id": cid, "items": [{"product_id": prod_ids[0], "quantity": 1}], "notes": "Orden demo"})
            print(f"Created demo order id={created.order_id if hasattr(created, 'order_id') else created}")
        except Exception as exc:
            print("Failed creating demo order:", exc)

    print("Seed complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.dry_run or not args.force:
        run(dry_run=True)
    else:
        run(dry_run=False, force=True)
