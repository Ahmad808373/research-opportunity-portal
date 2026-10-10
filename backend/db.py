"""One connection per request; Flask closes it even if a request fails."""
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from flask import g

load_dotenv(Path(__file__).with_name('.env'))


def get_connection():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'portal_user'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'research_portal'),
            charset='utf8mb4',
            connection_timeout=5,
            autocommit=False,
        )
    return g.db


def close_connection(error=None):
    connection = g.pop('db', None)
    if connection is not None:
        # An unfinished transaction is rolled back on close.
        connection.close()
