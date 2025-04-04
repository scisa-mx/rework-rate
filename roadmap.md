---
title: "Roadmap api rework"
author: "Chachacharlie"
---

## Esta es la estrucura esperada del proyecto

```markdown
.
├── .github/                   # Configuración de GitHub Actions (CI/CD)
│   └── workflows/
│       └── main.yml
├── app/                       # Código principal de la aplicación
│   ├── api/                   # Endpoints y routers
│   │   ├── v1/               # Versión 1 de la API
│   │   │   ├── endpoints/
│   │   │   │   ├── rework.py
│   │   │   │   └── ...       # Otros endpoints
│   │   │   └── __init__.py
│   │   └── dependencies.py    # Dependencias compartidas
│   ├── core/                  # Configuraciones centrales
│   │   ├── config.py          # Configuración de la aplicación
│   │   ├── security.py        # Autenticación y seguridad
│   │   └── logging.py         # Configuración de logs
│   ├── db/                    # Base de datos
│   │   ├── models/            # Modelos de DB
│   │   │   └── rework.py
│   │   ├── repositories/      # Patrón repositorio
│   │   │   └── rework_repo.py
│   │   └── session.py         # Sesión de DB y conexión
│   ├── schemas/               # Esquemas Pydantic
│   │   └── rework.py
│   ├── services/              # Lógica de negocio
│   │   └── rework_service.py
│   ├── utils/                 # Utilidades comunes
│   │   ├── error_handlers.py  # Manejo de errores
│   │   ├── middleware.py      # Middleware personalizado
│   │   └── helpers.py         # Funciones auxiliares
│   ├── static/                # Archivos estáticos
│   │   └── swagger/           # Custom Swagger docs
│   ├── tests/                 # Pruebas
│   │   ├── unit/              # Pruebas unitarias
│   │   ├── integration/       # Pruebas de integración
│   │   └── conftest.py        # Configuración de pytest
│   ├── logs/                  # Logs de aplicación
│   │   └── api.log            # (Ignorar en git)
│   └── main.py                # Punto de entrada
├── docs/                      # Documentación
│   ├── OPENAPI.yml            # Especificación OpenAPI
│   └── USER_GUIDE.md          # Manual de usuario
├── migrations/                # Migraciones de DB (Alembic)
│   └── versions/
├── scripts/                   # Scripts útiles
│   ├── db_setup.sh            # Configuración inicial de DB
│   └── deploy.sh              # Script de despliegue
├── .env                       # Variables de entorno locales
├── .env.example               # Plantilla de variables
├── .gitignore
├── requirements/              # Dependencias separadas
│   ├── base.txt               # Dependencias principales
│   ├── dev.txt                # Desarrollo y testing
│   └── prod.txt               # Producción
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml             # Configuración de proyecto
└── README.md
```

## Cosas por agregar
### Manejo Centralizado de Errores
¿Por qué agregarlo?
Para proporcionar respuestas consistentes en errores (ej: 404 Not Found, 500 Internal Server Error) y facilitar el debugging.

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

app.add_exception_handler(HTTPException, http_exception_handler)
```
### Logging Estructurado
¿Por qué agregarlo?
Para rastrear solicitudes, errores y rendimiento en producción. Usa logging con formato JSON para integración con herramientas como ELK o Datadog.

```python
import logging
from logging.config import dictConfig

dictConfig({
    "version": 1,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json"
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]}
})
```

### Pruebas Automatizadas
¿Por qué agregarlo?
Para asegurar la calidad del código y prevenir regresiones.
Hay que comprobar el desarrollo basado en pruebas TDD.

Pruebas Unitarias (con pytest)
```python
# tests/test_rework.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_rework_data():
    response = client.post("/rework", json={
        "repo_url": "https://github.com/example/repo",
        "rework_percentage": 10.0
    })
    assert response.status_code == 200
    assert "id" in response.json()
```

### Health Checks
¿Por qué agregarlo?
Para que sistemas externos (ej: Kubernetes) verifiquen el estado del servicio.

```python
@app.get("/health")
def health_check():
    return {"status": "OK", "timestamp": datetime.utcnow()}
```

