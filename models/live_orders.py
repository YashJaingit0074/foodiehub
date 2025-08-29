import json
import os
from datetime import datetime
import pandas as pd

# File to store orders
ORDERS_FILE = "live_orders.json"

def save_order(order_data):
    """Save a new order to the JSON file"""
    orders = load_live_orders()
    
    # Add timestamp and order ID
    order_data['order_id'] = len(orders) + 1
    order_data['timestamp'] = datetime.now().isoformat()
    order_data['status'] = 'Placed'
    
    orders.append(order_data)
    
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)
    
    return order_data['order_id']

def load_live_orders():
    """Load all live orders from JSON file"""
    if not os.path.exists(ORDERS_FILE):
        return []
    
    try:
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def get_live_orders_df():
    """Convert live orders to pandas DataFrame for analytics"""
    orders = load_live_orders()
    
    if not orders:
        return pd.DataFrame()
    
    # Flatten the data for analytics
    flattened_orders = []
    for order in orders:
        for item in order.get('items', []):
            flattened_orders.append({
                'order_id': order['order_id'],
                'user_name': order['user_name'],
                'meal': item['name'],
                'amount': item['total'],
                'payment_method': order.get('payment_method', 'Not specified'),
                'timestamp': pd.to_datetime(order['timestamp']),
                'status': order['status']
            })
    
    return pd.DataFrame(flattened_orders)

def get_today_orders():
    """Get orders placed today"""
    df = get_live_orders_df()
    if df.empty:
        return df
    
    today = datetime.now().date()
    return df[df['timestamp'].dt.date == today]

def clear_orders():
    """Clear all orders (for testing)"""
    if os.path.exists(ORDERS_FILE):
        os.remove(ORDERS_FILE)
        return True
    return False

# Clear orders on import for fresh start
clear_orders()
