import strawberry
from typing import Optional

@strawberry.type
class TagType:
    id: str
    name: str
    color: str

@strawberry.type
class TagResponse:
    tags: list[TagType]

# Input para actualizar tags en lote, ya tienes este para update_tags
@strawberry.input
class TagInput:
    names: list[str]
    rework_data_id: int

# Input para crear un tag individual
@strawberry.input
class TagInputCreate:
    name: str
    color: str = None  

# Input para actualizar un tag individual
@strawberry.input
class TagInputUpdate:
    id: str
    name: str = None
    color: str = None

@strawberry.input
class TagFilter:
    id: Optional[str] = None
    name: Optional[str] = None
