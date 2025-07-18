# db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# Cargar variables desde .env.development
load_dotenv(".env.development")

# Obtener variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

# Validación opcional
if not all([DB_USER, DB_PASSWORD, DB_SERVER, DB_PORT, DB_NAME, DB_DRIVER]):
    raise ValueError("Faltan variables de entorno requeridas para la conexión a la BD.")

# Crear cadena de conexión codificada
connection_string = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER},{DB_PORT};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)

# Crear URL para SQLAlchemy
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": quote_plus(connection_string)}
)

# Crear engine y sesión
engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar base para modelos
Base = declarative_base()

# Dependencia para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
