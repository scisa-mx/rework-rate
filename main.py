import strawberry
from typing import List, Optional
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import logging
from models.rework import ReworkDataDB
from models.rework import ReworkDataType, ReworkDataInput
from resolvers.rework import convert_to_type


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir las consultas
@strawberry.type
class Query:
    @strawberry.field
    def get_rework_data(self, info) -> List[ReworkDataType]:
        db: Session = info.context["db"]
        return [convert_to_type(record) for record in db.query(ReworkDataDB).all()]

    @strawberry.field
    def get_rework_data_by_pr(self, info, pr_number: str) -> Optional[ReworkDataType]:
        db: Session = info.context["db"]
        record = db.query(ReworkDataDB).filter(ReworkDataDB.pr_number == pr_number).first()
        return convert_to_type(record) if record else None

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

# Inyectar contexto con sesión de DB
async def get_context(db: Session = Depends(get_db)):
    return {"db": db}

# Crear el esquema GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Inicializar FastAPI y agregar GraphQL
app = FastAPI(title="Rework Rate API con GraphQL")
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
