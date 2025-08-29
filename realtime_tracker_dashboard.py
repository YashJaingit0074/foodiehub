import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime, timedelta
from models.realtime_tracker import tracker, RealTimeOrderTracker
import time

# Set page configuration
st.set_page_config(
    page_title="Real-Time Order Tracker",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for real-time dashboard
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        font-family: 'Arial', sans-serif;
    }
    .stApp header {
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
        height: 4rem;
    }
    .realtime-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid #ff6b6b;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3); }
        50% { box-shadow: 0 12px 48px rgba(255, 107, 107, 0.5); }
        100% { box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3); }
    }
    .tracker-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    .live-metric {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .status-active {
        color: #2ed573;
        font-weight: bold;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        50% { opacity: 0.5; }
    }
    h1, h2, h3 {
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stButton button {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Real-Time Tracker Header
st.markdown("""
<div class="realtime-header">
    <h1 style="color: white; margin: 0;">🔴 REAL-TIME ORDER TRACKER</h1>
    <p style="color: white; margin: 5px 0 0 0;">Live Order Monitoring & Analytics System</p>
    <p class="status-active" style="margin: 10px 0 0 0;">● LIVE TRACKING ACTIVE</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.title('🔴 Real-Time Controls')

# Auto-refresh with countdown
auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 60, 15)

if auto_refresh:
    st.sidebar.success("🔴 LIVE MODE ON")
    # Create countdown display
    countdown_placeholder = st.sidebar.empty()
    for i in range(refresh_interval, 0, -1):
        countdown_placeholder.info(f"⏰ Next refresh: {i}s")
        time.sleep(1)
    countdown_placeholder.success("🔄 Refreshing...")
    st.rerun()

# Manual controls
st.sidebar.markdown("---")
st.sidebar.subheader("🎮 Manual Controls")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🎲 +10 Orders"):
        result = tracker.simulate_realtime_orders(10)
        st.sidebar.success(result)
        st.rerun()

with col2:
    if st.button("🎲 +5 Orders"):
        result = tracker.simulate_realtime_orders(5)
        st.sidebar.success(result)
        st.rerun()

if st.sidebar.button("🧹 Clear All Data", type="secondary"):
    tracker.clear_orders()
    st.sidebar.warning("All data cleared!")
    st.rerun()

# Display current time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.markdown(f"**🕒 Current Time:** {current_time}")

# Main dashboard content
st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
st.subheader('📊 LIVE TRACKING DASHBOARD')

# Get real-time data
live_orders = tracker.get_live_orders_df()
today_orders = tracker.get_today_orders()
analytics_data = tracker.get_realtime_analytics()
hourly_trends = tracker.get_hourly_trends()

# Real-time metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_live = len(live_orders)
    st.markdown(f"""
    <div class="live-metric">
        <h4>📱 TOTAL ORDERS</h4>
        <h2>{total_live}</h2>
        <p>All time</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    today_count = len(today_orders)
    st.markdown(f"""
    <div class="live-metric">
        <h4>🔴 TODAY'S ORDERS</h4>
        <h2>{today_count}</h2>
        <p>Live today</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    daily_revenue = analytics_data.get('daily_revenue', 0)
    st.markdown(f"""
    <div class="live-metric">
        <h4>💰 TODAY'S REVENUE</h4>
        <h2>₹{daily_revenue:,.0f}</h2>
        <p>Live earnings</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_order = (daily_revenue / today_count) if today_count > 0 else 0
    st.markdown(f"""
    <div class="live-metric">
        <h4>📈 AVG ORDER</h4>
        <h2>₹{avg_order:.0f}</h2>
        <p>Today's average</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    last_updated = analytics_data.get('last_updated', 'Never')
    if last_updated != 'Never':
        last_updated_dt = datetime.fromisoformat(last_updated)
        time_diff = datetime.now() - last_updated_dt
        seconds_ago = int(time_diff.total_seconds())
        update_text = f"{seconds_ago}s ago"
    else:
        update_text = "Never"
    
    st.markdown(f"""
    <div class="live-metric">
        <h4>🔄 LAST UPDATE</h4>
        <h2 class="status-active">{update_text}</h2>
        <p>Data freshness</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Live data visualizations
if not live_orders.empty:
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔴 Live Popular Items")
        popular_items = analytics_data.get('popular_items', {})
        if popular_items:
            items_df = pd.DataFrame(list(popular_items.items()), columns=['Item', 'Orders'])
            items_df = items_df.sort_values('Orders', ascending=False).head(8)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(items_df['Item'][::-1], items_df['Orders'][::-1], 
                          color=['#ff6b6b', '#ee5a24', '#ff7675', '#fdcb6e', '#6c5ce7', '#a29bfe', '#fd79a8', '#e84393'])
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            ax.tick_params(colors='white')
            ax.set_xlabel('Live Orders', color='white', fontweight='bold')
            ax.set_title('🔴 Real-Time Popular Items', color='white', fontsize=14, fontweight='bold')
            
            # Add value labels on bars
            for bar, value in zip(bars, items_df['Orders'][::-1]):
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                       str(int(value)), va='center', color='white', fontweight='bold')
            
            st.pyplot(fig)
        else:
            st.info("📱 No orders yet. Use the simulation buttons to generate data!")
    
    with col2:
        st.subheader("💳 Real-Time Payments")
        payment_methods = analytics_data.get('payment_methods', {})
        if payment_methods:
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = ['#ff6b6b', '#ee5a24', '#fdcb6e', '#6c5ce7']
            wedges, texts, autotexts = ax.pie(payment_methods.values(), 
                                            labels=payment_methods.keys(), 
                                            autopct='%1.1f%%', 
                                            colors=colors,
                                            explode=[0.05]*len(payment_methods))
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            plt.title('🔴 Live Payment Methods', color='white', fontsize=14, fontweight='bold')
            
            # Style text
            for text in texts:
                text.set_color('white')
                text.set_fontweight('bold')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            st.pyplot(fig)
        else:
            st.info("💳 No payment data yet!")
    
    # Hourly trends
    if not hourly_trends.empty and hourly_trends['orders'].sum() > 0:
        st.subheader("📊 24-Hour Real-Time Trends")
        
        fig, ax1 = plt.subplots(figsize=(14, 8))
        
        # Plot orders
        color1 = '#ff6b6b'
        ax1.set_xlabel('Hour (Last 24h)', color='white', fontweight='bold')
        ax1.set_ylabel('Orders', color=color1, fontweight='bold')
        line1 = ax1.plot(range(len(hourly_trends)), hourly_trends['orders'], 
                        color=color1, linewidth=3, marker='o', markersize=8, label='Orders')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.tick_params(axis='x', colors='white')
        
        # Plot revenue on secondary axis
        ax2 = ax1.twinx()
        color2 = '#fdcb6e'
        ax2.set_ylabel('Revenue (₹)', color=color2, fontweight='bold')
        line2 = ax2.plot(range(len(hourly_trends)), hourly_trends['revenue'], 
                        color=color2, linewidth=2, marker='s', markersize=6, label='Revenue')
        ax2.tick_params(axis='y', labelcolor=color2)
        
        # Styling
        ax1.set_facecolor('none')
        ax2.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax1.grid(True, alpha=0.3)
        ax1.set_title('🔴 Real-Time 24-Hour Order & Revenue Trends', 
                     color='white', fontsize=16, fontweight='bold', pad=20)
        
        # Legend
        lines = line1 + line2
        labels = ['Orders', 'Revenue']
        ax1.legend(lines, labels, loc='upper left', framealpha=0.8)
        
        st.pyplot(fig)
    
    # Live orders table
    st.subheader("📋 Live Orders Table")
    if not today_orders.empty:
        display_orders = today_orders[['order_id', 'customer_name', 'food_item', 'amount', 'payment_method', 'status', 'timestamp']].copy()
        display_orders['timestamp'] = display_orders['timestamp'].dt.strftime('%H:%M:%S')
        display_orders = display_orders.sort_values('order_id', ascending=False)
        
        # Color code by status
        st.dataframe(
            display_orders,
            use_container_width=True,
            hide_index=True
        )
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            preparing = len(today_orders[today_orders.get('status', 'Delivered') == 'Preparing'])
            st.metric("🍳 Preparing", preparing)
        with col2:
            ready = len(today_orders[today_orders.get('status', 'Delivered') == 'Ready'])
            st.metric("✅ Ready", ready)
        with col3:
            in_progress = len(today_orders[today_orders.get('status', 'Delivered') == 'In Progress'])
            st.metric("🔄 In Progress", in_progress)
        with col4:
            delivered = len(today_orders[today_orders.get('status', 'Delivered') == 'Delivered'])
            st.metric("🚚 Delivered", delivered)
    else:
        st.info("📱 No orders today yet. Use the simulation buttons to generate test data!")

else:
    # No data state
    st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
    st.subheader("🚀 Welcome to Real-Time Order Tracker")
    st.info("""
    **Getting Started:**
    1. Use the **🎲 +10 Orders** or **🎲 +5 Orders** buttons to generate test data
    2. Enable **🔄 Auto Refresh** to see live updates
    3. Watch the dashboard update in real-time!
    
    **Features:**
    - Live order tracking with timestamps
    - Real-time analytics and charts
    - 24-hour trend analysis
    - Auto-refresh functionality
    - Order status monitoring
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with system info
st.markdown("---")
st.markdown(f"""
**🔴 Real-Time System Status:**
- **Tracking Active**: ✅ Live monitoring enabled
- **Data Points**: {len(live_orders)} total orders tracked
- **Today's Activity**: {len(today_orders)} orders placed
- **Last Analytics Update**: {analytics_data.get('last_updated', 'Never')[:19] if analytics_data.get('last_updated', 'Never') != 'Never' else 'Never'}
- **System Time**: {current_time}
""")
