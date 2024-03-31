import logging
from logging.handlers import RotatingFileHandler
import os
from src.utility.utils import get_base_path

def ensure_directory_exists(path):
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(path):
        os.makedirs(path)

def setup_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Determine the path to the log file
    log_directory = os.path.join(get_base_path(), 'logs')
    ensure_directory_exists(log_directory)
    log_file_path = os.path.join(log_directory, 'application.log')

    # Create a rotating file handler which logs debug messages
    fh = RotatingFileHandler(log_file_path, maxBytes=1024*1024, backupCount=5)  # Log file will rotate after 1MB, keeping up to 5 backup files
    fh.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

m_logger = setup_logging()
