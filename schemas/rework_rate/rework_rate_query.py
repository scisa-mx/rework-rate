from sqlalchemy.orm import Session
import strawberry
from services.rework_rate_service import ReworkService
from repositories.rework_rate_repository import ReworkRepository
from schemas.rework_rate.rework_rate_types import ReworkDataType, RepoUrlType, MeanAndMedianType, ReworkDataInput
from core.logger.logger_main import setup_logger
from typing import Optional
from datetime import datetime

logger = setup_logger("rework_rate_mutations")

@strawberry.type
class Query:
    @strawberry.field
    def get_rework_data(self, info) -> list[ReworkDataType]:
        db: Session = info.context["db"]
        service = ReworkService(ReworkRepository(db))
        return service.get_all_data()

    @strawberry.field
    def get_rework_data_by_pr(self, info, pr_number: str) -> Optional[ReworkDataType]:
        db: Session = info.context["db"]
        service = ReworkService(ReworkRepository(db))
        return service.get_by_pr(pr_number)

    @strawberry.field
    def get_all_repos(self, info) -> list[RepoUrlType]:
        db: Session = info.context["db"]
        service = ReworkService(ReworkRepository(db))
        return service.get_all_repos()

    @strawberry.field
    def get_rework_history(
        self,
        info,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[ReworkDataType]:
        db: Session = info.context["db"]
        service = ReworkService(ReworkRepository(db))
        return service.get_rework_history(repo_url, start_date, end_date)

    @strawberry.field
    def get_mean_and_median(
        self,
        info,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> MeanAndMedianType:
        db: Session = info.context["db"]
        service = ReworkService(ReworkRepository(db))
        return service.get_mean_and_median(repo_url, start_date, end_date)
