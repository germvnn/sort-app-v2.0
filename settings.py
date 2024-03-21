import logging
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox, QPushButton
from utilities import load_settings, save_settings, InfoWindow

logger = logging.getLogger(__file__)


class PullingSettings(QDialog):
    def __init__(self):
        super().__init__()
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

        # Apply button
        self.apply_btn = QPushButton('Set')
        self.apply_btn.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.apply_btn)

        self.setLayout(self.layout)

    def apply_changes(self):
        # Update settings based on checkbox states
        for key, cb in self.checkboxes.items():
            self.settings["execute"][key] = cb.isChecked()

        # Save updated settings back to file
        message = "Success" if save_settings(settings=self.settings, filename=self.config_file) else "Fail, View logs."
        InfoWindow(message=message).exec()


if __name__ == "__main__":
    app = QApplication([])
    window = PullingSettings()
    window.show()
    app.exec()
