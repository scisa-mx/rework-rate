import strawberry

@strawberry.type
class TagType:
    id: str
    name: str

@strawberry.type
class TagResponse:
    tags: list[TagType]

@strawberry.input
class TagInput:
    name: str
    rework_data_id: int

