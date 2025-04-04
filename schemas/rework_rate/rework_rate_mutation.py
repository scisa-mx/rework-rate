from sqlalchemy.orm import Session
import strawberry
from models.rework import ReworkDataDB
from schemas.rework_rate.rework_rate_types import ReworkDataType, ReworkDataInput
from resolvers.rework import convert_to_type

import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        logger.info(f"Registro creado: {new_record}")
        return convert_to_type(new_record)
