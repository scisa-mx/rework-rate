from abc import ABC
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class Repository(Generic[ModelT], ABC):
    """
    Interfaz genérica de repositorio.
    Esta clase define los métodos básicos para interactuar con la base de datos
    utilizando SQLAlchemy y AsyncSession.
    """

    def __init__(self, model: ModelT, session: Session) -> None:
        self.model = model
        self.session = session

