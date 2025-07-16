from sqlalchemy.orm import Session
from repositories.rework_repository import RepositoryRepository
from models.rework import ReworkDataDB

class RepositoryService:
    """
    Clase de servicio para manejar operaciones de repositorio.
    Proporciona métodos para obtener un repositorio específico basado en el modelo.
    """

    def __init__(self, session: Session, repo: RepositoryRepository) -> None:
        self.session = session
        self.repository = repo


    def get_rework_records(self, filters: dict = None) -> list[ReworkDataDB]:
        """
        Obtiene todos los registros de rework de la base de datos.
        """
        return self.repository.get_rework_records(db=self.session, filters=filters)