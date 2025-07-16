import sys
from PySide6.QtWidgets import QApplication, QSplitter, QFileSystemModel, QTreeView, QListView
from PySide6.QtCore import QDir

from src.views.windows.connections_window import ConnectionsWindow


class Application:
    def __init__(self):
        pass

    def run(self):
        self.app = QApplication(sys.argv)

        connectionWindow = ConnectionsWindow()
        connectionWindow.show()

        self.app.setApplicationName("MarmotQL")
        self.app.exec()
