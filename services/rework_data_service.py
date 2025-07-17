from fastapi import HTTPException, status
from repositories.rework_repository import ReworkDataRepository
from models.rework import ReworkDataDB
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from schemas.rework_rate.rework_rate_types import ReworkRateFilters, ReworkDataInput
from schemas.repository.repository_input import RepositoryCreateInput
from models.repository import RepositoryEntity
from services.repository_service import RepositoryService
from repositories.repository_repository import RepositoryRepository

class ReworkDataService:
    def __init__(self, session: Session, repo: ReworkDataRepository):
        self.session = session
        self.repo = repo

    def get_rework_records(self, filters: ReworkRateFilters = None) -> List[ReworkDataDB]:
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

    def create_rework_data(self, data: ReworkDataInput) -> ReworkDataDB:
        # Antes de crear el registro hay que verificar si el repositorio ya existe
        existing_record = self.repo.get_rework_repository_by_url(self.session, data.repo_url)

        if existing_record:
            # Si el repositorio ya existe, se añade un registro de rework
            # Se crea un ReworkDataDB a partir de los datos proporcionados
            # ReworkDataDB(**data_dict)
            record = self.repo.create_rework_data_record(self.session, ReworkDataDB(**data.__dict__))
            return record
        else:
            # Si el respository no existe, se crea uno nuevo
            repo = RepositoryRepository(RepositoryEntity, self.session)
            service = RepositoryService(self.session, repo)
            new_repo_data = RepositoryCreateInput(
                name=data.repo_url,
                description=None,
                repo_url=data.repo_url
            )
            service.create_repository(new_repo_data)
            # Ahora se crea el registro de rework asociado al nuevo repositorio
            record = self.repo.create_rework_data_record(self.session, ReworkDataDB(**data.__dict__))
            return record
            


    def delete_rework_data_by_repo_url(self, repo_url: str) -> None:
        exists = self.session.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url).first()
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found for repo_url")
        self.session.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url).delete()
        self.session.commit()
