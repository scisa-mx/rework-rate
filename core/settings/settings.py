# settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
from sqlalchemy.engine import URL
from urllib.parse import quote_plus


class Settings(BaseSettings):
    db_driver: str = Field(..., alias="DB_DRIVER")
    db_server: str = Field(..., alias="DB_SERVER")
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_auto_create_tables: bool = Field(default=False, alias="DB_AUTO_CREATE_TABLES")

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def sqlalchemy_url(self) -> URL:
        connection_string = (
            # Aquí está el cambio clave: DRIVER={TuControlador}
            f"DRIVER={{{self.db_driver}}};"
            f"SERVER={self.db_server},{self.db_port};"
            f"DATABASE={self.db_name};"
            f"UID={self.db_user};"
            f"PWD={self.db_password}"
        )
        return URL.create(
            "mssql+pyodbc",
            query={"odbc_connect": quote_plus(connection_string)}
        )