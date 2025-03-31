from models.user import User
from models.cart import Cart
from models.item import Item


class Customer(User):
    """Customer class."""

    def __init__(self, name : str, email : str, password : str, order_history = [], cart = Cart(), role = "customer"):
        super().__init__(name, email, password)
        self.role = "customer"
        self.cart = cart
        self.order_history = []

    def to_dict(self):
        return {
            **super().to_dict(),
            "role": self.role,
            "order_history": self.order_history
            }

    def add_to_cart(self, item: Item, quantity: int):
        """Add item to the cart."""
        return self.cart.add_item(item, quantity)

    def remove_from_cart(self, item : Item, quantity: int):
        """Remove item from the cart."""
        return self.cart.remove_item(item, quantity)

    def view_cart(self):
        """View the cart."""
        return self.cart.view_cart()

    def clear_cart(self):
        """Clear the cart."""
        self.cart.clear()

    def checkout(self):
        """Checkout the cart."""
        self.order_history.append(self.cart.view_cart())
        self.cart.checkout(self.get_email())
        self.clear_cart()

    def show_order_history(self):
        """Show order history."""
        return self.order_history
        

