import uuid
import strawberry
from typing import Optional

@strawberry.type
class RepositoryType:
    id: uuid.UUID
    name: str
    repo_url: str
    description: Optional[str]
