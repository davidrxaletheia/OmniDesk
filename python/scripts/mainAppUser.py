"""
Codigo para verificar el correcto funcionamiento de los app_user.

MENU:
    1. Listar todos los usuarios con sus detalles especificos
    2. Crear nuevo usuario.
    3. iniciar sesion con usuario existente.
        debera decir los detalles del usuario. entre ellos. el mas importante es su role.
    0. salir

"""
import email
import os
import sys
from pprint import pprint
from typing import Optional
from fastapi.testclient import TestClient

#hacer que el repo sea importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from python.app.main import app
from python.app.repos.app_user_repo import AppUserRepo

#Por qué: client nos permite llamar rutas como si fuésemos la app, y user_repo usa las funciones wrapper seguras para operar en app_user.
client = TestClient(app)
user_repo = AppUserRepo()

def list_users(limit: int):
    try:
        users = user_repo.list(limit=limit)
        for u in users:
            
            # u no puede ser un pydantic model o un fallback permisivo.
            uid = getattr(u, 'user_id', None) or (u.get('user_id') if isinstance(u, dict) else None)
            username = getattr(u, 'username', None) or (u.get('username') if isinstance(u, dict) else None)
            role = getattr(u, 'role', None) or (u.get('role') if isinstance(u, dict) else None)
            email = getattr(u, 'email', None) or (u.get('email') if isinstance(u, dict) else None)
            print(f"({uid}) - {username}\tRole: {role}\t {email}")
            print("-"*50)
            print(u)
            print("-"*50)
    except Exception as e:
        print("Error listando usuarios: ", repr(e))

def create_user(username: str, password: str, full_name: str, role: str, email: Optional[str] = None):
    
    username = username.strip()
    if not username:
        print("Username requerido")
        return
    password = password.strip()
    full_name = full_name.strip()
    role = role.strip()
    
    if email:
        email = email.strip()
    else:
        email = f"{username}@example.test"

    try:
        uid = user_repo.create({
            'username': username,
            'password': password,
            'full_name': full_name,
            'role': role,
            'email': email
        })
        print("Usuario creado! username -> ", username)
    except Exception as e:
        print("Error al crear un usuario: ", repr(e))

def login_as_admin(username: str, password: str) -> bool:
    """Login y comprobacion de role admin.

    Pide username/password al usuario, llama a /api/login y devuelve True
    si el campo `role` del usuario es 'admin' (case-insensitive), sino False.
    """
    r = client.post("/api/login", json={"username": username, "password": password})
    if r.status_code != 200:
        print("Login fallido:", r.status_code, r.text)
        return False

    body = r.json()
    # El endpoint devuelve {'access_token': ..., 'token_type': 'bearer', 'user': {...}}
    user = body.get("user")
    if not user:
        print("Respuesta de login no contiene 'user' ->", body)
        return False

    # user puede ser un dict o un Pydantic model-like (con .role)
    role = None
    if isinstance(user, dict):
        role = user.get("role")
    else:
        role = getattr(user, 'role', None)

    is_admin = str(role).lower() == 'admin'
    print(f"Role obtenido: {role!s} -> is_admin={is_admin}")
    return is_admin

def login_and_show(username: str, password: str) -> bool:
    return login_as_admin(username, password)

    #llamamos al endpoint /api/login (esta en routes/auth.py)
    r = client.post("/api/login", json={"username": username, "password": password})
    print("Status: ", r.status_code)
    if r.status_code != 200:
        print("Login Fallido: ", r.text)
        return False
    body = r.json()
    token = body.get("acces_token")
    user = body.get("user")
    print("Acces token: ", token)
    print("User details (desde /api.login:)")
    pprint(user)
    
    #refuerza: obtener direcxtamente desde el repo para comparar
    repo_user = user_repo.get_by_username(username)
    print("USer desde repo (get_by_username): ")
    pprint(repo_user)
    return True

def edit_user():
    #usamos la funcion login_and_show para aceptar los cambios
    if not login_and_show():
        return
    print("Edicion de usuario")
    print("Deja en blanco los campos que no quieras cambiar")
    username = input("Username (no se puede cambiar): ").strip()
    full_name = input("Full name (nuevo): ").strip()
    email = input("Email (nuevo): ").strip()

    # Actualizamos el usuario en el repo
    user_repo.update(username, {
        "full_name": full_name,
        "email": email
    })


if __name__ == "__main__":
    #Menu interactivo
    while True:
        print("\n--- Menu de gestion de App Users ---")
        print("1. Listar usuarios")
        print("2. Crear nuevo usuario")
        print("3. Iniciar sesion y mostrar detalles usuario")
        print("0. Salir")
        choice = input("Elige una opcion: ").strip()
        if choice == '1':
            list_users()
        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            full_name = input("Full name: ")
            role = input("Role (admin/empleado): ")
            email = input("Email (opcional): ")
            create_user(username, password, full_name, role, email)
        elif choice == '3':
            username = input("Username: ")
            password = input("Password: ")
            login_and_show(username, password)
        elif choice == '0':
            print("Saliendo...")
            break
        else:
            print("Opcion no valida, intenta de nuevo.")