import sys
from os import path, environ
from PySide6.QtWidgets import QApplication

from src.models.handlers.json_connections_handler import JsonDataHandler
from src.views.windows.connections_window import ConnectionsWindow


class Application:
    JSON_FILE = "connections.json"

    def __init__(self):
        print(environ)
        self.handler = JsonDataHandler(
            path.join(environ['HOME'], '.config/marmotql/connections.json'))

    def run(self):
        self.app = QApplication(sys.argv)

        connectionWindow = ConnectionsWindow(self.handler)
        connectionWindow.show()

        self.app.setApplicationName("MarmotQL")
        self.app.exec()
