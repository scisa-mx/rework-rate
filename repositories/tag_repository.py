from sqlalchemy.orm import Session
from models.tags import TagDB
from typing import Optional

class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[TagDB]:
        return self.db.query(TagDB).filter_by(name=name).first()

    def get_all(self) -> list[TagDB]:
        return self.db.query(TagDB).all()

    def create(self, name: str, color: str) -> TagDB:
        tag = TagDB(name=name, color=color)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
