import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os

LIVE_ORDERS_FILE = "live_orders.json"
REALTIME_ANALYTICS_FILE = "realtime_analytics.json"

class RealTimeOrderTracker:
    def __init__(self):
        self.orders_file = LIVE_ORDERS_FILE
        self.analytics_file = REALTIME_ANALYTICS_FILE
        self.ensure_files_exist()
    
    def ensure_files_exist(self):
        if not os.path.exists(self.orders_file):
            with open(self.orders_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.analytics_file):
            initial_analytics = {
                "hourly_stats": {},
                "daily_revenue": 0,
                "popular_items": {},
                "payment_methods": {},
                "customer_segments": {},
                "last_updated": datetime.now().isoformat()
            }
            with open(self.analytics_file, 'w') as f:
                json.dump(initial_analytics, f, indent=2)
    
    def add_order(self, order_data):
        """Add a new real-time order and update analytics"""
        # Load existing orders
        with open(self.orders_file, 'r') as f:
            orders = json.load(f)
        
        # Add new order with timestamp
        order_data['order_id'] = len(orders) + 1
        order_data['timestamp'] = datetime.now().isoformat()
        order_data['status'] = 'Preparing'
        
        orders.append(order_data)
        
        # Save updated orders
        with open(self.orders_file, 'w') as f:
            json.dump(orders, f, indent=2)
        
        # Update real-time analytics
        self.update_analytics(order_data)
        
        return order_data['order_id']
    
    def update_analytics(self, new_order):
        """Update real-time analytics with new order"""
        with open(self.analytics_file, 'r') as f:
            analytics = json.load(f)
        
        current_hour = datetime.now().strftime("%Y-%m-%d-%H")
        
        # Update hourly stats
        if current_hour not in analytics["hourly_stats"]:
            analytics["hourly_stats"][current_hour] = {
                "orders_count": 0,
                "revenue": 0,
                "items": {}
            }
        
        analytics["hourly_stats"][current_hour]["orders_count"] += 1
        analytics["hourly_stats"][current_hour]["revenue"] += new_order["amount"]
        
        # Update popular items
        item = new_order.get("food_item", new_order.get("meal", "Unknown"))
        if item not in analytics["popular_items"]:
            analytics["popular_items"][item] = 0
        analytics["popular_items"][item] += 1
        
        # Update payment methods
        payment = new_order.get("payment_method", "Unknown")
        if payment not in analytics["payment_methods"]:
            analytics["payment_methods"][payment] = 0
        analytics["payment_methods"][payment] += 1
        
        # Update daily revenue
        analytics["daily_revenue"] += new_order["amount"]
        
        # Update last updated timestamp
        analytics["last_updated"] = datetime.now().isoformat()
        
        # Save updated analytics
        with open(self.analytics_file, 'w') as f:
            json.dump(analytics, f, indent=2)
    
    def get_live_orders_df(self):
        """Get all live orders as DataFrame"""
        try:
            with open(self.orders_file, 'r') as f:
                orders = json.load(f)
            
            if orders:
                df = pd.DataFrame(orders)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
            else:
                return pd.DataFrame()
        except:
            return pd.DataFrame()
    
    def get_today_orders(self):
        """Get today's orders only"""
        df = self.get_live_orders_df()
        if not df.empty:
            today = datetime.now().date()
            df['order_date'] = df['timestamp'].dt.date
            return df[df['order_date'] == today]
        return pd.DataFrame()
    
    def get_realtime_analytics(self):
        """Get real-time analytics data"""
        try:
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def get_hourly_trends(self):
        """Get hourly order trends for the last 24 hours"""
        analytics = self.get_realtime_analytics()
        hourly_stats = analytics.get("hourly_stats", {})
        
        # Get last 24 hours
        now = datetime.now()
        last_24_hours = []
        
        for i in range(24):
            hour_key = (now - timedelta(hours=i)).strftime("%Y-%m-%d-%H")
            stats = hourly_stats.get(hour_key, {"orders_count": 0, "revenue": 0})
            last_24_hours.append({
                "hour": hour_key,
                "orders": stats["orders_count"],
                "revenue": stats["revenue"]
            })
        
        return pd.DataFrame(last_24_hours[::-1])  # Reverse to show chronologically
    
    def clear_orders(self):
        """Clear all orders (for testing)"""
        with open(self.orders_file, 'w') as f:
            json.dump([], f)
        
        initial_analytics = {
            "hourly_stats": {},
            "daily_revenue": 0,
            "popular_items": {},
            "payment_methods": {},
            "customer_segments": {},
            "last_updated": datetime.now().isoformat()
        }
        with open(self.analytics_file, 'w') as f:
            json.dump(initial_analytics, f, indent=2)
    
    def simulate_realtime_orders(self, count=10):
        """Simulate real-time orders for testing"""
        meals = ['Pizza Margherita', 'Burger Deluxe', 'Pasta Alfredo', 'Caesar Salad', 
                'Fish Curry', 'Chicken Biryani', 'Paneer Tikka', 'Veggie Wrap']
        
        customers = [f'Customer_{i}' for i in range(101, 151)]
        payment_methods = ['Card', 'UPI', 'Cash', 'Wallet']
        
        for i in range(count):
            order = {
                "customer_name": np.random.choice(customers),
                "food_item": np.random.choice(meals),
                "meal": np.random.choice(meals),
                "amount": np.random.randint(150, 600),
                "payment_method": np.random.choice(payment_methods),
                "order_date": datetime.now().date().isoformat()
            }
            self.add_order(order)
        
        return f"Added {count} simulated real-time orders"

# Global tracker instance
tracker = RealTimeOrderTracker()

# Legacy functions for backward compatibility
def get_live_orders_df():
    return tracker.get_live_orders_df()

def get_today_orders():
    return tracker.get_today_orders()

def clear_orders():
    return tracker.clear_orders()

def add_live_order(order_data):
    return tracker.add_order(order_data)

def get_realtime_analytics():
    return tracker.get_realtime_analytics()
