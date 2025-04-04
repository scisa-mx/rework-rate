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
        
        # Usar el logger para registrar el evento
        logger.info(f"Registro creado: {new_record}")
        
        return convert_to_type(new_record)
