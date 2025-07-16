from repositories.base_repository import Repository
from models.rework import ReworkDataDB
from sqlalchemy.orm import Session

class RepositoryRepository(Repository[ReworkDataDB]):

    def get_rework_records(self, db: Session, filters: dict = None) -> list[ReworkDataDB]:

        pass

    def get_rework_records_by_repository(self, db, repository, start_date=None, end_date=None):
        """
        Si el repository contiene un name, busca por name.
        Si el repository contiene un id, busca por id.

        Si se proporciona un rango de fechas, filtra los registros por ese rango.
        """
        pass