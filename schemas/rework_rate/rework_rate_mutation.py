from fastapi import HTTPException
from sqlalchemy.orm import Session
import strawberry
from schemas.rework_rate.rework_rate_types import ReworkDataType, ReworkDataInput
from resolvers.rework import convert_to_type
from services.rework_rate_service import ReworkService
from repositories.rework_rate_repository import ReworkRepository

# Importar la función setup_logger para obtener un logger específico
from core.logger.logger_main import setup_logger

# Crear un logger específico para este archivo (mutaciones de rework_rate)
logger = setup_logger("rework_rate_mutations")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_rework_data(self, info, data: ReworkDataInput) -> ReworkDataType:
        db: Session = info.context["db"]
        service = ReworkService(ReworkRepository(db))
        new_record = service.create_record(data.__dict__)
        logger.info(f"Registro creado: {data.__dict__}")
        return convert_to_type(new_record)

    @strawberry.mutation
    def delete_repo_with_url(self, info, url: str) -> None:
        db: Session = info.context["db"]
        service = ReworkService(ReworkRepository(db))

        if not service.delete_repo(url):
            logger.warning(f"No se encontraron registros para la URL del repositorio: {url}")
            raise HTTPException(status_code=404, detail="No se encontraron registros")
        
        logger.info(f"Registros eliminados para la URL del repositorio: {url}")
        return None