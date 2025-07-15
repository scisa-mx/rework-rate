import strawberry
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends

from models.repository import RepositoryEntity
from schemas.repository.repository_type import RepositoryType
from schemas.repository.repository_input import RepositoryCreateInput, RepositoryUpdateInput
import uuid

@strawberry.type
class RepositoryMutation:

    @strawberry.mutation
    def create_repository(self, info, input: RepositoryCreateInput) -> RepositoryType:
        db: Session = info.context["db"]

        new_repo = RepositoryEntity(
            name=input.name,
            repo_url=input.repo_url,
            description=input.description,
        )

        db.add(new_repo)
        db.commit()
        db.refresh(new_repo)

        return RepositoryType(
            id=new_repo.id,
            name=new_repo.name,
            repo_url=new_repo.repo_url,
            description=new_repo.description
        )

    @strawberry.mutation
    def update_repository(self, info, input: RepositoryUpdateInput) -> RepositoryType:
        db: Session = info.context["db"]

        repo = db.query(RepositoryEntity).filter(RepositoryEntity.id == input.id).first()
        if not repo:
            raise Exception(f"Repository with id {input.id} not found")

        if input.name is not None:
            repo.name = input.name
        if input.repo_url is not None:
            repo.repo_url = input.repo_url
        if input.description is not None:
            repo.description = input.description

        db.commit()
        db.refresh(repo)

        return RepositoryType(
            id=repo.id,
            name=repo.name,
            repo_url=repo.repo_url,
            description=repo.description,
        )
    @strawberry.mutation
    def delete_repository(self, info, id: uuid.UUID) -> bool:
        db: Session = info.context["db"]

        repo = db.query(RepositoryEntity).filter(RepositoryEntity.id == id).first()
        if not repo:
            raise Exception(f"Repository with id {id} not found")

        db.delete(repo)
        db.commit()

        return True