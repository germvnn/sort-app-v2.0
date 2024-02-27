import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox


class WelcomeWindow(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setText("The beginning of develop sorting app with sophisticated GUI")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorter")
        self.setFixedWidth(500)
        self.setFixedHeight(500)
        WelcomeWindow().exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sorter = MainWindow()
    sorter.show()
    sys.exit(app.exec())
