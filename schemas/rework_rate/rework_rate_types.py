from datetime import datetime
from typing import List, Optional 
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
    createdAtDate: datetime
    tags: Optional[List[str]] = None

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
    createdAtDate: datetime

@strawberry.type
class RepoUrlType:
    url: str
    name: str

@strawberry.type
class MeanAndMedianType:
    mean: float
    median: float