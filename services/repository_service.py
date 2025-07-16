from fastapi import HTTPException, status


from repositories.repository_repository import RepositoryRepository
from models.repository import RepositoryEntity
from sqlalchemy.orm import Session

from schemas.repository.repository_input import RepositoryFilterInput

class RepositoryService:
    """
    Clase de servicio para manejar operaciones de repositorio.
    Proporciona métodos para obtener un repositorio específico basado en el modelo.
    """

    def __init__(self, session: Session, repo: RepositoryRepository) -> None:
        self.session = session
        self.repository = repo

    def get_repositories(self, filters: RepositoryFilterInput) -> list[RepositoryEntity]:
        """
        Obtiene todos los repositorios de la base de datos.
        """        
        return self.repository.get_repositories(db=self.session, filters=filters)

    def get_repository_by_id(self, id: str):
        """
        Obtiene un repositorio por su ID.
        """

        repository = self.repository.get_repository_by_id(self.session, id)

        if not repository:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository with ID {id} not found."
            )

        return repository

    def update_repository(self, repository: RepositoryEntity) -> RepositoryEntity:
        """
        Actualiza un repositorio existente en la base de datos.
        """
        return self.repository.update_repository(self.session, repository)

    def delete_repository(self, id: str) -> None:
        """
        Elimina un repositorio de la base de datos por su ID.
        """
        self.repository.delete_repository(self.session, id)

    def create_repository(self, repository: RepositoryEntity, data) -> RepositoryEntity:
        """
        Crea un nuevo repositorio en la base de datos.
        """

        # Buscar con la url del record si existe un repositorio con esa URL, si no existe, lo crea, si existe, no hace nada

        self.session.add(repository)
        self.session.commit()
        self.session.refresh(repository)
        return repository