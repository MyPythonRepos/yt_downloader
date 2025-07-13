import logging
import os

def setup_logger():
    # Crear carpeta de logs si no existe
    log_folder = 'logs'
    os.makedirs(log_folder, exist_ok=True)

    log_file = os.path.join(log_folder, 'app.log')

    # Crear logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formato común
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

    # Handler para fichero
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Evita duplicar handlers si setup_logger() se llama más de una vez
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)