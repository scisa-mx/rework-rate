import strawberry
from typing import Optional
import uuid

@strawberry.input
class RepositoryCreateInput:
    name: str
    repo_url: str
    description: Optional[str] = None

@strawberry.input
class RepositoryUpdateInput:
    id: uuid.UUID  # Para identificar qué repo actualizar
    name: Optional[str] = None
    repo_url: Optional[str] = None
    description: Optional[str] = None

@strawberry.input
class RepositoryFilterInput:
    name: Optional[str] = None
    description: Optional[str] = None