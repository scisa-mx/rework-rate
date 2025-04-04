from sqlalchemy.orm import Session
import strawberry
from models.rework import ReworkDataDB
from schemas.rework_rate.rework_rate_types import ReworkDataType
from resolvers.rework import convert_to_type

@strawberry.type
class Query:
    @strawberry.field
    def get_rework_data(self, info) -> list[ReworkDataType]:
        db: Session = info.context["db"]
        records = db.query(ReworkDataDB).all()
        return [convert_to_type(record) for record in records]

    @strawberry.field
    def get_rework_data_by_pr(self, info, pr_number: str) -> ReworkDataType:
        db: Session = info.context["db"]
        record = db.query(ReworkDataDB).filter(ReworkDataDB.pr_number == pr_number).first()
        return convert_to_type(record) if record else None
