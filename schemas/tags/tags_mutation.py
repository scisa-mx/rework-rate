import strawberry
from sqlalchemy.orm import Session
from strawberry.types import Info
from fastapi import HTTPException
from services.tag_service import TagService
from schemas.tags.tags_types import TagType, TagInputCreate, TagInputUpdate


@strawberry.type
class TagMutation:

    @strawberry.mutation
    def create_tag(self, info: Info, data: TagInputCreate) -> TagType:
        db: Session = info.context["db"]
        service = TagService(db)
        tag = service.create_tag(data.name, data.color)
        return TagType(id=str(tag.id), name=tag.name, color=tag.color)

    @strawberry.mutation
    def update_tag(self, info: Info, data: TagInputUpdate) -> TagType:
        db: Session = info.context["db"]
        service = TagService(db)
        tag = service.update_tag(data.id, data.name, data.color)
        return TagType(id=str(tag.id), name=tag.name, color=tag.color)

    @strawberry.mutation
    def delete_tag(self, info: Info, tag_id: str) -> bool:
        db: Session = info.context["db"]
        service = TagService(db)
        service.delete_tag(tag_id)
        return True
