from models.user import User
from utils.file_handler import FileHandler
from models.item import Item

class Staff(User):
    """Staff class."""
    
    def __init__(self, name : str, email : str, password : str, role = "staff", timetable = []):
        super().__init__(name, email, password)
        self.role = "staff"
        self.timetable = []

    def to_dict(self):
        return {
            **super().to_dict(),
            "role": self.role,
            "timetable": self.timetable
            }

    def show_timetable(self):
        """view timetable list"""
        return self.timetable

    def manage_table(self, table_id : int, status : str):
        """Mangae tables in the table pool."""
        db = "db/tables.json"
        tables = FileHandler.read(db)
        for table in tables:
            if table["table_id"] == table_id:
                if table["status"] != status:
                    table["status"] = status
                    FileHandler.write(db, tables)
                    return True
        return False


    def add_stock(self, item : Item , quantity : int):
        """Increase stock quantity."""
        return item.add_stock(quantity)
    

    def do_order(self):
        """change the status of order and transfer completed order to finished order list."""
        db_todo = "db/orders.json"
        db_finished = "db/orders_finished.json"

        orders_todo = FileHandler.read(db_todo)
        orders_finished = FileHandler.read(db_finished)

        new_order = orders_todo[0]
        new_orders_todo = orders_todo[1:]

        FileHandler.write(db_todo, new_orders_todo)

        new_order["status"] = "done" 
        orders_finished.append(new_order)
        FileHandler.write(db_finished, orders_finished)
        return True

