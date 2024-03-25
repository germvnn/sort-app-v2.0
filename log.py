import logging
import logging.config
from datetime import datetime
from utilities import load_settings


def setup_logger(name):
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    log_filename = f"logs/processing_{current_time}.log"

    log_config = load_settings("logger.json")
    log_config['handlers']['fileHandler']['filename'] = log_filename
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(name)
    return logger
