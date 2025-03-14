from utils.file_handler import FileHandler
from models.item import Item

class User:   

    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role


    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
    
    @classmethod
    def from_dict(cls, user_dict):
        """Reconstruct the object from a dictionary (read from JSON)"""

        if user_dict["role"] == "customer":
            return Customer(**user_dict)
        elif user_dict["role"] == "staff":
            return Staff(**user_dict)
        elif user_dict["role"] == "administrator":
            return Administrator(**user_dict)
        elif user_dict["role"] == "owner":
            return Owner(**user_dict)
        else:
            raise ValueError("Invalid role")


    @classmethod
    def get_all_users(cls, role):
        return FileHandler.read(role)


    @classmethod
    def add_user(cls, user):
        users = FileHandler.read(user.role)
        users.append(user.to_dict())
        FileHandler.write(user.role, users)


class Customer(User):
    def __init__(self, user_id, name, email, password, order_history, cart, role='customer'): 
        super().__init__(user_id, name, email, password, role='customer')
        self.order_history = order_history
        self.cart = cart

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "order_history": self.order_history,
            "cart" : self.cart
        }

    @staticmethod
    def save_customers(customers):
        """Save all customers to the file."""

        print("save method called")
        # Convert the list of Customer objects into a list of dictionaries
        customer_data = [customer.to_dict() for customer in customers] 
        print(customer_data)
        
        # Write the data to the file
        FileHandler.write("customer", customer_data)

    @staticmethod
    def load_customers():
        """Load customers from the file."""
        # Read the data from the file
        customer_data = FileHandler.read('customer')
        
        # Convert the list of dictionaries back into Customer objects
        return [Customer.from_dict(customer) for customer in customer_data]

    def add_to_cart(self, item: Item, quantity: int) -> bool:
        """Adds an item object to the cart."""
        if item.stock < quantity:
            print("Not enough stock available.")
            return False
        
        print(self.cart)

        # if not self.cart:
        #     self.cart.append(item)
        #     print("self card = ",self.cart)

        # if self.cart:
        #     print("hello")
        #     if item in self.cart:
        #         print("hello")
        #         print("item = ",item)
        #         item.quantity += quantity #self.cart[obj]
        
        
        print(f"{quantity}x {item.name} added to cart.")
        return True
    
    def remove_from_cart(self, item: Item, quantity: int) -> bool:
        """Removes an item from the cart."""
        if item in self.cart:
            if self.cart[item] <= quantity:
                del self.cart[item]             # Remove item if quantity reaches zero
            else:
                self.cart[item] -= quantity
            print(f"{quantity}x {item.name} removed from cart.")
            return True
        else:
            print("Item not found in cart.")
            return False

    def view_cart(self):
        """Displays items in the cart."""
        if not self.cart:
            print("Cart is empty.")
            return {}
        
        for item, quantity in self.cart.items():
            print(f"{item.name} - {quantity}x (${item.price} each)")
        return self.cart
    
    def place_order(self) -> bool:
        """Places an order and clears the cart."""
        if not self.cart:
            print("Cart is empty. Cannot place order.")
            return False
        
        total_price = sum(item.price * quantity for item, quantity in self.cart.items())

        # Simulate reducing stock for each item
        for item, quantity in self.cart.items():
            item.update_stock(-quantity)

        # Store order details
        order_details = {"items": self.cart, "total_price": total_price}
        self.order_history.append(order_details)

        print(f"Order placed successfully! Total: ${total_price}")
        self.cart.clear()  # Clear cart after order
        return True
    
    def view_order_history(self):
        """Displays the customer's past orders."""
        if not self.order_history:
            print("No past orders.")
            return []
        
        for idx, order in enumerate(self.order_history, start=1):
            print(f"Order {idx}:")
            for item, quantity in order["items"].items():
                print(f"  - {item.name}: {quantity}x (${item.price} each)")
            print(f"  Total: ${order['total_price']}")
        
        return self.order_history

class Staff(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, role='staff')

    def can_manage_order(self):
        pass

    def can_access_reports(self):
        pass



class Administrator(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, role='administrator')

    def can_manage_staff(self):
        pass

    def can_manage_menu(self):
        pass

    def can_mange_order(self):
        pass

class Owner(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, role='owner')

