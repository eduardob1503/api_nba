import psycopg2
from config import DB_CONFIG
def conectar():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn