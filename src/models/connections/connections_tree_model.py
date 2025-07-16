from typing import Optional
from PySide6.QtCore import QAbstractItemModel, QPersistentModelIndex, QModelIndex, Qt, QObject

from src.models.entities.connections import TreeNode, Connection


class ConnectionTreeModel(QAbstractItemModel):
    def __init__(self, root_node: TreeNode, parent=None):
        super().__init__(parent)
        self._root_node = root_node

    def index(self, row: int, column: int, parent: "QModelIndex | QPersistentModelIndex" = QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self._root_node
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)

        return self.createIndex(row, column, child_item) if child_item else QModelIndex()

    def parent(self, child: QModelIndex | QPersistentModelIndex):  # type: ignore
        if not child.isValid():
            return QModelIndex()

        child_item = child.internalPointer()
        parent_item = child_item.parentItem()

        if parent_item == self._root_node:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: "QModelIndex | QPersistentModelIndex" = QModelIndex()):
        if not parent.isValid():
            parent_item = self._root_node
        else:
            parent_item = parent.internalPointer()

        return parent_item.childCount()

    def columnCount(self, parent: "QModelIndex | QPersistentModelIndex" = QModelIndex()):
        return 2

    def data(self, index, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return item.name()
            if index.column() == 1:
                return item.typeInfo()

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Name"
            if section == 1:
                return "Type"
        return None

    def refreshItem(self, item_index):
        start_index = self.index(item_index.row(), 0, item_index.parent())
        end_index = self.index(
            item_index.row(), self.columnCount() - 1, item_index.parent())
        self.dataChanged.emit(start_index, end_index, [
                              Qt.ItemDataRole.DisplayRole])

    def addNewConnection(self, name, host, port, user, password, description, parent: Optional[TreeNode] = None):
        if not name or not host or not user:
            return None

        if parent is None:
            parent = self._root_node

        new_connection = Connection(
            name=name,
            host=host,
            port=port,
            user=user,
            password=password,
            description=description,
            parent=parent
        )

        self._root_node.appendChild(new_connection)
        new_index = self.index(new_connection.row(), 0, QModelIndex())
        self.dataChanged.emit(new_index, new_index, [
                              Qt.ItemDataRole.DisplayRole])
        return new_connection
