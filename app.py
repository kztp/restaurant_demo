from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.index_controller import index_bp
from controllers.customer_controller import customer_bp
from controllers.staff_controller import staff_bp
from controllers.owner_controller import owner_bp
from controllers.admin_controller import admin_bp
#from controllers.customer_controller import customer_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(index_bp)
app.register_blueprint(auth_bp, url_prefix  ="/auth")
app.register_blueprint(customer_bp, url_prefix  = "/customer")
app.register_blueprint(staff_bp, url_prefix  = "/staff")
app.register_blueprint(owner_bp, url_prefix="/owner")
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)