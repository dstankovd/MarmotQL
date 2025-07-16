import sys
from PySide6.QtWidgets import QApplication, QSplitter, QFileSystemModel, QTreeView, QListView
from PySide6.QtCore import QDir

from src.models.handlers.json_connections_handler import JsonDataHandler
from src.views.windows.connections_window import ConnectionsWindow


class Application:
    JSON_FILE = "connections.json"

    def __init__(self):
        self.handler = JsonDataHandler(self.JSON_FILE)
        self.handler.load()

    def run(self):
        self.app = QApplication(sys.argv)

        connectionWindow = ConnectionsWindow(self.handler)
        connectionWindow.show()

        self.app.setApplicationName("MarmotQL")
        self.app.exec()
