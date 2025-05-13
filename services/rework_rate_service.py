from repositories.rework_rate_repository import ReworkRepository
from resolvers.rework import convert_to_type
from core.utils.formatter import extract_repo_name
from schemas.rework_rate.rework_rate_types import ReworkDataType, RepoUrlType, MeanAndMedianType
from datetime import datetime
from typing import Optional

class ReworkService:
    def __init__(self, repo: ReworkRepository):
        self.repo = repo

    def get_all_data(self) -> list[ReworkDataType]:
        records = self.repo.get_all()
        return [convert_to_type(record) for record in records]

    def get_by_pr(self, pr_number: str) -> Optional[ReworkDataType]:
        record = self.repo.get_by_pr_number(pr_number)
        return convert_to_type(record) if record else None

    def get_all_repos(self) -> list[RepoUrlType]:
        urls = self.repo.get_all_repo_urls()
        return [RepoUrlType(url=u[0], name=extract_repo_name(u[0])) for u in urls]

    def get_rework_history(
        self, repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[ReworkDataType]:
        records = self.repo.get_by_repo_and_dates(repo_url, start_date, end_date)
        return [convert_to_type(record) for record in records]

    def get_mean_and_median(
        self, repo_url: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> MeanAndMedianType:
        records = self.repo.get_by_period_range(repo_url, start_date, end_date)
        if not records:
            return MeanAndMedianType(mean=0.0, median=0.0)

        rework_percentages = [r.rework_percentage for r in records]
        mean = sum(rework_percentages) / len(rework_percentages)
        sorted_rp = sorted(rework_percentages)
        n = len(sorted_rp)

        median = (
            (sorted_rp[n // 2 - 1] + sorted_rp[n // 2]) / 2
            if n % 2 == 0 else sorted_rp[n // 2]
        )

        return MeanAndMedianType(mean=mean, median=median)

    def create_record(self, data_dict: dict):
        return self.repo.create(data_dict)

    def delete_repo(self, url: str):
        if not self.repo.exists_by_repo_url(url):
            return False
        self.repo.delete_by_repo_url(url)
        return True
