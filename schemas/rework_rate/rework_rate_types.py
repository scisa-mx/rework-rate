from datetime import datetime
import strawberry

@strawberry.type
class ReworkDataType:
    id: int
    repo_url: str
    pr_number: str
    author: str
    pr_approver: str
    timestamp: datetime
    total_commits: int
    period_start: datetime
    period_end: datetime
    modified_lines: int
    rework_lines: int
    rework_percentage: float

@strawberry.input
class ReworkDataInput:
    repo_url: str
    pr_number: str
    author: str
    pr_approver: str
    timestamp: datetime
    total_commits: int
    period_start: datetime
    period_end: datetime
    modified_lines: int
    rework_lines: int
    rework_percentage: float
