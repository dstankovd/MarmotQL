from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QTreeView, QSplitter,  QMessageBox, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QAction

from src.models.connections.connections_tree_model import ConnectionTreeModel
from src.models.entities.connections import Connection
from src.models.handlers.json_connections_handler import JsonDataHandler
from src.views.widgets.connections.connection_form import ConnectionForm
from src.views.widgets.connections.connections_tree import ConnectionsTree


class ConnectionsWindow(QMainWindow):
    JSON_FILE = "connections.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Connections Viewer")
        self.resize(800, 600)
        self.handler = JsonDataHandler()
        root_item = self.handler.load_from_file(self.JSON_FILE)
        self.tree_model = ConnectionTreeModel(root_item)
        splitter = QSplitter(self)
        self.setCentralWidget(splitter)
        self.tree_view = QTreeView(splitter)
        self.tree_view.setModel(self.tree_model)
        self.tree_view.expandAll()
        self.tree_view.header().resizeSection(0, 200)
        self.connection_form = ConnectionForm(self.tree_model)

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.tree_view)
        new_connection_button = QPushButton("New Connection", self)
        new_connection_button.setShortcut("Ctrl+N")
        new_connection_button.clicked.connect(
            self.connection_form.clear_form)
        self.left_layout.addWidget(new_connection_button)
        left_widget = QWidget()
        left_widget.setLayout(self.left_layout)

        splitter.addWidget(left_widget)
        splitter.addWidget(self.connection_form)
        splitter.setSizes([300, 500])

        self.tree_view.selectionModel().currentChanged.connect(
            self.on_tree_selection_changed)

        self._create_menus()

    def on_tree_selection_changed(self, current_index, previous_index):
        item = current_index.internalPointer()
        if isinstance(item, Connection):
            self.connection_form.set_connection(item, current_index)
        else:
            self.connection_form.clear_form()

    def _create_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        save_action = QAction("&Save to JSON", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

    def save_data(self):
        root_node = self.tree_model._root_node
        self.handler.save_to_file(root_node, self.JSON_FILE)
        QMessageBox.information(
            self, "Success", f"Data saved to {self.JSON_FILE}")
