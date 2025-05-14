import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models.rework import ReworkDataDB

# Usa SQLite en memoria para tests rápidos
TEST_DATABASE_URL = "sqlite:///:memory:"

# Crear motor y sesión
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta fixture crea y destruye una base temporal
@pytest.fixture(scope="function")
def db_session():
    # Crea tablas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
