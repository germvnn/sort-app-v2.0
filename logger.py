import logging.config
import json

# Wczytanie konfiguracji logowania
with open('configs/logger.json', 'r') as f:
    config_dict = json.load(f)
    logging.config.dictConfig(config_dict)

# Utwórz loggera na podstawie konfiguracji
logger = logging.getLogger("logger")


def success(log_message):
    logger.info(log_message)
    return True


def failure(log_message):
    logger.error(log_message)
    return False
