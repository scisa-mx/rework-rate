import strawberry
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends

from models.repository import RepositoryEntity
from schemas.repository.repository_type import RepositoryType
from schemas.repository.repository_input import RepositoryCreateInput, RepositoryUpdateInput
import uuid

from repositories.repository_repository import RepositoryRepository
from services.repository_service import RepositoryService


@strawberry.type
class RepositoryMutation:

    @strawberry.mutation
    def create_repository(self, info, input: RepositoryCreateInput) -> RepositoryType:
        db: Session = info.context["db"]

        repo = RepositoryRepository(RepositoryEntity, db)
        service = RepositoryService(db, repo)

        new_repository = service.create_repository(input)

        return new_repository

    @strawberry.mutation
    def update_repository(self, info, input: RepositoryUpdateInput) -> RepositoryType:
        db: Session = info.context["db"]

        repo = RepositoryRepository(RepositoryEntity, db)
        service = RepositoryService(db, repo)


        existing_repository = service.update_repository(input)

        return existing_repository
    

    @strawberry.mutation
    def delete_repository(self, info, id: uuid.UUID) -> bool:
        db: Session = info.context["db"]

        repo = RepositoryRepository(RepositoryEntity, db)
        service = RepositoryService(db, repo)

        service.delete_repository(id)

        return True