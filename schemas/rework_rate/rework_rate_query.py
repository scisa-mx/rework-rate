import strawberry
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from strawberry.types import Info
from schemas.rework_rate.rework_rate_types import ReworkDataType, MeanAndMedianType
from services.rework_data_service import ReworkDataService
from repositories.rework_repository import ReworkDataRepository
from models.rework import ReworkDataDB



@strawberry.type
class Query:
    
    @strawberry.field
    def get_rework_history(
        self,
        info: Info,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[ReworkDataType]:
        db: Session = info.context["db"]
        service = ReworkDataService(db, ReworkDataRepository(ReworkDataDB, db))
        filters = {"repo_url": repo_url, "start_date": start_date, "end_date": end_date}
        records = service.get_rework_records(filters)
        return records


    @strawberry.field
    def get_mean_and_median(
        self,
        info: Info,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> MeanAndMedianType:
        db: Session = info.context["db"]
        service = ReworkDataService(db, ReworkDataRepository(ReworkDataDB, db))
        records = service.get_rework_records({"repo_url": repo_url, "start_date": start_date, "end_date": end_date})

        if not records:
            return MeanAndMedianType(mean=0.0, median=0.0)

        rework_percentages = [r.rework_percentage for r in records]
        mean = sum(rework_percentages) / len(rework_percentages)

        sorted_perc = sorted(rework_percentages)
        n = len(sorted_perc)
        median = (sorted_perc[n//2 - 1] + sorted_perc[n//2]) / 2 if n % 2 == 0 else sorted_perc[n//2]

        return MeanAndMedianType(mean=mean, median=median)
