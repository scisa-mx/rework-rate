from fastapi import HTTPException
from sqlalchemy.orm import Session
import strawberry
from models.rework import ReworkDataDB
from models.tags import TagDB
from schemas.rework_rate.rework_rate_types import ReworkDataType, ReworkDataInput
from schemas.tags.tags_types import TagType
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
    
    @strawberry.mutation
    def remove_tag_from_repo(self, info, repo_url: str, tag_name: str) -> None:
        db: Session = info.context["db"]

        # Verificar si el tag existe
        tag = db.query(TagDB).filter(TagDB.name == tag_name).first()
        if not tag:
            logger.warning(f"Tag '{tag_name}' no encontrado.")
            raise HTTPException(status_code=404, detail=f"Tag '{tag_name}' no encontrado.")

        # Verificar si existen registros con la URL del repositorio
        exists = db.query(ReworkDataDB).filter(ReworkDataDB.repo_url == repo_url).first()
        if not exists:
            logger.warning(f"No se encontraron registros para la URL del repositorio: {repo_url}")
            raise HTTPException(status_code=404, detail=f"No se encontraron registros para la URL del repositorio: {repo_url}")

        # Eliminar el tag del registro
        # db.query(rework_data_tags).filter(
        #     rework_data_tags.c.rework_data_id == exists.id,
        #     rework_data_tags.c.tag_id == tag.id
        # ).delete()
        # db.commit()

        logger.info(f"Tag '{tag_name}' eliminado de la URL del repositorio: {repo_url}")
        return None