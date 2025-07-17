import json
from os import makedirs, path
from src.models.entities.connections import Connection, Folder, TreeNode


class JsonDataHandler:
    def __init__(self, json_file: str):
        self.json_file = json_file
        print(self.json_file)
        self.root_item = Folder("Connections")
        self.load()

    def load(self):
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                print(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print('error', e)
            return

        self._build_tree(data, self.root_item)

    def _build_tree(self, nodes_data: list[dict], parent_item: TreeNode):
        for node_dict in nodes_data:
            item_type = node_dict.get("type")
            name = node_dict.get("name") or ""

            if item_type == "folder":
                new_item = Folder(name, parent=parent_item)
                if "children" in node_dict:
                    self._build_tree(node_dict["children"], new_item)
            elif item_type == "connection":
                host = node_dict.get("host", "")
                port = node_dict.get("port", "")
                user = node_dict.get("user", "")
                password = node_dict.get("password", "")
                description = node_dict.get("description", "")

                new_item = Connection(name, host=host, port=port, user=user,
                                      password=password, description=description, parent=parent_item)
            else:
                continue

            parent_item.appendChild(new_item)

    def save(self, root_node: TreeNode):
        data = self._serialize_tree(root_node)
        print("Saving connections config", data, self.json_file)
        print(path.dirname(self.json_file), self.json_file)
        makedirs(path.dirname(self.json_file), exist_ok=True)
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def _serialize_tree(self, node: TreeNode):
        output = []
        for child in node._children:
            node_dict = {"name": child.name()}

            if isinstance(child, Folder):
                node_dict["type"] = "folder"
                node_dict["children"] = self._serialize_tree(child)
            elif isinstance(child, Connection):
                node_dict["type"] = "connection"
                node_dict["host"] = child.host
                node_dict["port"] = child.port
                node_dict["user"] = child.user
                node_dict["password"] = child.password
                node_dict["description"] = child.description
            output.append(node_dict)

        return output
