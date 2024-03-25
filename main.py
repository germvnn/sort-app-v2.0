import sys
import log
from PyQt6.QtGui import QAction, QDesktopServices
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

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        InfoWindow(message="The beginning of develop sorting app with sophisticated GUI",
                   title="Welcome").exec()

        # Menu Bar -> {item}
        help_menu_item = self.menuBar().addMenu("&Help")
        sets_menu_item = self.menuBar().addMenu("&Settings")

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
        help_menu_item.addAction(github_action)
        github_action.triggered.connect(self._help)

        # MainWindow (bottom) -> Run
        self.runButton = QPushButton("Run", self)
        self.runButton.clicked.connect(self._runner_instructions)
        layout.addWidget(self.runButton, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)

    @staticmethod
    def _pull_settings():
        pull_settings_dialog = PullingSettings()
        pull_settings_dialog.exec()

    @staticmethod
    def _runner_settings():
        runner_settings_dialog = InfoWindow("Runner Settings")
        runner_settings_dialog.exec()

    @staticmethod
    def _help():
        url = QtCore.QUrl("https://github.com/germvnn/sort-app-v2.0")
        QDesktopServices.openUrl(url)

    @staticmethod
    def _runner_instructions():
        executor = PullingExecutor()
        result = executor.pull("C:/Users/Daniel/Desktop/test")
        message = "Success!" if result else "Failure, view logs."
        InfoWindow(message=message, title="Runner").exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sorter = MainWindow()
    sorter.show()
    logger.info("Run Application")
    sys.exit(app.exec())
