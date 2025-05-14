from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import and_ # type: ignore
from models.rework import ReworkDataDB
from typing import Optional
from datetime import datetime

class ReworkRepository:
    """
    Repositorio para manejar operaciones CRUD en la tabla de datos de rework.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(ReworkDataDB).all()

    def get_by_pr_number(self, pr_number: str):
        return self.db.query(ReworkDataDB).filter(ReworkDataDB.pr_number == pr_number).first()

    def get_all_repo_urls(self):
        return self.db.query(ReworkDataDB.repo_url).distinct().all()

    def get_by_repo_and_dates(
        self,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        query = self.db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url)

        # Normalizamos fechas sin timezone
        if start_date:
            start_date = start_date.replace(tzinfo=None)
        if end_date:
            end_date = end_date.replace(tzinfo=None)

        if start_date and end_date:
            query = query.filter(
                and_(
                    ReworkDataDB.createdAtDate >= start_date,
                    ReworkDataDB.createdAtDate <= end_date
                )
            )
        return query.order_by(ReworkDataDB.period_start.asc()).all()

    def get_by_period_range(
        self,
        repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        query = self.db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url)

        if start_date and end_date:
            query = query.filter(
                and_(
                    ReworkDataDB.period_start >= start_date,
                    ReworkDataDB.period_start <= end_date
                )
            )

        return query.all()

    def create(self, data_dict: dict):
        new_record = ReworkDataDB(**data_dict)
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        return new_record

    def exists_by_repo_url(self, url: str):
        return self.db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == url).first()

    def delete_by_repo_url(self, url: str):
        self.db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == url).delete()
        self.db.commit()
