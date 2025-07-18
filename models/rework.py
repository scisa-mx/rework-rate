from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Table
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
import uuid
from database import Base


rework_data_tags = Table(
    "rework_data_tags",
    Base.metadata,
    Column("rework_data_id", Integer, ForeignKey("rework_data.id"), primary_key=True),
    Column("tag_id", UNIQUEIDENTIFIER, ForeignKey("tags.id"), primary_key=True)
)

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
    tags = relationship("TagDB", secondary=rework_data_tags, backref="reworks")
    repository_id = Column(UNIQUEIDENTIFIER, ForeignKey("repositories.id"))
    repository = relationship("RepositoryEntity", back_populates="rework_data")
    
