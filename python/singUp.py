"""Script y utilitario para iniciar sesión (login).

Provee:
- `authenticate(identifier, password, repo=None)` -> AppUserModel | None
  identifica por `username` o `email` y verifica la contraseña usando bcrypt.
- Modo interactivo cuando se ejecuta como script: pide credenciales y muestra
  resultado (sin crear tokens ni gestionar sesiones, solo demo local).

Uso (desde la raíz del repo):
	python python/singUp.py

Nota: el script asume que `Classes` está en el PYTHONPATH (ejecutar desde el
directorio raíz del proyecto para que `import Classes...` funcione).
"""

from __future__ import annotations

from getpass import getpass
from datetime import datetime
from typing import Optional

import bcrypt

from Classes.repos.app_user_repo import AppUserRepo
from Classes.models.app_user import AppUserModel


def authenticate(identifier: str, password: str, repo: Optional[AppUserRepo] = None) -> Optional[AppUserModel]:
	"""Authenticate a user by username or email using bcrypt.

	Returns the `AppUserModel` on success (and updates `last_login_at`), or
	None on failure.

	Parameters:
	- identifier: username or email
	- password: plain-text password to verify
	- repo: optional AppUserRepo instance (if provided, won't be closed here)
	"""
	own = False
	if repo is None:
		repo = AppUserRepo()
		own = True

	try:
		# Try username first
		user = repo.find_by_username(identifier)

		# If not found and identifier looks like an email, try search by email
		if not user and '@' in identifier:
			rows = repo.filter('email=%s', (identifier,), limit=1)
			user = rows[0] if rows else None

		if not user:
			return None

		stored_hash = (user.password_hash or '').encode('utf-8')
		if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
			# Update last_login_at
			try:
				repo.update(user.user_id, {'last_login_at': datetime.utcnow()})
			except Exception:
				# non-fatal: ignore update errors but still authenticate
				pass
			return user

		return None
	finally:
		if own:
			try:
				repo.close()
			except Exception:
				pass


def prompt_and_auth():
	print('Iniciar sesión — modo interactivo')
	identifier = input('Usuario o email: ').strip()
	password = getpass('Contraseña: ')

	user = authenticate(identifier, password)
	if user:
		print(f"Autenticación OK. Bienvenido, {user.full_name} (id={user.user_id})")
	else:
		print('Autenticación fallida. Usuario o contraseña incorrectos.')


if __name__ == '__main__':
	prompt_and_auth()

