import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    ENV = os.getenv("ENV")
    DATABASE_URL = os.getenv("DATABASE_URL")
    if ENV == "production":
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    else:
        conn = psycopg2.connect(DATABASE_URL)
        return conn