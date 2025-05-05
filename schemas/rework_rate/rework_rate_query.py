from sqlalchemy.orm import Session
import strawberry
from models.rework import ReworkDataDB
from schemas.rework_rate.rework_rate_types import ReworkDataType, RepoUrlType, MeanAndMedianType
from resolvers.rework import convert_to_type
from core.utils.formatter import extract_repo_name
from typing import Optional
from datetime import datetime
from sqlalchemy import and_

@strawberry.type
class Query:
    @strawberry.field
    def get_rework_data(self, info) -> list[ReworkDataType]:
        db: Session = info.context["db"]
        records = db.query(ReworkDataDB).all()
        return [convert_to_type(record) for record in records]

    @strawberry.field
    def get_rework_data_by_pr(self, info, pr_number: str) -> ReworkDataType:
        db: Session = info.context["db"]
        record = db.query(ReworkDataDB).filter(ReworkDataDB.pr_number == pr_number).first()
        return convert_to_type(record) if record else None

    @strawberry.field
    def get_all_repos(self, info) -> list[RepoUrlType]:
        db: Session = info.context["db"]
        distinct_urls = db.query(ReworkDataDB.repo_url).distinct().all()
        return [
            RepoUrlType(url=url[0], name=extract_repo_name(url[0]))
            for url in distinct_urls
        ]
    @strawberry.field
    def get_rework_history(
        self,
        info,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[ReworkDataType]:
        db: Session = info.context["db"]
        
        query = db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url)

        if start_date and end_date:
            query = query.filter(
                and_(
                    ReworkDataDB.period_start >= start_date,
                    ReworkDataDB.period_start <= end_date
                )
            )
        query = query.order_by(ReworkDataDB.period_start.asc())
        records = query.all()
        return [convert_to_type(record) for record in records]
    
    @strawberry.field
    def get_mean_and_median(
        self, 
        info,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> MeanAndMedianType:
        db: Session = info.context["db"]

        query = db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url)
        
        # Apply date filters if provided
        if start_date and end_date:
            query = query.filter(
                and_(
                    ReworkDataDB.period_start >= start_date,
                    ReworkDataDB.period_start <= end_date
                )
            )
        # Get all records for the specified repo_url and date range
        records = query.all()
        if not records:
            return MeanAndMedianType(mean=0.0, median=0.0)
        
        # Calculate mean and median of rework percentages
        rework_percentages = [record.rework_percentage for record in records]
        mean = sum(rework_percentages) / len(rework_percentages)
        
        sorted_percentages = sorted(rework_percentages)
        n = len(sorted_percentages)
        if n % 2 == 0:
            median = (sorted_percentages[n // 2 - 1] + sorted_percentages[n // 2]) / 2
        else:
            median = sorted_percentages[n // 2]
        
        return MeanAndMedianType(mean=mean, median=median) 