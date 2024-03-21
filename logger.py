import logging.config
import json

with open('configs/logger.json', 'r') as f:
    config_dict = json.load(f)
    logging.config.dictConfig(config_dict)

logger = logging.getLogger("logger")


def success(log_message):
    logger.info(log_message)
    return True


def failure(log_message):
    logger.error(log_message)
    return False
