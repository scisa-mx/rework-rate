import strawberry
from sqlalchemy.orm import Session
from services.tag_service import TagService
from schemas.tags.tags_types import TagType
from schemas.tags.tags_types import TagFilter
from typing import Optional, List

@strawberry.type
class TagQuery:
    @strawberry.field
    def get_all_tags(self, info, filters: Optional[TagFilter] = None) -> List[TagType]:
        db: Session = info.context["db"]
        service = TagService(db)

        tags = service.get_all_tags(filters)
        return [TagType(id=str(tag.id), name=tag.name, color=tag.color) for tag in tags]
    
