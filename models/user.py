class User:   

    def __init__(self, name : str, email : str, password : str):
        self.name = name
        self.email = email
        self.password = password


    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            }
    

    def verify_password(self, password : str) -> bool:
        """Verify the entered password."""
        return self.password == password


    def change_password(self, old_password : str, new_password : str) -> bool:
        """Change the password."""
        if self.verify_password(old_password):
            self.password = new_password
            return True
        return False
    
    def get_email(self):
        """Return the name of the email."""
        return self.email