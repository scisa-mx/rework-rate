from sqlalchemy.orm import Session, joinedload
import strawberry
from models.rework import ReworkDataDB, rework_data_tags
from models.tags import TagDB
from schemas.rework_rate.rework_rate_types import (
    ReworkDataType,
    RepoUrlType,
    MeanAndMedianType,
)
from resolvers.rework import convert_to_type
from core.utils.formatter import extract_repo_name
from typing import Optional
from datetime import datetime
from sqlalchemy import and_, func


@strawberry.type
class Query:
    @strawberry.field
    def get_rework_data(self, info) -> list[ReworkDataType]:
        db: Session = info.context["db"]
        records = db.query(ReworkDataDB).all()
        return [convert_to_type(record) for record in records]

    @strawberry.field
    def get_rework_data_by_name(
        self, info, repo_url: Optional[str] = None, tags: Optional[list[str]] = None
    ) -> list[RepoUrlType]:
        db: Session = info.context["db"]

        query = db.query(ReworkDataDB)

        # Si no hay filtros, retorna todo
        if (not repo_url and not tags) or (
            repo_url == "" and (not tags or len(tags) == 0)
        ):
            records = query.options(joinedload(ReworkDataDB.tags)).all()
            return [convert_to_type(record) for record in records]

        if repo_url:
            query = query.filter(
                func.right(
                    ReworkDataDB.repo_url,
                    func.charindex("/", func.reverse(ReworkDataDB.repo_url)) - 1,
                ) == repo_url
            )

        if tags and len(tags) > 0 and tags[0] != "":
            subq = (
                db.query(rework_data_tags)
                .join(TagDB)
                .filter(
                    rework_data_tags.c.rework_data_id == ReworkDataDB.id,
                    TagDB.name.in_(tags),
                )
                .exists()
            )
            query = query.filter(subq)
            query = query.options(joinedload(ReworkDataDB.tags))
        
        
        records = query.all()

        print(records)
        return [
            RepoUrlType(
                id=record.id,
                url=record.repo_url,
                name=extract_repo_name(record.repo_url),
            )
            for record in records
        ]

    @strawberry.field
    def get_rework_data_by_pr(self, info, pr_number: str) -> ReworkDataType:
        db: Session = info.context["db"]
        record = (
            db.query(ReworkDataDB).filter(ReworkDataDB.pr_number == pr_number).first()
        )
        return convert_to_type(record) if record else None

    @strawberry.field
    def get_all_repos(self, info) -> list[RepoUrlType]:
        db: Session = info.context["db"]
        repos = db.query(ReworkDataDB).all()
        return [
            RepoUrlType(
                id=repo.id,
                url=repo.repo_url,
                name=extract_repo_name(repo.repo_url),
            )
            for repo in repos
        ]

    @strawberry.field
    def get_rework_history(
        self,
        info,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[ReworkDataType]:
        db: Session = info.context["db"]

        query = db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url)

        if start_date:
            start_date = start_date.replace(tzinfo=None)
        if end_date:
            end_date = end_date.replace(tzinfo=None)

        if start_date and end_date:
            query = query.filter(
                and_(
                    ReworkDataDB.createdAtDate >= start_date,
                    ReworkDataDB.createdAtDate <= end_date,
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
                    ReworkDataDB.period_start <= end_date,
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
