from sqlalchemy.orm import Session
import strawberry
from schemas.tags.tags_types import TagType
from services.tag_service import TagService


@strawberry.type
class TagQuery:
    @strawberry.field
    def get_all_tags(self, info) -> list[TagType]:
        db: Session = info.context["db"]
        service = TagService(db)

        tags = service.get_all_tags()
        return [TagType(id=str(tag.id), name=tag.name, color=tag.color) for tag in tags]
