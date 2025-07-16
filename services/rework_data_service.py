from fastapi import HTTPException, status
from repositories.rework_repository import ReworkDataRepository
from models.rework import ReworkDataDB
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

class ReworkDataService:
    def __init__(self, session: Session, repo: ReworkDataRepository):
        self.session = session
        self.repo = repo

    def get_rework_records(self, filters: Optional[dict] = None) -> List[ReworkDataDB]:
        return self.repo.get_rework_records(self.session, filters)

    def get_rework_records_by_repository(
        self,
        repository: dict,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[ReworkDataDB]:
        return self.repo.get_rework_records_by_repository(
            self.session, repository, start_date, end_date
        )

    def create_rework_data(self, data: dict) -> ReworkDataDB:
        new_record = ReworkDataDB(**data)
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        return new_record

    def delete_rework_data_by_repo_url(self, repo_url: str) -> None:
        exists = self.session.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url).first()
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found for repo_url")
        self.session.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url).delete()
        self.session.commit()
