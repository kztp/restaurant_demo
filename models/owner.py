from models.user import User
from utils.file_handler import FileHandler

class Owner(User):
    """Owner class"""

    def __init__(self, name, email, password, role = "owner"):
        super().__init__(name, email, password)
        self.role = "owner"

    def to_dict(self):
        return {
            **super().to_dict(),
            "role": self.role
            }
    
    def show_staffs(self):
        """show all the staffs"""
        db = "db/staff.json"
        return FileHandler.read(db)

    def show_sales(self):
        """show all the complete order for analysis view"""
        db = "db/orders_finished.json"
        orders = FileHandler.read(db)
        total = 0
        data = {}
        for order in orders:
            total += order["total_price"]
            for item in order["items"]:
                if item["name"] not in data:
                    data[item["name"]] = item["purchased"]
                else:
                    data[item["name"]] += item["purchased"]
        return [data, total]

