import json

from src.models.entities.connections import Connection, Folder


class JsonDataHandler:
    def load_from_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return Folder("Connections")

        root_item = Folder("Connections")
        self._build_tree(data, root_item)

        return root_item

    def _build_tree(self, nodes_data, parent_item):
        for node_dict in nodes_data:
            item_type = node_dict.get("type")
            name = node_dict.get("name")

            if item_type == "folder":
                new_item = Folder(name, parent=parent_item)
                if "children" in node_dict:
                    self._build_tree(node_dict["children"], new_item)
            elif item_type == "connection":
                new_item = Connection(name, host=node_dict.get("host", ""), port=node_dict.get("port", 5432), user=node_dict.get(
                    "user", ""), password=node_dict.get("password", ""), description=node_dict.get("description", ""), parent=parent_item)
            else:
                continue

            parent_item.appendChild(new_item)

    def save_to_file(self, root_node, filepath):
        data = self._serialize_tree(root_node)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def _serialize_tree(self, node):
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
