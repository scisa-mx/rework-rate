from database import Base
import uuid
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship



class TagDB(Base):
    __tablename__ = "tags"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    color = Column(String, nullable=True) 
    
    repositories = relationship(
        "RepositoryEntity",
        secondary="repository_tags",
        back_populates="tags"
    )