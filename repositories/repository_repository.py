from models.repository import RepositoryEntity
from repositories.base_repository import Repository
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import Session
from schemas.repository.repository_input import RepositoryFilterInput


class RepositoryRepository(Repository[RepositoryEntity]):

    def get_repositories(self, db: Session, filters: RepositoryFilterInput) -> list[RepositoryEntity]:
        conditions = []

        if filters.name:
            conditions.append(self.model.name.ilike(f"%{filters.name}%"))

        if filters.description:
            conditions.append(self.model.description.ilike(f"%{filters.description}%"))

        query = select(self.model)
        if conditions:
            query = query.where(and_(*conditions))

        result = db.execute(query)
        return result.scalars().all()

    def update_repository(
        self, db: Session, repository: RepositoryEntity
    ) -> RepositoryEntity:
        """
        Actualiza un repositorio existente en la base de datos.
        """
        
        merged = db.merge(repository)
        db.commit()
        db.refresh(merged)
        return merged
    
    def get_repository_by_id(
        self, db: Session, repository_id: str
    ) -> RepositoryEntity:
        """
        Obtiene un repositorio por su ID.
        """
        query = select(self.model).where(self.model.id == repository_id)
        result = db.execute(query)
        return result.scalar_one_or_none()
    
    def delete_repository(self, db: Session, repository_id: str) -> None:
        """
        Elimina un repositorio de la base de datos por su ID.
        """
        query = delete(self.model).where(self.model.id == repository_id)
        db.execute(query)
        db.commit()