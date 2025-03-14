import json

class FileHandler:
    @staticmethod
    def get_file_path(role):
        file_paths = {
            "customer": "db/customer.json",
            "staff": "db/staff.json",
            "administrator": "db/administrator.json",
            "owner": "db/owner.json",
            "menu": "db/item.json"
        }
        return file_paths.get(role.lower(), "db/menu.json")    # default to customer file 

    @staticmethod
    def read(role):
        file_path = FileHandler.get_file_path(role)
    
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def write(role, data):
        file_path = FileHandler.get_file_path(role)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)