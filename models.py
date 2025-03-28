from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReworkData(BaseModel):
    repo_url: str
    pr_number: str
    author: str
    pr_approver: str
    timestamp: datetime
    rework_percentage: float
    total_commits: int
    period_start: datetime
    period_end: datetime
    modified_lines: int
    rework_lines: int 