from sqlalchemy.orm import Query
from repositories.rework.RepositoryRework import RepositoryRework as ReworkRepository
from models.rework import ReworkDataDB
from schemas.rework_rate.rework_rate_types import MeanAndMedianType


class ServiceRework:
    """
    Servicio para manejar la lógica de negocio relacionada con los datos de rework.
    Proporciona métodos para obtener, crear y eliminar registros de rework.
    """

    def __init__(self, repo: ReworkRepository):
        self.repo = repo

    def get_mean_and_median(sefl, records: Query[ReworkDataDB]):
        """
        Calcula la media y mediana de las líneas rework.
        """
        if not records:
            return MeanAndMedianType(mean=0.0, median=0.0)

        # Calculate mean and median of rework percentages
        rework_percentages = [record.rework_percentage for record in records]
        mean = sum(rework_percentages) / len(rework_percentages)

        sorted_percentages = sorted(rework_percentages)
        n = len(sorted_percentages)
        if n % 2 == 0:
            median = (sorted_percentages[n // 2 - 1] + sorted_percentages[n // 2]) / 2
        else:
            median = sorted_percentages[n // 2]

        return MeanAndMedianType(mean=mean, median=median)

   