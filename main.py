from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import ReworkData, ReworkDataDB
from database import get_db, engine, Base
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rework Rate API")

@app.get("/", response_class=RedirectResponse, status_code=308)
async def root():
    return "/v1/repo-rework-rates"

@app.post("/v1/repo-rework-rates")
async def create_rework_data(data: ReworkData, db: Session = Depends(get_db)):
    try:
        logger.info(f"Datos recibidos: {data}")
        db_rework = ReworkDataDB(**data.dict())
        db.add(db_rework)
        db.commit()
        db.refresh(db_rework)
        return {"message": "Datos guardados exitosamente", "data": data}
    except Exception as e:
        logger.error(f"Error al procesar datos: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/repo-rework-rates")
async def get_rework_data(db: Session = Depends(get_db)):
    return db.query(ReworkDataDB).all()

@app.get("/v1/repo-rework-rates/{pr_number}")
async def get_rework_data_by_pr(pr_number: str, db: Session = Depends(get_db)):
    record = db.query(ReworkDataDB).filter(ReworkDataDB.pr_number == pr_number).first()
    if record is None:
        raise HTTPException(status_code=404, detail="PR no encontrado")
    return record

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 