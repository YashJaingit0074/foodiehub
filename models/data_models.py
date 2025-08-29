import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Sample order data with more realistic dataset
def load_orders():
    np.random.seed(42)
    
    meals = ['Pizza', 'Burger', 'Salad', 'Pasta', 'Sandwich', 'Rice Bowl', 'Noodles', 'Biryani']
    payment_methods = ['Card', 'UPI', 'Cash', 'Wallet']
    
    # Generate more orders for better real-time analysis - increasing from 50 to 500
    n_orders = 500
    
    # Create more realistic data spread across different time periods
    np.random.seed(42)
    
    return pd.DataFrame({
        'order_id': range(1, n_orders + 1),
        'customer_name': [f'Customer_{i}' for i in np.random.randint(101, 200, n_orders)],
        'user_id': np.random.randint(101, 200, n_orders),
        'food_item': np.random.choice(meals, n_orders, p=[0.25, 0.20, 0.10, 0.15, 0.10, 0.08, 0.07, 0.05]),
        'meal': np.random.choice(meals, n_orders, p=[0.25, 0.20, 0.10, 0.15, 0.10, 0.08, 0.07, 0.05]),
        'amount': np.random.randint(120, 650, n_orders),
        'payment_method': np.random.choice(payment_methods, n_orders, p=[0.4, 0.35, 0.15, 0.10]),
        'order_date': pd.date_range('2025-08-01', periods=n_orders, freq='2h').date,
        'timestamp': pd.date_range('2025-08-01', periods=n_orders, freq='2h'),
        'status': np.random.choice(['Delivered', 'In Progress', 'Preparing', 'Ready'], n_orders, p=[0.7, 0.15, 0.10, 0.05])
    })

# Sample feedback data with more variety
def load_feedback():
    np.random.seed(42)
    
    comments = [
        'Excellent food!', 'Very tasty!', 'Good quality', 'Average taste',
        'Could be better', 'Loved it!', 'Fresh and hot', 'Quick delivery',
        'Great experience', 'Will order again', 'Not bad', 'Decent meal'
    ]
    
    n_feedback = 45  # Not all orders have feedback
    
    return pd.DataFrame({
        'feedback_id': range(1, n_feedback + 1),
        'order_id': range(1, n_feedback + 1),
        'rating': np.random.choice([3, 4, 5], n_feedback, p=[0.2, 0.4, 0.4]),
        'comment': np.random.choice(comments, n_feedback)
    })
