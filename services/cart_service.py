from utils.file_handler import FileHandler

def save_cart(data):
    db = "db/cart.json"
    FileHandler.write(db, data)

def return_cart():
    db = "db/cart.json"
    return FileHandler.read(db)