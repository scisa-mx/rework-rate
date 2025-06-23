from fastapi import HTTPException
from sqlalchemy.orm import Session
import strawberry
from models.tags import TagDB
from schemas.tags.tags_types import TagType, TagInput
from models.rework import ReworkDataDB
from core.logger.logger_main import setup_logger

logger = setup_logger("tags_mutations")


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_tag(self, info, data: TagInput) -> TagType:
        db: Session = info.context["db"]
        print(data)
        # Buscar el repositorio por id
        repo = db.query(ReworkDataDB).filter(ReworkDataDB.id == data.rework_data_id).first()
        if not repo:
            raise HTTPException(status_code=404, detail="Repositorio no encontrado")

        # Buscar si ya existe un tag con ese nombre
        existing_tag = db.query(TagDB).filter(TagDB.name == data.name).first()
        if existing_tag:
            # Si el tag ya está asociado, no volver a agregarlo
            if existing_tag not in repo.tags:
                repo.tags.append(existing_tag)
                db.commit()
            return TagType(id=existing_tag.id, name=existing_tag.name)

        # Crear el tag
        new_tag = TagDB(name=data.name)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)

        # Asociar el tag al repositorio
        repo.tags.append(new_tag)
        db.commit()

        logger.info(f"Etiqueta creada: {new_tag.name} y asignada al repositorio {repo.id}")

        return TagType(id=str(new_tag.id), name=new_tag.name)
