from sqlalchemy.orm import Session
from typing import List
from models.rework import ReworkDataDB
from repositories.tag_repository import TagRepository
from models.tags import TagDB
from core.utils.colors.colors import get_next_available_color
from fastapi import HTTPException

class TagService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TagRepository(db)

    def update_tags_for_rework(self, rework_id: int, tag_names: List[str]) -> List[TagDB]:
        rework = self.db.query(ReworkDataDB).filter_by(id=rework_id).first()
        if not rework:
            raise HTTPException(status_code=404, detail="Repositorio no encontrado")

        current_tags = []
        for name in tag_names:
            tag = self.repo.get_by_name(name)
            if not tag:
                color = get_next_available_color(self.db)
                tag = self.repo.create(name, color)
            if tag not in rework.tags:
                rework.tags.append(tag)
            current_tags.append(tag)

        # Eliminar tags no incluidos
        for tag in list(rework.tags):
            if tag.name not in tag_names:
                rework.tags.remove(tag)

        self.db.commit()
        return rework.tags

    def get_all_tags(self) -> List[TagDB]:
        return self.repo.get_all()
