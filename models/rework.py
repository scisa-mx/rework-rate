from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from database import Base

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
    createdAtDate = Column(Date)
