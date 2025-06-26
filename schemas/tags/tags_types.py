import strawberry

@strawberry.type
class TagType:
    id: str
    name: str
    color: str

@strawberry.type
class TagResponse:
    tags: list[TagType]

@strawberry.input
class TagInput:
    names: list[str]
    rework_data_id: int

