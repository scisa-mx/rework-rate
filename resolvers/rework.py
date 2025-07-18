from typing import Optional
from models.rework import ReworkDataDB
from schemas.rework_rate.rework_rate_types import ReworkDataType

def convert_to_type(record: ReworkDataDB) -> ReworkDataType:
    tags: Optional[list[str]] = None
    if hasattr(record, "tags") and record.tags is not None:
        tags = [tag.name for tag in record.tags]
    
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
        createdAtDate=record.createdAtDate,
        tags=tags
    )
