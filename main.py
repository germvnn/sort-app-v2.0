import sys
import log
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout
from PyQt6 import QtCore

from executor import PullingExecutor
from utilities import InfoWindow
from settings import PullingSettings
logger = log.setup_logger('root')


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorter")
        self.setGeometry(100, 100, 500, 500)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        InfoWindow(message="The beginning of develop sorting app with sophisticated GUI",
                   title="Welcome").exec()

        help_menu_item = self.menuBar().addMenu("&Help")
        sets_menu_item = self.menuBar().addMenu("&Settings")

        executor_adb_settings = QAction("Pulling", self)
        executor_adb_settings.triggered.connect(self._pull_settings)
        sets_menu_item.addAction(executor_adb_settings)

        help_action = QAction("Documentation", self)
        help_menu_item.addAction(help_action)
        help_action.triggered.connect(self._help)

        self.runButton = QPushButton("Run", self)
        self.runButton.clicked.connect(self._run_instructions)
        layout.addWidget(self.runButton, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

    @staticmethod
    def _pull_settings():
        pull_settings_dialog = PullingSettings()
        pull_settings_dialog.exec()

    @staticmethod
    def _help():
        help_dialog = InfoWindow(message="github")
        help_dialog.exec()

    @staticmethod
    def _run_instructions():
        executor = PullingExecutor()
        result = executor.pull("C:/Users/Daniel/Desktop/test")
        message = "Success" if result else "Failure"
        InfoWindow(message=message, title="Runner").exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sorter = MainWindow()
    sorter.show()
    sys.exit(app.exec())
