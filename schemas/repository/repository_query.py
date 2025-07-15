import strawberry
import uuid
from sqlalchemy.orm import Session
from typing import List, Optional
from strawberry.types import Info
from models.repository import RepositoryEntity
from schemas.repository.repository_type import RepositoryType
from schemas.tags.tags_types import TagType

@strawberry.type
class RepositoryQuery:
    
    @strawberry.field
    def get_all_repositories(self, info) -> List[RepositoryType]:
        db: Session = info.context["db"]
        repos = db.query(RepositoryEntity).all()

        return [
            RepositoryType(
                id=repo.id,
                name=repo.name,
                repo_url=repo.repo_url,
                description=repo.description,
            )
            for repo in repos
        ]

@strawberry.type
class RepositoryQuery:

    @strawberry.field
    def get_repository_by_id_or_name(
        self,
        info: Info,
        id: Optional[uuid.UUID] = None,
        name: Optional[str] = None
    ) -> Optional[RepositoryType]:
        db: Session = info.context["db"]

        if not id and not name:
            return None

        query = db.query(RepositoryEntity)

        if id:
            query = query.filter(RepositoryEntity.id == id)
        elif name:
            query = query.filter(RepositoryEntity.name.ilike(f"%{name}%"))

        repo = query.first()

        if not repo:
            return None

        return RepositoryType(
            id=repo.id,
            name=repo.name,
            repo_url=repo.repo_url,
            description=repo.description,
            tags=[
                TagType(id=tag.id, name=tag.name, color=tag.color)
                for tag in repo.tags
            ]
        )