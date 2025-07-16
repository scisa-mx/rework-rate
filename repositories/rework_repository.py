from repositories.base_repository import Repository
from models.rework import ReworkDataDB
from sqlalchemy.orm import Session

class RepositoryRepository(Repository[ReworkDataDB]):

    def get_rework_records(self, db: Session, filters: dict = None) -> list[ReworkDataDB]:

        pass
