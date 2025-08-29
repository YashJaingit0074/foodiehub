import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
from datetime import datetime, timedelta
from models.data_models import load_orders, load_feedback
from models.analysis import analyze_order_trends, analyze_payment_patterns, feedback_analysis
from models.live_orders import get_live_orders_df, get_today_orders, clear_orders

# Set page configuration with custom theme
st.set_page_config(
    page_title="Meal Orders Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the dashboard appearance
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        font-family: 'Arial', sans-serif;
    }
    .stApp header {
        background: linear-gradient(90deg, #4a55a2, #2c3e94);
        height: 4rem;
    }
    .block-container {
        padding: 2rem 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    .analytics-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid #4facfe;
        box-shadow: 0 8px 32px rgba(79, 172, 254, 0.3);
    }
    .analytics-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    .metric-analytics {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .analytics-info {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        color: #333;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    h1, h2, h3 {
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.15);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stButton button {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
    }
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)
# Analytics Dashboard Header
st.markdown("""
<div class="analytics-header">
    <h1 style="color: white; margin: 0;">📊 ANALYTICS DASHBOARD</h1>
    <p style="color: white; margin: 5px 0 0 0;">Business Intelligence & Data Insights</p>
    <div class="analytics-info" style="margin-top: 1rem;">
        📈 Real-time Data Analysis & Performance Metrics
    </div>
</div>
""", unsafe_allow_html=True)
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Add refresh button at the top
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
with col2:
    if st.button("🗑️ Clear Live Orders", use_container_width=True):
        clear_orders()
        st.success("🗑️ All live orders cleared!")
        st.rerun()
with col3:
    st.metric("🔄 Status", "Ready", help="System ready for testing")

st.markdown("<div style='text-align: center;'><h1 style='color: #4a55a2;'>🍽️ Meal Orders & Feedback Analytics</h1></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])
with col_left:
    st.markdown("""
    <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h3 style='color: #4a55a2;'>Welcome to Your Data Analytics Dashboard</h3>
        <p>This interactive dashboard provides powerful insights into meal orders and customer feedback. 
        Explore the visualizations to understand trends, patterns, and customer preferences.</p>
    </div>
    """, unsafe_allow_html=True)
    
with col_right:
    st.markdown("""
    <div style='background-color: #4a55a2; color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h3 style='color: white;'>Dashboard Highlights</h3>
        <ul>
            <li>Real-time order tracking</li>
            <li>Customer feedback analysis</li>
            <li>Payment pattern insights</li>
            <li>Data-driven meal planning</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# Load data
orders = load_orders()
feedback = load_feedback()

# Load live orders from user panel
try:
    live_orders = get_live_orders_df()
    today_orders = get_today_orders()
except Exception as e:
    live_orders = pd.DataFrame()
    today_orders = pd.DataFrame()

# Combine sample data with live orders for comprehensive analytics
if not live_orders.empty:
    combined_orders = pd.concat([orders, live_orders], ignore_index=True)
else:
    combined_orders = orders

# Show summary cards with simple explanations
st.header('📊 Quick Summary')

col1, col2, col3 = st.columns(3)

total_orders = len(combined_orders)
total_payments = combined_orders['amount'].sum() if len(combined_orders) > 0 and 'amount' in combined_orders.columns else 0
avg_rating = feedback['rating'].mean() if len(feedback) > 0 and 'rating' in feedback.columns else 0

col1.metric('Total Orders', total_orders, help='How many meals have been ordered so far')
col2.metric('Total Payments', f"₹{total_payments:,.2f}", help='Total money received from orders')
col3.metric('Average Rating', f"{avg_rating:.2f}", help='Average customer rating for meals')

# Show today's live orders if any
if not today_orders.empty:
    st.markdown("""
    <div class="live-update">
        <h3 style="margin: 0; color: white;">🔴 LIVE: Real Orders from User Panel!</h3>
        <p style="margin: 5px 0; color: white;">Orders placed through the FoodieHub customer interface</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader(f'📱 {len(today_orders)} Live Orders Today')
    
    # Group by order_id to show complete orders
    order_groups = today_orders.groupby('order_id').first().reset_index()
    
    for _, order in order_groups.iterrows():
        order_items = today_orders[today_orders['order_id'] == order['order_id']]
        
        with st.expander(f"🍽️ Order #{order['order_id']} - {order['user_name']} - ₹{order_items['amount'].sum():.0f}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**📋 Items Ordered:**")
                for _, item in order_items.iterrows():
                    st.write(f"• {item['meal']} - ₹{item['amount']}")
                
                st.write(f"**👤 Customer:** {order['user_name']}")
                st.write(f"**⏰ Time:** {order['timestamp'].strftime('%H:%M:%S')}")
                st.write(f"**💳 Payment:** {order['payment_method']}")
            
            with col2:
                st.metric("Order Value", f"₹{order_items['amount'].sum():.0f}")
                st.write("**Status:** ✅ Confirmed")
    
    # Today's stats
    col1, col2, col3 = st.columns(3)
    col1.metric("📱 Live Orders Today", len(today_orders))
    col2.metric("💰 Today's Revenue", f"₹{today_orders['amount'].sum():.0f}")
    col3.metric("🎯 Avg Order Value", f"₹{today_orders['amount'].mean():.0f}")
else:
    st.info("🛒 No live orders yet today. Place orders through the User Panel to see them here!")
    st.markdown("""
    **To see live integration:**
    1. Use the 🍕 Customer Panel button below to place orders
    2. Orders will instantly appear in this dashboard!
    3. Try different items and see real-time analytics!
    """)

st.markdown('---')

st.header('📈 Order Trends')
st.write('See how meal orders change over time. This helps spot busy days and plan ahead!')
order_trends = analyze_order_trends(combined_orders)

# Create a colorful bar chart using matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
bars = ax.bar(order_trends.index, order_trends.values, color=colors[:len(order_trends)])
ax.set_title('Most Popular Meals', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Meals', fontsize=10)
ax.set_ylabel('Orders', fontsize=10)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.xticks(rotation=45, fontsize=9)
plt.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close()

st.markdown('---')

st.header('💸 Payment Patterns')
st.write('Check how customers pay for their meals. Spot popular payment methods and trends!')
payment_patterns = analyze_payment_patterns(combined_orders)

col1, col2 = st.columns(2)

with col1:
    # Create a pie chart for payment methods
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFD700']
    wedges, texts, autotexts = ax.pie(payment_patterns.values, labels=payment_patterns.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90,
                                      explode=(0.02, 0.02, 0.02, 0.02))

    # Enhance text styling
    for text in texts:
        text.set_fontsize(10)
        text.set_fontweight('bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)

    ax.set_title('Payment Methods', fontsize=12, fontweight='bold', pad=15)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col2:
    # Add a horizontal bar chart for payment amounts
    st.subheader('💰 Revenue by Method')
    payment_amounts = combined_orders.groupby('payment_method')['amount'].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(5, 3))
    bars = ax.barh(payment_amounts.index, payment_amounts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax.set_title('Total Revenue', fontsize=11, fontweight='bold')
    ax.set_xlabel('Amount (₹)', fontsize=9)

    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 50, bar.get_y() + bar.get_height()/2., 
                f'₹{int(width/1000)}K', ha='left', va='center', fontweight='bold', fontsize=8)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

st.markdown('---')

st.header('⭐ Top-Rated Meals')
st.write('Find out which meals customers love the most!')
top_meals = feedback_analysis(feedback, orders)

# Create an attractive table with styling
col1, col2 = st.columns([3, 2])

with col1:
    # Convert to DataFrame for better display
    top_meals_df = pd.DataFrame({
        'Meal': top_meals.index,
        'Avg Rating': top_meals.values.round(2),
        'Stars': ['⭐' * int(rating) for rating in top_meals.values]
    }).reset_index(drop=True)
    
    st.dataframe(top_meals_df, use_container_width=True, hide_index=True)

with col2:
    # Add a rating distribution chart
    rating_counts = feedback['rating'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(4, 3))
    colors = ['#FF6B6B', '#FFD93D', '#6BCF7F']
    bars = ax.bar(rating_counts.index, rating_counts.values, color=colors)
    ax.set_title('Rating Distribution', fontsize=11, fontweight='bold')
    ax.set_xlabel('Stars', fontsize=9)
    ax.set_ylabel('Count', fontsize=9)
    ax.set_xticks(rating_counts.index)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

st.markdown('---')

# Add a simple tip for users
st.info('Tip: Click and drag on charts to zoom in, or use the sidebar to filter data if available.')

# Add a friendly closing message
st.success('This dashboard makes it easy for anyone to understand meal orders and feedback. If you have questions, just ask!')

st.success('Demonstrates real-time analytics and actionable insights for data-driven decision making.')

# Admin access section
st.markdown("---")
st.subheader("🚀 Access Different Panels")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background-color: #4ecdc4; color: white; padding: 20px; border-radius: 15px; text-align: center;'>
        <h4 style='color: white; margin: 0;'>🍕 User Panel</h4>
        <p style='margin: 10px 0;'>Order food, leave reviews</p>
        <p style='margin: 0; font-size: 0.9em;'>Customer Experience</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("🍕 Open User Panel", "http://localhost:8508", use_container_width=True)

with col2:
    st.markdown("""
    <div style='background-color: #45b7d1; color: white; padding: 20px; border-radius: 15px; text-align: center;'>
        <h4 style='color: white; margin: 0;'>� Analytics Dashboard</h4>
        <p style='margin: 10px 0;'>Business insights & data</p>
        <p style='margin: 0; font-size: 0.9em;'>Current Page</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("✅ You are currently here!")

with col3:
    st.markdown("""
    <div style='background-color: #ff6b6b; color: white; padding: 20px; border-radius: 15px; text-align: center;'>
        <h4 style='color: white; margin: 0;'>🔐 Admin Panel</h4>
        <p style='margin: 10px 0;'>Restaurant management</p>
        <p style='margin: 0; font-size: 0.9em;'>Password: admin123</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("🔐 Open Admin Panel", "http://localhost:8503", use_container_width=True)
