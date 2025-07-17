from sqlalchemy.orm import Session
from typing import List, Optional
from models.tags import TagDB
from repositories.tag_repository import TagRepository
from fastapi import HTTPException
from core.utils.colors.colors import get_next_available_color  # para crear tags nuevos
from schemas.tags.tags_types import TagFilter
from core.utils.colors.colors import validate_color

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

        if color:
            try:
                color = validate_color(color)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        # Solo validar nombre si es distinto del actual
        if name and name != tag.name:
            existing = self.repo.get_by_name(name)
            if existing and existing.id != tag_id:
                raise HTTPException(status_code=400, detail="Otro tag con ese nombre ya existe")

        # Solo enviar el nombre si cambió, para evitar tocarlo sin querer
        name_to_update = name if name and name != tag.name else None

        return self.repo.update(tag, name_to_update, color)
    
    def delete_tag(self, tag_id: str) -> None:
        tag = self.get_tag_by_id(tag_id)
        self.repo.delete(tag)


    def match_tag_name(self, tag_name: str) -> Optional[TagDB]:
        """
        Busca un tag por su nombre.
        """
        return self.repo.get_by_name(tag_name)