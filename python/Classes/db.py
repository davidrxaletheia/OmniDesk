# -*- coding: utf-8 -*-
# Classes/db.py
import os
import mysql.connector

# Variables de entorno (con defaults)
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "omnidesk")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

def get_connection(autocommit: bool=False):
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
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
