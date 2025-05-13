from models.rework import ReworkDataDB
from sqlalchemy.orm import Session
from sqlalchemy import and_

class ReworkRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(ReworkDataDB).all()

    def get_by_pr_number(self, pr_number: str):
        return self.db.query(ReworkDataDB).filter(ReworkDataDB.pr_number == pr_number).first()

    def get_by_repo_and_period(self, repo_url: str, start_date, end_date):
        query = self.db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url)

        if start_date:
            start_date = start_date.replace(tzinfo=None)
        if end_date:
            end_date = end_date.replace(tzinfo=None)

        if start_date and end_date:
            query = query.filter(
                and_(
                    ReworkDataDB.period_start >= start_date,
                    ReworkDataDB.period_start <= end_date
                )
            )
        return query.order_by(ReworkDataDB.period_start.asc()).all()
