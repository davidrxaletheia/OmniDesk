"""Script de prueba que lanza el registro interactivo desde `python/register_user.py`.

Ejecutar (desde la raíz del repo):
	python python/Langgraph/test/signUp.py

Esto añade la carpeta `python/` al sys.path para poder importar el util
`register_user` y ejecutar su modo interactivo.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

try:
	from register_user import create_user_interactive
except Exception as e:
	print('No se pudo importar register_user:', e)
	sys.exit(1)


if __name__ == '__main__':
	create_user_interactive()

