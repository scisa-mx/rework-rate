from sqlalchemy.orm import Session
import strawberry
from models.rework import ReworkDataDB
from models.rework import ReworkDataType, ReworkDataInput

def convert_to_type(record: ReworkDataDB) -> ReworkDataType:
    return ReworkDataType(
        id=record.id,
        repo_url=record.repo_url,
        pr_number=record.pr_number,
        author=record.author,
        pr_approver=record.pr_approver,
        timestamp=record.timestamp,
        total_commits=record.total_commits,
        period_start=record.period_start,
        period_end=record.period_end,
        modified_lines=record.modified_lines,
        rework_lines=record.rework_lines,
        rework_percentage=record.rework_percentage,
    )

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
