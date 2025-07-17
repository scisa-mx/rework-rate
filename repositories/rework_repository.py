from repositories.base_repository import Repository
from models.rework import ReworkDataDB
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional
from datetime import datetime
from schemas.rework_rate.rework_rate_types import ReworkRateFilters

class ReworkDataRepository(Repository[ReworkDataDB]):

    def get_rework_records(self, db: Session, filters: ReworkRateFilters
 = None) -> list[ReworkDataDB]:
        query = select(self.model)
        conditions = []

        if filters:
            if filters.repo_url:
                conditions.append(self.model.repo_url == filters.repo_url)
            if filters.start_date:
                conditions.append(self.model.createdAtDate >= filters.start_date)
            if filters.end_date:
                conditions.append(self.model.createdAtDate <= filters.end_date)

        if conditions:
            query = query.where(and_(*conditions))

        result = db.execute(query)
        return result.scalars().all()
    
    def get_rework_repository_by_url(
        self, db: Session, repo_url: str
    ) -> Optional[ReworkDataDB]:
        query = select(self.model).where(self.model.repo_url == repo_url)
        result = db.execute(query)
        return result.scalar_one_or_none()

    def get_rework_records_by_repository(
        self,
        db: Session,
        repository: dict,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[ReworkDataDB]:
        query = select(self.model)

        conditions = []
        if "name" in repository and repository["name"]:
            conditions.append(self.model.repo_url == repository["name"])
        elif "id" in repository and repository["id"]:
            conditions.append(self.model.repo_url == repository["id"])

        if start_date:
            conditions.append(self.model.createdAtDate >= start_date)
        if end_date:
            conditions.append(self.model.createdAtDate <= end_date)

        if conditions:
            query = query.where(and_(*conditions))

        result = db.execute(query)
        return result.scalars().all()

    
    def create_rework_data_record(self, db: Session, data: ReworkDataDB) -> ReworkDataDB:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data