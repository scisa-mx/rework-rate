from repositories.base_repository import Repository
from models.rework import ReworkDataDB
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional
from datetime import datetime

class ReworkDataRepository(Repository[ReworkDataDB]):

    def get_rework_records(self, db: Session, filters: Optional[dict] = None) -> list[ReworkDataDB]:
        query = select(self.model)
        conditions = []

        if filters:
            if "repo_url" in filters and filters["repo_url"]:
                conditions.append(self.model.repo_url == filters["repo_url"])
            if "start_date" in filters and filters["start_date"]:
                conditions.append(self.model.createdAtDate >= filters["start_date"])
            if "end_date" in filters and filters["end_date"]:
                conditions.append(self.model.createdAtDate <= filters["end_date"])

        if conditions:
            query = query.where(and_(*conditions))

        result = db.execute(query)
        return result.scalars().all()

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
