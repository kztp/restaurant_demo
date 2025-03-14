from utils.file_handler import FileHandler

class Order:
    FILE_PATH = "db/orders.json"

    def __init__(self, order_id, user_id, items, total_price, status="pending"):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items  # List of menu items
        self.total_price = total_price
        self.status = status  # 'pending', 'completed'

    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_orders(cls):
        return FileHandler.read(cls.FILE_PATH)

    @classmethod
    def add_order(cls, order_data):
        orders = cls.get_orders()
        orders.append(order_data)
        FileHandler.write(cls.FILE_PATH, orders)