from app.models.order import Order

def create_order(user_id, menu_item_id, quantity):
    return Order.create_order(user_id, menu_item_id, quantity)