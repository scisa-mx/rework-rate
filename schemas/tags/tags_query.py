from sqlalchemy.orm import Session
import strawberry
from models.tags import TagDB 
from schemas.tags.tags_types import TagType


@strawberry.type
class Query:
    @strawberry.field
    def get_all_tags(self, info) -> list[TagType]:
        db: Session = info.context["db"]
        records = db.query(TagDB).all()
        return [TagType(id=str(record.id), name=record.name, color=record.color) for record in records]
