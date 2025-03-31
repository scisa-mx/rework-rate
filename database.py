from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a MSSQL
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:2Oc28XhT65R0s7B@sql:1433/rework_rate?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()