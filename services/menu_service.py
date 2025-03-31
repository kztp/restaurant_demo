from utils.file_handler import FileHandler

def get_all_menu():
    db = "db/menu.json"
    return FileHandler.read(db)