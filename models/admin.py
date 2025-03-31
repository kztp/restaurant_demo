from models.user import User
from models.staff import Staff
from utils.file_handler import FileHandler
from models.item import Item

class Admin(User):
    """Admin class."""
    
    def __init__(self, name : str, email : str, password : str, role = "admin"):
        super().__init__(name, email, password)
        self.role = "admin"
    
    
    def to_dict(self):
        return {
            **super().to_dict(),
            "role": self.role
            }
    

    def add_staff(self, name : str, email : str, password : str):
        """Add staff to the staff list."""
        db = "db/staff.json"
        staff_all = FileHandler.read(db)
        for staff in staff_all:
            if staff["email"] == email:
                return False
            
        new_staff = Staff(name, email, password)
        staff_all.append(new_staff.to_dict())
        FileHandler.write(db, staff_all)
        return True


    def remove_staff(self, email : str):
        """Remove staff from the staff list."""
        db = "db/staff.json"
        staff_all = FileHandler.read(db)
        for i, s in enumerate(staff_all):
            if s["email"] == email:
                del staff_all[i]
                FileHandler.write(db, staff_all)
                return True
        return False
    

    def search_staff(self, email : str):
        """Search staff by email."""
        db = "db/staff.json"
        staff_all = FileHandler.read(db)
        for staff in staff_all:
            if staff["email"] == email:
                return Staff(**staff)
        return None
    

    def add_timetable(self, staff_email : str, timetable : dict):
        """Add timetable to staff."""
        db = "db/staff.json"
        staff_all = FileHandler.read(db)
        for i, s in enumerate(staff_all):
            if s["email"] == staff_email:
                staff_all[i]["timetable"] = timetable
                FileHandler.write(db, staff_all)
                return True
        return False
    
    def add_menu(self, name : str , price : int , stock : int):
        """Add menu items"""
        db = "db/menu.json"
        menu_all = FileHandler.read(db)
        for menu in menu_all:
            if menu["name"] == name:
                return False

        new_menu = Item(name, price, stock)
        new_menu = new_menu.to_dict()
        menu_all.append(new_menu)
        FileHandler.write(db, menu_all)
        return True

    def remove_menu(self, name : str):
        """Remove menu items"""
        db = "db/menu.json"
        menu_all = FileHandler.read(db)
        for i, s in enumerate(menu_all):
            if s["name"] == name:
                del menu_all[i]
                FileHandler.write(db, menu_all)
                return True
        return False


    def add_promo(self, item_name : str, promo : int):
        """Add the promo of the item"""
        db = "db/menu.json"
        menu_all = FileHandler.read(db)
        for i, s in enumerate(menu_all):
            if s["name"] == item_name:
                menu_all[i]["promo"] = promo
                FileHandler.write(db, menu_all)
                return True
        return False
