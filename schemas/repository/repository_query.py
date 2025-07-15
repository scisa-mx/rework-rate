import strawberry
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.repository import RepositoryEntity
from schemas.repository.repository_type import RepositoryType

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
