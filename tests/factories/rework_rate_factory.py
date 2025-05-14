from datetime import datetime, timedelta
from typing import Dict, Any
from faker import Faker

fake = Faker()

class ReworkDataFactory:
    """
    Factory para generar datos de prueba que imitan ReworkDataType / ReworkDataInput.
    """
    @staticmethod
    def _random_datetime(start_year: int = 2023, end_year: int = 2025) -> datetime:
        """Genera un datetime aleatorio entre dos años."""
        start = datetime(start_year, 1, 1)
        end = datetime(end_year, 12, 31, 23, 59, 59)
        return fake.date_time_between(start_date=start, end_date=end)

    @classmethod
    def build_dict(cls) -> Dict[str, Any]:
        """
        Retorna un dict con campos llenados aleatoriamente,
        listo para pasar al método create() de tu ReworkRepository.
        """
        period_start = cls._random_datetime()
        # Asegura que period_end sea luego de period_start
        period_end = period_start + timedelta(days=fake.random_int(min=0, max=7))
        timestamp   = period_start + timedelta(hours=fake.random_int(min=0, max=72))
        created_at  = period_end + timedelta(hours=fake.random_int(min=0, max=24))

        total_commits     = fake.random_int(min=1, max=20)
        modified_lines    = fake.random_int(min=1, max=500)
        rework_lines      = fake.random_int(min=0, max=modified_lines)
        rework_percentage = round((rework_lines / modified_lines) * 100, 2) if modified_lines else 0.0

        return {
            "repo_url": fake.url(),
            "pr_number": fake.bothify(text="PR-####"),
            "author": fake.name(),
            "pr_approver": fake.name(),
            "timestamp": timestamp,
            "total_commits": total_commits,
            "period_start": period_start,
            "period_end": period_end,
            "modified_lines": modified_lines,
            "rework_lines": rework_lines,
            "rework_percentage": rework_percentage,
            "createdAtDate": created_at,
        }

    @classmethod
    def create_in_repo(cls, repo) -> Any:
        """
        Genera datos con build_dict() y los inserta usando el método create() del repositorio.
        Devuelve la instancia creada.
        """
        data = cls.build_dict()
        return repo.create(data)
