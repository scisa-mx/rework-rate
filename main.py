import strawberry
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
from database import get_db, engine, Base

from schemas.rework_rate.rework_rate_query import Query
from schemas.rework_rate.rework_rate_mutation import Mutation
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inyectar contexto con sesión de DB
async def get_context(db: Session = Depends(get_db)):
    return {"db": db}

# Crear el esquema GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI(title="Rework Rate API con GraphQL")

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
