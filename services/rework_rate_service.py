from repositories.rework_rate_repository import ReworkRepository
from schemas.rework_rate.rework_rate_types import MeanAndMedianType

class ReworkService:
    def __init__(self, repo: ReworkRepository):
        self.repo = repo

    def get_mean_and_median(self, repo_url, start_date, end_date):
        records = self.repo.get_by_repo_and_period(repo_url, start_date, end_date)

        if not records:
            return MeanAndMedianType(mean=0.0, median=0.0)

        rework_percentages = [r.rework_percentage for r in records]
        mean = sum(rework_percentages) / len(rework_percentages)

        sorted_vals = sorted(rework_percentages)
        n = len(sorted_vals)
        median = (
            (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
            if n % 2 == 0 else sorted_vals[n // 2]
        )

        return MeanAndMedianType(mean=mean, median=median)
