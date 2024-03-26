import sys
import log
from PyQt6.QtGui import QAction, QDesktopServices
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog,
                             QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy)
from PyQt6 import QtCore

from executor import PullingExecutor
from utilities import InfoWindow, load_settings, save_settings
from settings import PullingSettings, RunnerSettings
from variables import *

logger = log.setup_logger('root')


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorter")
        self.setGeometry(100, 100, 500, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        InfoWindow(message="The beginning of develop sorting app with sophisticated GUI",
                   title="Welcome").exec()

        # Menu Bar -> {item}
        help_menu_item = self.menuBar().addMenu("&Help")
        sets_menu_item = self.menuBar().addMenu("&Settings")
        test_menu_item = self.menuBar().addMenu("&Test")

        # Menu Bar -> Settings -> Pulling
        pulling_settings = QAction("Pulling", self)
        pulling_settings.triggered.connect(self._pull_settings)
        sets_menu_item.addAction(pulling_settings)

        # Menu Bar -> Settings -> Runner
        runner_settings = QAction("Runner", self)
        runner_settings.triggered.connect(self._runner_settings)
        sets_menu_item.addAction(runner_settings)

        # Menu Bar -> Help -> GitHub
        github_action = QAction("GitHub", self)
        github_action.triggered.connect(self._help)
        help_menu_item.addAction(github_action)

        # Menu Bar -> Test -> Extract
        extract_action = QAction("Extract", self)
        extract_action.triggered.connect(self._test_extract)
        test_menu_item.addAction(extract_action)

        # Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        # MainWindow (bottom) -> Current path: {path}
        self.path_config = load_settings(RUNNER_CONFIG_FILE)
        self.path = self.path_config['path']
        self.pathLabel = QLabel(f"Current path: {self.path}", self)
        layout.addWidget(self.pathLabel, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

        # MainWindow (bottom) -> Choose Path
        self.choosePathButton = QPushButton("Choose Path", self)
        self.choosePathButton.clicked.connect(self._choose_path)
        layout.addWidget(self.choosePathButton, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

        # MainWindow (bottom) -> Run
        self.runButton = QPushButton("Run", self)
        self.runButton.clicked.connect(self._runner_instructions)
        layout.addWidget(self.runButton, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

    def _choose_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.pathLabel.setText(f"Current path: {path}")
            self.path_config['path'] = path
            logger.info(f"Set path: {path} in {RUNNER_CONFIG_FILE}")
            save_settings(settings=self.path_config, filename=RUNNER_CONFIG_FILE)
        else:
            self.pathLabel.setText("No path selected")

    def _test_extract(self):
        PullingExecutor.extract_images(self.path)
        InfoWindow(message=SUCCESS, title="Extraction").exec()

    def _runner_instructions(self):
        executor = PullingExecutor()
        result = executor.pull(self.path)
        message = SUCCESS if result else FAILURE
        InfoWindow(message=message, title="Runner").exec()

    @staticmethod
    def _pull_settings():
        pull_settings_dialog = PullingSettings()
        pull_settings_dialog.exec()

    @staticmethod
    def _runner_settings():
        runner_settings_dialog = RunnerSettings()
        runner_settings_dialog.exec()

    @staticmethod
    def _help():
        QDesktopServices.openUrl(REPOSITORY_URL)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sorter = MainWindow()
    sorter.show()
    logger.info("Run Application")
    sys.exit(app.exec())
