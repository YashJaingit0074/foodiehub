import pandas as pd
from .data_models import load_orders, load_feedback

def analyze_order_trends(orders):
    return orders.groupby('meal').size().sort_values(ascending=False)

def analyze_payment_patterns(orders):
    return orders['payment_method'].value_counts()

def feedback_analysis(feedback, orders):
    merged = pd.merge(feedback, orders, on='order_id')
    top_meals = merged.groupby('meal')['rating'].mean().sort_values(ascending=False)
    return top_meals
