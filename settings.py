import logging
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox, QPushButton, QLabel
from utilities import load_settings, save_settings, InfoWindow

logger = logging.getLogger('settings')


class PullingSettings(QDialog):
    def __init__(self):
        super().__init__()
        logger.info("Open Pulling Setting")
        self.setWindowTitle('ExecutorADB Settings')
        self.layout = QVBoxLayout()
        self.config_file = "adbexecutor.json"
        # Load settings from file
        self.settings = load_settings(self.config_file)
        self.checkboxes = {}
        self.setFixedWidth(200)

        # Create checkboxes for each setting in "execute"
        for key, value in self.settings["execute"].items():
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

    def apply_changes(self):
        # Update settings based on checkbox states
        for key, cb in self.checkboxes.items():
            self.settings["execute"][key] = cb.isChecked()
            logger.info(f"Set {key} to {cb.isChecked()}")

        # Save updated settings back to file
        if save_settings(settings=self.settings, filename=self.config_file):
            self.status_label.setText("Success: Settings saved")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("Fail: View logs.")
            self.status_label.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = QApplication([])
    window = PullingSettings()
    window.show()
    app.exec()
