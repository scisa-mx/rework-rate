from sqlalchemy.orm import Session
from typing import List, Optional
from models.tags import TagDB
from repositories.tag_repository import TagRepository
from fastapi import HTTPException
from core.utils.colors.colors import get_next_available_color  # para crear tags nuevos
from schemas.tags.tags_types import TagFilter

class TagService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TagRepository(db)

    def get_all_tags(self, filters: Optional[TagFilter] = None) -> List[TagDB]:
        if filters:
            return self.repo.get_by_filter(filters)
        return self.repo.get_all()

    def get_tag_by_id(self, tag_id: str) -> TagDB:
        tag = self.repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag no encontrado")
        return tag

    def create_tag(self, name: str) -> TagDB:
        existing = self.repo.get_by_name(name)
        if existing:
            raise HTTPException(status_code=400, detail="Tag con ese nombre ya existe")
        color = get_next_available_color(self.db)
        return self.repo.create(name, color)

    def update_tag(self, tag_id: str, name: Optional[str] = None, color: Optional[str] = None) -> TagDB:
        tag = self.get_tag_by_id(tag_id)
        if name:
            existing = self.repo.get_by_name(name)
            if existing and existing.id != tag_id:
                raise HTTPException(status_code=400, detail="Otro tag con ese nombre ya existe")
        return self.repo.update(tag, name, color)

    def delete_tag(self, tag_id: str) -> None:
        tag = self.get_tag_by_id(tag_id)
        self.repo.delete(tag)
