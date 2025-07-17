from fastapi import HTTPException, status


from repositories.repository_repository import RepositoryRepository
from models.repository import RepositoryEntity
from schemas.repository.repository_input import RepositoryCreateInput
from sqlalchemy.orm import Session
from schemas.repository.repository_input import RepositoryUpdateInput

from schemas.repository.repository_input import RepositoryFilterInput, AssingTagsInput
from schemas.repository.repository_type import RepositoryType
from services.tag_service import TagService

class RepositoryService:
    """
    Clase de servicio para manejar operaciones de repositorio.
    Proporciona métodos para obtener un repositorio específico basado en el modelo.
    """

    def __init__(self, session: Session, repo: RepositoryRepository) -> None:
        self.session = session
        self.repository = repo

    def get_repositories(self, filters: RepositoryFilterInput) -> list[RepositoryType]:
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

    def update_repository(self, repository: RepositoryUpdateInput) -> RepositoryEntity:
        """
        Actualiza un repositorio existente en la base de datos.
        """
        existing_repository = self.repository.get_repository_by_id(self.session, repository.id)

        if not existing_repository:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository with ID {repository.id} not found."
            )
        

        # actializar los campos del repositorio existente
        for field, value in repository.__dict__.items():
            if value is not None and field != "id":
                setattr(existing_repository, field, value)

        # Crear un nuevo objeto limpio con los datos ya actualizados
        updated_repository = RepositoryEntity(
            id=existing_repository.id,
            name=existing_repository.name,
            repo_url=existing_repository.repo_url,
            description=existing_repository.description
        )
        return self.repository.update_repository(self.session, updated_repository)

    def delete_repository(self, id: str) -> None:
        """
        Elimina un repositorio de la base de datos por su ID.
        """
        self.repository.delete_repository(self.session, id)

    def create_repository(self, repository: RepositoryCreateInput) -> RepositoryEntity:
        """
        Crea un nuevo repositorio en la base de datos.
        """

        new_repository = RepositoryEntity(
            name=repository.name,
            repo_url=repository.repo_url,
            description=repository.description
        )        

        self.session.add(new_repository)
        self.session.commit()
        self.session.refresh(new_repository)
        return new_repository
    
    def assing_tags_to_repository(self, data: AssingTagsInput) -> RepositoryEntity:
        """
        Asigna etiquetas a un repositorio.
        """
        repo = self.repository.get_repository_by_id(self.session, data.repository_id)
        if not repo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repository with ID {data.repository_id} not found."
            )
        
        service = TagService(self.session)
        
        final_tags = []
        
        for name in data.tag_names:
            # Buscar el tag por nombre
            tag = service.match_tag_name(name)
            if not tag:
                # Si no existe, crear uno nuevo
                tag = service.create_tag(name)
            # Agregar el tag a la lista final
            if tag not in final_tags:
                final_tags.append(tag)

        # Asignar los tags al repositorio
        repo.tags = final_tags
        repository = self.repository.update_repository(self.session, repo)

        return repository