import strawberry
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
from database import get_db, engine, Base

from schemas.rework_rate.rework_rate_query import Query as ReworkQuery
from schemas.rework_rate.rework_rate_mutation import Mutation as ReworkMutation
from schemas.tags.tags_mutation import Mutation as TagsMutation
from schemas.tags.tags_query import Query as TagsQuery
from schemas.repository.repository_mutation import RepositoryMutation
from schemas.repository.repository_query import RepositoryQuery
from fastapi.middleware.cors import CORSMiddleware


@strawberry.type
class RootQuery(ReworkQuery, TagsQuery, RepositoryQuery):
    pass

@strawberry.type
class RootMutation(ReworkMutation, TagsMutation, RepositoryMutation):
    pass

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inyectar contexto con sesión de DB
async def get_context(db: Session = Depends(get_db)):
    return {"db": db}

# Crear el esquema GraphQL
schema = strawberry.Schema(query=RootQuery, mutation=RootMutation)

app = FastAPI(title="Rework Rate API con GraphQL", version="0.1.0")

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://rework-rate.scisa.com.mx"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
