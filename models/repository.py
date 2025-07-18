import uuid
from typing import List, Optional
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from models.mixins import TimestampMixin, AuditMixin
from models.rework import ReworkDataDB
from models.tags import TagDB


# Tabla intermedia para la relación many-to-many
repository_tags = Table(
    "repository_tags",
    Base.metadata,
    Column("repository_id", ForeignKey("repositories.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class RepositoryEntity(Base, TimestampMixin, AuditMixin):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    repo_url: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relaciones
    rework_data: Mapped[List["ReworkDataDB"]] = relationship("ReworkDataDB", back_populates="repository")
    tags: Mapped[List["TagDB"]] = relationship("TagDB", secondary=repository_tags, back_populates="repositories")
