class Item:
    """Item class"""

    def __init__(self, name : str, price : int, stock : int , promo : int = None, purchased = 0):
        self.name = name
        self.price = price
        self.stock = stock
        self.promo = promo
        self.purchased = purchased

    def to_dict(self):
        """Converts Item object to a dictionary (for JSON response)."""
        return {
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "promo": self.promo,
            "purchased": self.purchased
        }

    def get_stock(self):
        """Return the avaliable stock quantitiy"""
        return self.stock

    def add_stock(self, quantity: int):
        """Increase stock quantity."""
        
        if isinstance(quantity, int) and quantity > 0:
            self.stock += quantity
            return True
        return False
    

    def remove_stock(self, quantity: int):
        """Decrease stock quantity."""
        
        if isinstance(quantity, int) and quantity > 0 and quantity <= self.stock:
            self.stock -= quantity
            return True
        return False
    

    def get_price(self):
        """Get price of item with promo."""
        if self.promo:
            return self.price * ((100 - self.promo) / 100)
        return self.price


    def clear_purchase(self):
        """Clear purchase history."""
        self.purchased = 0


    def purchase_item(self, quantity: int):
        """Purchase item."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.purchased += quantity
            return True
        return False
    
    def return_item(self, quantity: int):
        """Return item."""
        if self.purchased >= quantity:
            self.stock += quantity
            self.purchased -= quantity
            return True
        elif self.purchased < quantity:
            self.stock += self.purchased
            self.purchased = 0
            return True
        return False
