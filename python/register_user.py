"""Utility para registrar usuarios desde línea de comandos (modo local).

Características:
- Pide datos del usuario por consola (nombre, usuario, email, contraseña, rol, activo).
- Hashea la contraseña con bcrypt antes de guardarla.
- Usa `Classes.repos.app_user_repo.AppUserRepo` para persistir en la base de datos.
- Validación mínima con Pydantic (AppUserModel).

Ejecutar desde la raíz del proyecto:
    python python/register_user.py

Nota: el script asume que la configuración de conexión a MySQL está en
las variables de entorno o en `python/Classes/db.py` defaults.
"""
from __future__ import annotations

import sys
from getpass import getpass
from datetime import datetime
from typing import Optional

import bcrypt

from Classes.repos.app_user_repo import AppUserRepo
from Classes.models.app_user import AppUserModel


def hash_password(password: str) -> str:
    """Return bcrypt hash (utf-8 str) for the given password."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def prompt_input(prompt: str, default: Optional[str] = None) -> str:
    raw = input(f"{prompt}" + (f" [{default}]" if default else "") + ": ")
    if raw.strip() == "" and default is not None:
        return default
    return raw.strip()


def create_user_interactive() -> int:
    print("Registro de nuevo usuario — modo interactivo")
    full_name = prompt_input("Nombre completo")
    username = prompt_input("Nombre de usuario (username)")
    email = prompt_input("Email (opcional)", default="") or None

    # password (hidden)
    while True:
        password = getpass("Contraseña: ")
        password2 = getpass("Confirmar contraseña: ")
        if password != password2:
            print("Las contraseñas no coinciden. Intenta de nuevo.")
            continue
        if not password:
            print("La contraseña no puede estar vacía.")
            continue
        break

    role = prompt_input("Rol (admin/empleado)", default="empleado")
    role = role if role in ("admin", "empleado") else "empleado"
    active_raw = prompt_input("Activo? (s/n)", default="s")
    active = active_raw.lower().startswith('s')

    password_hash = hash_password(password)
    now = datetime.utcnow()

    # prepare data for DB insert according to AppUserModel
    data = {
        "full_name": full_name,
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "role": role,
        "active": active,
        "password_changed_at": now,
    }

    repo = AppUserRepo()
    try:
        # check unique username
        if repo.find_by_username(username):
            print(f"El nombre de usuario '{username}' ya existe. Abortando.")
            return 0

        # validate with pydantic model before insert
        _ = AppUserModel(**{**data})

        new_id = repo.create(data)
        print(f"Usuario creado con id: {new_id}")
        return new_id or 0
    finally:
        try:
            repo.close()
        except Exception:
            pass


def create_user(**kwargs) -> int:
    """Programmatic helper to create a user.

    Accepts fields: full_name, username, email (optional), password (raw),
    role, active (bool).

    Returns the new user id (int) or 0 if failed.
    """
    password = kwargs.pop('password', None)
    if not password:
        raise ValueError("'password' is required")

    password_hash = hash_password(password)
    kwargs['password_hash'] = password_hash
    kwargs.setdefault('password_changed_at', datetime.utcnow())

    repo = AppUserRepo()
    try:
        username = kwargs.get('username')
        if username and repo.find_by_username(username):
            raise ValueError(f"username '{username}' already exists")

        # validate
        _ = AppUserModel(**kwargs)

        new_id = repo.create(kwargs)
        return new_id or 0
    finally:
        repo.close()


if __name__ == '__main__':
    create_user_interactive()
