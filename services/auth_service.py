from app.models.user import User

def register_user(email, password, role='customer'):
    return User.register_user(email, password, role)

def login_user(email, password):
    user = User.get_user_by_email(email)
    if user and user['password'] == password:
        return user
    return None