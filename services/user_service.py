from utils.file_handler import FileHandler

def get_all_users(db : str):
    """Retrieve all users from the json file"""
    return FileHandler.read(db)

def get_customer_by_email(email : str):
    """Find a user by email"""
    db = "db/customer.json"
    user_all = FileHandler.read(db)
    for user in user_all:
        if user["email"] == email:
            return user
    return None

def register_customer(customer):
    """Register customer in db"""
    db = "db/customer.json"
    customer_all = FileHandler.read(db)
    customer_all.append(customer)
    FileHandler.write(db, customer_all)
    return True