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
    def update_tags(self, info, data: TagInput) -> list[TagType]:
        db: Session = info.context["db"]

        repo = (
            db.query(ReworkDataDB)
            .filter(ReworkDataDB.id == data.rework_data_id)
            .first()
        )
        if not repo:
            raise HTTPException(status_code=404, detail="Repositorio no encontrado")

        # 1. Crear o asociar los nuevos tags
        final_tags = []
        for tag_name in data.names:
            tag = db.query(TagDB).filter(TagDB.name == tag_name).first()

            if not tag:
                tag = TagDB(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
                logger.info(f"Nuevo tag '{tag.name}' creado")

            if tag not in repo.tags:
                repo.tags.append(tag)
                logger.info(f"Tag '{tag.name}' asociado al repo {repo.id}")

            final_tags.append(tag)

        # 2. Eliminar tags que ya no están en `data.names`
        tags_to_remove = [tag for tag in repo.tags if tag.name not in data.names]
        for tag in tags_to_remove:
            repo.tags.remove(tag)
            logger.info(f"Tag '{tag.name}' eliminado del repo {repo.id}")

        db.commit()

        return [TagType(id=tag.id, name=tag.name) for tag in repo.tags]
