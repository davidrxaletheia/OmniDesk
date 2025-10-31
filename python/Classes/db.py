# -*- coding: utf-8 -*-
# Classes/db.py
import os
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector

# Load environment variables from the repository root `.env` file (if present).
# We resolve the repo root relative to this file so loading works even when the
# script is executed from a different working directory.
ROOT = Path(__file__).resolve().parents[2]
env_path = ROOT / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # fallback to default behavior (search for .env in cwd or parent paths)
    load_dotenv()

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
# Leer DATABASE_PORT desde .env sin exigir comillas en el archivo .env.
# .env almacena valores como strings (ej `DATABASE_PORT=3306`), así que hacemos
# parsing seguro: si la variable está presente y no vacía la convertimos a int,
# si no, usamos el default 3306.
_port_val = os.getenv("DATABASE_PORT")
if _port_val is None or _port_val == "":
    DB_PORT = 3306
else:
    try:
        DB_PORT = int(_port_val)
    except ValueError:
        # Si alguien puso un valor no numérico, fallback al puerto por defecto
        DB_PORT = 3306

# Credentials must come from environment variables (.env). Do not hardcode them here.
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME")

# Validate required credential variables early and fail fast with a clear message.
# Accept empty passwords when the variable is explicitly present in the environment
# (common for local MySQL setups where root has an empty password). We treat a
# variable as missing only if it is not set at all in the environment (i.e. not
# present in os.environ). load_dotenv() will populate os.environ for keys defined
# in the .env file even if the value is empty.
missing = []
env = os.environ
if 'DATABASE_USER' not in env:
    missing.append('DATABASE_USER')
if 'DATABASE_PASSWORD' not in env:
    missing.append('DATABASE_PASSWORD')
if 'DATABASE_NAME' not in env:
    missing.append('DATABASE_NAME')
if missing:
    raise RuntimeError(
        "Missing required database environment variables: %s. "
        "Create a .env file (copy .env.example) or set these variables in your environment." % ", ".join(missing)
    )


def get_connection(autocommit: bool=False):
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=autocommit,
    )

class DB:
    """Helper de conexión con context manager."""
    def __init__(self, autocommit: bool=False):
        self.conn = get_connection(autocommit=autocommit)
        self.autocommit = autocommit
    def cursor(self):
        return self.conn.cursor()
    def commit(self):
        self.conn.commit()
    def rollback(self):
        self.conn.rollback()
    def close(self):
        try: self.conn.close()
        except: pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        if exc:
            if not self.autocommit: self.rollback()
        else:
            if not self.autocommit: self.commit()
        self.close()

#main para probar la conexión
if __name__ == "__main__":
    with DB() as db:
        cursor = db.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print("Conectado a la base de datos:", result[0])
        cursor.close()
