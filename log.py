import logging.config
from utilities import load_settings


def setup_logger(name):
    config_dict = load_settings("logger.json")
    logging.config.dictConfig(config_dict)
    logger = logging.getLogger(name)
    return logger
