import json
import git
import os
import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger('utilities')


class InfoWindow(QMessageBox):
    def __init__(self, message, title="Message"):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        logger.info(f"Run InfoWindow with Title: {title}, Message: {message}")


def success(log_message):
    logger.info(log_message)
    return True


def failure(log_message):
    logger.error(log_message)
    return False


def get_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    root = git_repo.git.rev_parse("--show-toplevel")
    return root


def load_settings(filename):
    try:
        with open(os.path.join(get_root(__file__)+'/configs', filename), 'r') as file:
            logger.info(f"Configs from {filename} successfully load")
            return json.load(file)
    except Exception as e:
        return failure(f"Configs from {filename}. Message: {e}")


def save_settings(settings, filename):
    try:
        with open(os.path.join(get_root(__file__)+'/configs', filename), 'w') as file:
            json.dump(settings, file, indent=4)
            return success(f"Configs successfully saved to {filename}")
    except Exception as e:
        return failure(f"Saving configs failure due to {e}.")


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Create directory: {path}")
