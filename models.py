from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from pydantic import BaseModel
from datetime import datetime

# Modelo SQLAlchemy para la base de datos
class ReworkDataDB(Base):
    __tablename__ = "rework_data"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String(500))
    pr_number = Column(String(50), index=True)
    author = Column(String(100))
    pr_approver = Column(String(100))
    timestamp = Column(DateTime)
    total_commits = Column(Integer)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    modified_lines = Column(Integer)
    rework_lines = Column(Integer)
    rework_percentage = Column(Float)

# Modelo Pydantic para la API
class ReworkData(BaseModel):
    repo_url: str
    pr_number: str
    author: str
    pr_approver: str
    timestamp: datetime
    total_commits: int
    period_start: datetime
    period_end: datetime
    modified_lines: int
    rework_lines: int
    rework_percentage: float

    class Config:
        from_attributes = True 