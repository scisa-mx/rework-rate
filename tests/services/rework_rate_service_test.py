import pytest
from repositories.rework_rate_repository import ReworkRepository
from services.rework_rate_service import ReworkService
from tests.factories.rework_rate_factory import ReworkDataFactory
from models.rework import ReworkDataDB

# Fixture que configura el servicio y agrega datos de prueba a la base de datos
@pytest.fixture
def setup_service_with_data(db_session):
    """
    Configura un repositorio y un servicio, luego crea varios registros 
    aleatorios en la base de datos utilizando un 'factory'.
    
    Args:
        db_session (Session): La sesión de la base de datos.
    
    Returns:
        tuple: Una tupla que contiene la sesión de la base de datos y el servicio configurado.
    """
    repo = ReworkRepository(db_session)
    
    # Generamos varios registros aleatorios para las pruebas
    for _ in range(10):
        ReworkDataFactory.create_in_repo(repo)
    
    service = ReworkService(repo)
    return db_session, service

# Test que verifica el cálculo de la media y la mediana de los datos de rework
def test_mean_and_median_with_factory(setup_service_with_data: tuple[ReworkDataDB, ReworkService]):
    """
    Test para asegurar que el servicio puede calcular la media y la mediana de los datos de rework.
    
    Args:
        setup_service_with_data (tuple): Fixture que proporciona la sesión de base de datos y el servicio.
    """
    db_session, service = setup_service_with_data
    
    any_url = db_session.query(ReworkDataDB.repo_url).first()[0]

    result = service.get_mean_and_median(
        repo_url=any_url, start_date=None, end_date=None
    )

    # Verificamos que los resultados sean números flotantes
    assert isinstance(result.mean, float)
    assert isinstance(result.median, float)

# Test que verifica que el servicio retorna las URLs de los repositorios correctamente
def test_get_repo_urls(setup_service_with_data: tuple[ReworkDataDB, ReworkService]):
    """
    Test para asegurar que el servicio puede devolver correctamente las URLs y nombres de los repositorios.
    
    Args:
        setup_service_with_data (tuple): Fixture que proporciona la sesión de base de datos y el servicio.
    """
    _, service = setup_service_with_data
    
    urls = service.get_all_repos()
    
    # Verificamos que las URLs devueltas sean una lista y que cada elemento tenga los atributos correctos
    assert isinstance(urls, list)
    assert all(hasattr(url, "url") for url in urls)
    assert all(hasattr(url, "name") for url in urls)

# Test que verifica que el servicio devuelve el historial de datos de rework correctamente
def test_get_all_rework_data(setup_service_with_data: tuple[ReworkDataDB, ReworkService]):
    """
    Test para asegurar que el servicio puede devolver el historial completo de datos de rework de un repositorio.
    
    Args:
        setup_service_with_data (tuple): Fixture que proporciona la sesión de base de datos y el servicio.
    """
    db_session, service = setup_service_with_data
    
    any_url = db_session.query(ReworkDataDB.repo_url).first()[0]

    results = service.get_rework_history(
        repo_url=any_url, start_date=None, end_date=None
    )

    # Verificamos que los resultados sean una lista con al menos un elemento, 
    # y que cada elemento tenga los atributos esperados
    assert isinstance(results, list)
    assert len(results) > 0
    assert hasattr(results[0], "author")
    assert hasattr(results[0], "rework_percentage")
