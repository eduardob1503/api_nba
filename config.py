import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "host":os.getenv("host"),
    "port": os.getenv("port"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "database": os.getenv("database")
}
SECRET_KEY = os.getenv("SECRET_KEY") 