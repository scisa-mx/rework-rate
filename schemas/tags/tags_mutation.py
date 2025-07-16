from fastapi import HTTPException
from sqlalchemy.orm import Session
import strawberry
from schemas.tags.tags_types import TagType, TagInput
from services.tag_service import TagService

@strawberry.type
class TagMutation:
    @strawberry.mutation
    def update_tags(self, info, data: TagInput) -> list[TagType]:
        db: Session = info.context["db"]
        service = TagService(db)
        try:
            tags = service.update_tags_for_rework(data.rework_data_id, data.names)
            return [TagType(id=str(tag.id), name=tag.name, color=tag.color) for tag in tags]
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
