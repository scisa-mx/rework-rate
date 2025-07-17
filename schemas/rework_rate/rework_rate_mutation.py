import strawberry
from sqlalchemy.orm import Session
from fastapi import HTTPException
from strawberry.types import Info
from models.rework import ReworkDataDB
from schemas.rework_rate.rework_rate_types import ReworkDataType, ReworkDataInput
from services.rework_data_service import ReworkDataService
from repositories.rework_repository import ReworkDataRepository
from resolvers.rework import convert_to_type

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_rework_data(self, info, data: ReworkDataInput) -> ReworkDataType:
        db: Session = info.context["db"]
        service = ReworkDataService(db, ReworkDataRepository(ReworkDataDB, db))
        new_record = service.create_rework_data(data)

        return convert_to_type(new_record)

    @strawberry.mutation
    def delete_rework_data_by_repo_url(self, info: Info, repo_url: str) -> bool:
        db: Session = info.context["db"]
        service = ReworkDataService(db, ReworkDataRepository(ReworkDataDB, db))
        service.delete_rework_data_by_repo_url(repo_url)
        return True
