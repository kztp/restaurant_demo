from flask import Flask
from controllers.user_controller import user_bp
from controllers.item_controller import item_bp
from controllers.order_controller import order_bp
from controllers.customer_controller import customer_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(item_bp, url_prefix="/api")
app.register_blueprint(order_bp, url_prefix="/api")
app.register_blueprint(customer_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)