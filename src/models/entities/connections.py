from typing import Optional


class TreeNode:
    def __init__(self, name: str, parent: Optional['TreeNode'] = None):
        self._name = name
        self._parent = parent
        self._children = []

    def appendChild(self, item: 'TreeNode'):
        self._children.append(item)

    def child(self, row: int) -> Optional['TreeNode']:
        return self._children[row] if 0 <= row < len(self._children) else None

    def childCount(self) -> int:
        return len(self._children)

    def parentItem(self) -> Optional['TreeNode']:
        return self._parent

    def row(self) -> int:
        return self._parent._children.index(
            self) if self._parent else 0

    def name(self) -> str:
        return self._name

    def setName(self, name: str):
        self._name = name

    def typeInfo(self) -> str:
        return "Node"


class Folder(TreeNode):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

    def typeInfo(self):
        return "Folder"


class Connection(TreeNode):
    def __init__(self, name, host="", port=5432, user="", password="", description="", parent=None):
        super().__init__(name, parent)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.description = description

    def typeInfo(self):
        return "Connection"
