from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from models import ReworkData
from datetime import datetime
import json
import os

app = FastAPI(title="Rework Rate API")

@app.get("/", response_class=RedirectResponse, status_code=308)
async def root():
    return "/v1/repo-rework-rates"

# Lista para almacenar los datos (en un entorno de producción, usarías una base de datos)
rework_records = []

@app.post("/v1/repo-rework-rates")
async def create_rework_data(data: ReworkData):
    try:
        # Agregar timestamp si no se proporciona
        if not data.timestamp:
            data.timestamp = datetime.now()
        
        # Convertir el modelo a diccionario
        record = data.dict()
        
        # Agregar a la lista de registros
        rework_records.append(record)
        
        # Guardar en un archivo JSON (solución temporal)
        with open("rework_data.json", "w") as f:
            json.dump(rework_records, f, default=str)
        
        return {"message": "Datos guardados exitosamente", "data": record}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/repo-rework-rates")
async def get_rework_data():
    return rework_records

@app.get("/v1/repo-rework-rates/{pr_number}")
async def get_rework_data_by_pr(pr_number: str):
    for record in rework_records:
        if record["pr_number"] == pr_number:
            return record
    raise HTTPException(status_code=404, detail="PR no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 