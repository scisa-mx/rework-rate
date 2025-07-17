import strawberry
import uuid
from sqlalchemy.orm import Session
from typing import List, Optional
from strawberry.types import Info
from models.repository import RepositoryEntity
from schemas.repository.repository_type import RepositoryType
from schemas.tags.tags_types import TagType

from repositories.repository_repository import RepositoryRepository
from services.repository_service import RepositoryService
from schemas.repository.repository_input import RepositoryFilterInput

@strawberry.type
class RepositoryQuery:
    @strawberry.field
    def get_all_repositories(self, info, filters: Optional[RepositoryFilterInput]) -> List[RepositoryType]:
        db: Session = info.context["db"]
        
        repo = RepositoryRepository(RepositoryEntity, db)
        service = RepositoryService(db, repo)

        res = service.get_repositories(filters)
        
        return res
    
    @strawberry.field
    def get_repository_by_id(self, info: Info, id: uuid.UUID) -> Optional[RepositoryType]:
        db: Session = info.context["db"]

        repo = RepositoryRepository(RepositoryEntity, db)
        service = RepositoryService(db, repo)

        repository = service.get_repository_by_id(id)

        return repository
