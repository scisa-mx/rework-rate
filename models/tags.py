from database import Base
import uuid
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import Column, String


class TagDB(Base):
    __tablename__ = "tags"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
