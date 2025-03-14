from utils.file_handler import FileHandler
import json

class Item:
    def __init__(self, item_id: str, name: str, price: float, stock: int):   #img_path: str
        self.item_id = item_id
        self.name = name
        self.price = price
        self.stock = stock  # Available stock quantity
        #self.img_path = img_path
        self.role = 'menu'

    def update_stock(self, quantity: int) -> bool:
        """Updates stock when an item is purchased or restocked."""
        if self.stock + quantity < 0:
            return False  # Not enough stock
        self.stock += quantity
        return True

    def to_dict(self):
        """Converts Item object to a dictionary (for JSON response)."""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            ##"img_path": self.img_path   
        }

    @staticmethod
    def load_items():
        """Load all items from json file."""
    
        items_list = FileHandler.read('menu') 
        print("items_list", items_list)
        return [Item(**data) for data in items_list]  


    @staticmethod
    def save_items(items):
        """Save the updated item list to json file."""
        items_data = [item.to_dict() for item in items]  
        FileHandler.write('menu', items_data)  


