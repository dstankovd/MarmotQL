
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QSpinBox

from src.models.connections.connections_tree_model import ConnectionTreeModel


class ConnectionForm(QWidget):
    def __init__(self, model: ConnectionTreeModel):
        super().__init__()
        self.model = model
        self.current_connection = None
        self.current_index = None
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.host_edit = QLineEdit()
        self.port_edit = QSpinBox()
        self.port_edit.setRange(1, 65535)
        self.user_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.description_edit = QLineEdit()
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Host:", self.host_edit)
        form_layout.addRow("Port:", self.port_edit)
        form_layout.addRow("User:", self.user_edit)
        form_layout.addRow("Password:", self.password_edit)
        form_layout.addRow("Description:", self.description_edit)
        layout.addLayout(form_layout)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._save_changes)
        layout.addWidget(self.save_button)
        layout.addStretch()
        self.clear_form()

    def set_connection(self, connection_node, index):
        self.current_connection = connection_node
        self.current_index = index
        self.name_edit.setText(connection_node.name())
        self.host_edit.setText(connection_node.host)
        self.port_edit.setValue(connection_node.port)
        self.user_edit.setText(connection_node.user)
        self.password_edit.setText(connection_node.password)
        self.description_edit.setText(connection_node.description)

    def clear_form(self):
        self.current_connection = None
        self.current_index = None
        self.name_edit.clear()
        self.host_edit.clear()
        self.port_edit.clear()
        self.user_edit.clear()
        self.password_edit.clear()
        self.description_edit.clear()

    def _save_changes(self):
        if not self.current_connection:
            return
        self.current_connection.setName(self.name_edit.text())
        self.current_connection.host = self.host_edit.text()
        self.current_connection.port = self.port_edit.value()
        self.current_connection.user = self.user_edit.text()
        self.current_connection.password = self.password_edit.text()
        self.current_connection.description = self.description_edit.text()
        self.model.refreshItem(self.current_index)
        QMessageBox.information(self, "Success", "Connection updated.")
