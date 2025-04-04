import logging
import os

# Definir la ruta donde se guardarán los logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configuración básica del logger
def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Puedes usar DEBUG, INFO, WARNING, ERROR, CRITICAL

    # Crear un manejador que escriba los logs en un archivo
    log_file = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Puedes cambiar el nivel del log para cada archivo

    # Crear un formato para los logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Añadir el manejador al logger
    logger.addHandler(file_handler)
    
    # También agregar un manejador para mostrar en consola (opcional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Nivel de consola
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
