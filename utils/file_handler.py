import json

class FileHandler:
    @staticmethod
    def write(file_path ,data):
        """open json file and write data to it."""
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
                return True
        except FileNotFoundError:
            print("File not found")
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def read(file_path):
        """"open json file and read data from it."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File not found")
            return []
        except Exception as e:
            print(e)
            return []