from utils.file_handler import FileHandler
from models.item import Item
from services.cart_service import save_cart

class Cart:
    """Cart class with cart functionality"""

    def __init__(self, items = []):
        self.items = self.from_dict(items)

    def to_dict(self):
        """Converts Cart items to dictionary for storage"""
        return  [item.to_dict() for item in self.items]
    
    def from_dict(self, data):
        return [Item(**item) for item in data]


    def __str__(self):
        """Converts Cart object to a string """
        return {
            "items": [item.to_dict() for item in self.items],
            "total": self.get_total()
        }   
    

    def remove_item(self, item: Item, quantity: int):
        """Remove item from the cart."""
        for i, s in enumerate(self.items):
            if s.name == item.name:
                if quantity >= item.purchased:
                    item.return_item(quantity)
                    del self.items[i]
                else:
                    item.return_item(quantity)
                save_cart(self.to_dict())
                return True
        return False


    def add_item(self, item: Item, quantity: int):
        """Add item to the cart."""
        if item.get_stock() >= quantity:
            if item in self.items:
                item.purchase_item(quantity)
            else:
                item.purchase_item(quantity)
                self.items.append(item)
            save_cart(self.to_dict())
            return True
        return False
    

    def get_total(self):
        """Get total price of the cart."""
        total = 0
        for item in self.items:
            total += item.get_price() * item.purchased
        return total


    def clear(self):
        """Clear the cart."""
        self.items = []
        save_cart(self.to_dict())


    def view_cart(self):
        """View the cart."""
        return self.__str__()
    

    def checkout(self,email: str):
        """Checkout the cart."""
        db = "db/orders.json"
        orders = FileHandler.read(db)
        order_data = {
            "user_id": email,
            "items": [item.to_dict() for item in self.items],
            "total_price": self.get_total(),
            "status" : "pending"
        }
        orders.append(order_data)
        FileHandler.write(db, orders)
        for item in self.items:
            item.clear_purchase()
        self.clear()
        return True

