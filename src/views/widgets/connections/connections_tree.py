
from PySide6.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem, QStyle
from PySide6.QtCore import Qt


class ConnectionsTree(QTreeWidget):
    def __init__(self, connections):
        super().__init__()
        self.connections = connections

        self.setExpandsOnDoubleClick(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setAutoScroll(True)
        self.setUniformRowHeights(True)
        self.setColumnCount(2)
        self.setHeaderHidden(False)
        self.setHeaderLabels(["Name", "Description"])
        self.setRootIsDecorated(True)
        self.setItemsExpandable(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        self.populate_tree(self.invisibleRootItem(), self.connections)

    def populate_tree(self, parent, items):
        for item in items:
            print(item)
            if not isinstance(item, dict):
                continue

            if item["type"] == "group":
                tree_item = QTreeWidgetItem([item["name"]])
                parent.addChild(tree_item)
                self.populate_tree(tree_item, item.get("children", []))

            else:
                tree_item = QTreeWidgetItem([item["name"]])
                tree_item.setData(0, 1, item)
                if item.get("type") == "connection":
                    tree_item.setIcon(0, self.style().standardIcon(
                        QStyle.StandardPixmap.SP_FileIcon))
                    tree_item.setToolTip(
                        0, f"Host: {item['host']}\nPort: {item['port']}\nUser: {item['user']}")
                    tree_item.setFlags(tree_item.flags() |
                                       Qt.ItemFlag.ItemIsEditable)
                    tree_item.setFlags(tree_item.flags() & ~
                                       Qt.ItemFlag.ItemIsDropEnabled)
                else:
                    tree_item.setIcon(0, self.style().standardIcon(
                        QStyle.StandardPixmap.SP_DirIcon))

                parent.addChild(tree_item)
