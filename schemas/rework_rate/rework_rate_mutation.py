from fastapi import HTTPException
from sqlalchemy.orm import Session
import strawberry
from models.rework import ReworkDataDB
from schemas.rework_rate.rework_rate_types import ReworkDataType, ReworkDataInput
from resolvers.rework import convert_to_type

# Importar la función setup_logger para obtener un logger específico
from core.logger.logger_main import setup_logger

# Crear un logger específico para este archivo (mutaciones de rework_rate)
logger = setup_logger("rework_rate_mutations")

# Definir las mutaciones
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_rework_data(self, info, data: ReworkDataInput) -> ReworkDataType:
        db: Session = info.context["db"]
        new_record = ReworkDataDB(**data.__dict__)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        data_dict = {k: v for k, v in new_record.__dict__.items() if not k.startswith('_')}
        logger.info(f"Registro creado: {data_dict}")
        
        return convert_to_type(new_record)

    @strawberry.mutation
    def delete_repo_with_url(self, info, url: str) -> None:
        db: Session = info.context["db"]

        # Verificar si existen registros primero
        exists = db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == url).first()
        if not exists:
            # Usar el logger para registrar el evento
            logger.warning(f"No se encontraron registros para la URL del repositorio: {url}")
            raise HTTPException(status_code=404, detail=f"No se encontraron registros para la URL del repositorio: {url}")

        # Eliminar los registros
        db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == url).delete()
        db.commit()

        logger.info(f"Registros eliminados para la URL del repositorio: {url}")
        return None