from sqlalchemy.orm import Session
from models.tags import TagDB
from typing import Optional, List
from schemas.tags.tags_types import TagFilter
from sqlalchemy import and_


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, tag_id: str) -> Optional[TagDB]:
        return self.db.query(TagDB).filter_by(id=tag_id).first()

    def get_by_name(self, name: str) -> Optional[TagDB]:
        return self.db.query(TagDB).filter_by(name=name).first()

    def get_all(self) -> List[TagDB]:
        return self.db.query(TagDB).all()
    
    def get_by_filter(self, filters: TagFilter) -> list[TagDB]:
        query = self.db.query(TagDB)
        conditions = []
        if filters.id:
            conditions.append(TagDB.id == filters.id)
        if filters.name:
            conditions.append(TagDB.name.ilike(f"%{filters.name}%"))  # búsqueda parcial, case insensitive

        if conditions:
            query = query.filter(and_(*conditions))

        return query.all()

    def create(self, name: str, color: str) -> TagDB:
        tag = TagDB(name=name, color=color)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def update(self, tag: TagDB, name: Optional[str] = None, color: Optional[str] = None) -> TagDB:
        if name:
            tag.name = name
        if color:
            tag.color = color
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete(self, tag: TagDB) -> None:
        self.db.delete(tag)
        self.db.commit()
    
