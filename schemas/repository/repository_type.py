import uuid
import strawberry
from typing import Optional, List
from schemas.tags.tags_types import TagType

@strawberry.type
class RepositoryType:
    id: uuid.UUID
    name: str
    repo_url: str
    description: Optional[str]
    tags: List[TagType]
