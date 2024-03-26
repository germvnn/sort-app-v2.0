import logging

from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox, QPushButton, QLabel

from utilities import load_settings, save_settings
from variables import *

logger = logging.getLogger('settings')


class CheckBoxSettings(QDialog):
    def __init__(self, config_file, settings_key, title):
        super().__init__()
        logger.info(f"Open {title}")
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.config_file = config_file
        self.settings_key = settings_key
        # Load settings from file
        self.settings = load_settings(self.config_file)
        self.settings_content = self.settings[self.settings_key].items()
        self.checkboxes = {}
        self.setFixedWidth(200)

        # Create checkboxes for each setting
        for key, value in self.settings_content:
            cb = QCheckBox(key)
            cb.setChecked(value)
            self.checkboxes[key] = cb
            self.layout.addWidget(cb)

        # Status label
        self.status_label = QLabel()
        self.layout.addWidget(self.status_label)

        # Apply button
        self.apply_btn = QPushButton('Set')
        self.apply_btn.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.apply_btn)

        self.setLayout(self.layout)

    def apply_changes(self) -> None:
        # Update settings based on checkbox states
        for key, cb in self.checkboxes.items():
            self.settings[self.settings_key][key] = cb.isChecked()
            logger.info(f"Set {key} to {cb.isChecked()}")

        # Save updated settings back to file
        if save_settings(settings=self.settings, filename=self.config_file):
            self.status_label.setText(f"{SUCCESS} Settings saved")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText(FAILURE)
            self.status_label.setStyleSheet("color: red;")


class PullingSettings(CheckBoxSettings):
    def __init__(self):
        super().__init__(config_file=PULLING_CONFIG_FILE, settings_key="execute", title="Pulling Settings")


class RunnerSettings(CheckBoxSettings):
    def __init__(self):
        super().__init__(config_file=RUNNER_CONFIG_FILE, settings_key="pulling_executor", title="Runner Settings")


if __name__ == "__main__":
    app = QApplication([])
    window = PullingSettings()
    window.show()
    app.exec()
