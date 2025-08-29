import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from models.data_models import load_orders, load_feedback
from models.analysis import analyze_order_trends, analyze_payment_patterns, feedback_analysis
from models.live_orders import get_live_orders_df, get_today_orders, clear_orders
from models.realtime_tracker import tracker, get_realtime_analytics

# Set page configuration with custom theme
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
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
    .realtime-card {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.2), rgba(0, 242, 254, 0.2));
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #4facfe;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(79, 172, 254, 0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 4px 16px rgba(79, 172, 254, 0.3); }
        50% { box-shadow: 0 8px 24px rgba(79, 172, 254, 0.5); }
        100% { box-shadow: 0 4px 16px rgba(79, 172, 254, 0.3); }
    }
    .metric-realtime {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4);
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
</style>
""", unsafe_allow_html=True)

# Analytics Dashboard Header
st.markdown("""
<div class="analytics-header">
    <h1 style="color: white; margin: 0;">📊 REAL-TIME ANALYTICS DASHBOARD</h1>
    <p style="color: white; margin: 5px 0 0 0;">Live Order Tracking & Business Intelligence</p>
    <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">🔴 LIVE • Updated every second</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with auto-refresh
st.sidebar.title('📊 Real-Time Controls')

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh (30s)", value=False)
if auto_refresh:
    st.sidebar.success("🔴 LIVE MODE ACTIVE")
    import time
    # Auto refresh every 30 seconds with countdown
    for i in range(30, 0, -1):
        placeholder = st.sidebar.empty()
        placeholder.info(f"⏰ Refresh in: {i}s")
        time.sleep(1)
    placeholder.success("🔄 Refreshing...")
    st.rerun()

selected_analysis = st.sidebar.selectbox('Choose Analysis', 
    ['🔴 Live Dashboard', '📈 Order Trends', '💳 Payment Analysis', '📝 Customer Feedback', '🎯 Real-Time Orders'])

# Simulation controls
st.sidebar.markdown("---")
st.sidebar.subheader("🧪 Testing Tools")

if st.sidebar.button("🎲 Simulate 10 Orders"):
    result = tracker.simulate_realtime_orders(10)
    st.sidebar.success(result)

if st.sidebar.button("🔄 Clear All Data"):
    clear_orders()
    st.sidebar.warning("All data cleared!")

# Load data
orders, feedback = load_orders(), load_feedback()
live_orders = get_live_orders_df()
today_orders = get_today_orders()
realtime_analytics = get_realtime_analytics()

if selected_analysis == '🔴 Live Dashboard':
    st.markdown('<div class="realtime-card">', unsafe_allow_html=True)
    st.subheader('🔴 LIVE DASHBOARD - Real-Time Tracking')
    
    # Real-time metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_orders = len(orders) + len(live_orders)
        st.markdown(f"""
        <div class="metric-realtime">
            <h4>📋 TOTAL ORDERS</h4>
            <h2>{total_orders:,}</h2>
            <p>Historical + Live</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        live_today = len(today_orders)
        st.markdown(f"""
        <div class="metric-realtime">
            <h4>🔴 TODAY'S ORDERS</h4>
            <h2>{live_today}</h2>
            <p>Live orders today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_revenue = orders['amount'].sum() + (today_orders['amount'].sum() if not today_orders.empty else 0)
        st.markdown(f"""
        <div class="metric-realtime">
            <h4>💰 TOTAL REVENUE</h4>
            <h2>₹{total_revenue:,.0f}</h2>
            <p>All time revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        daily_revenue = realtime_analytics.get('daily_revenue', 0)
        st.markdown(f"""
        <div class="metric-realtime">
            <h4>💳 TODAY'S REVENUE</h4>
            <h2>₹{daily_revenue:,.0f}</h2>
            <p>Real-time earnings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        avg_order = (total_revenue / total_orders) if total_orders > 0 else 0
        st.markdown(f"""
        <div class="metric-realtime">
            <h4>📈 AVG ORDER</h4>
            <h2>₹{avg_order:.0f}</h2>
            <p>Average order value</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Real-time charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔴 Live Popular Items")
        popular_items = realtime_analytics.get('popular_items', {})
        if popular_items:
            items_df = pd.DataFrame(list(popular_items.items()), columns=['Item', 'Orders'])
            items_df = items_df.sort_values('Orders', ascending=False).head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(items_df['Item'][::-1], items_df['Orders'][::-1], color='#4facfe')
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            ax.tick_params(colors='white')
            ax.set_xlabel('Live Orders Count', color='white', fontweight='bold')
            ax.set_title('🔴 Real-Time Popular Items', color='white', fontsize=14, fontweight='bold')
            st.pyplot(fig)
        else:
            st.info("📱 No live orders yet. Use 'Simulate Orders' to see real-time data!")
    
    with col2:
        st.subheader("💳 Real-Time Payment Methods")
        payment_methods = realtime_analytics.get('payment_methods', {})
        if payment_methods:
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = ['#4facfe', '#00f2fe', '#667eea', '#764ba2']
            wedges, texts, autotexts = ax.pie(payment_methods.values(), 
                                            labels=payment_methods.keys(), 
                                            autopct='%1.1f%%', 
                                            colors=colors)
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            plt.title('🔴 Live Payment Distribution', color='white', fontsize=14, fontweight='bold')
            
            # Make text white
            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            st.pyplot(fig)
        else:
            st.info("💳 No payment data yet. Place some orders to see payment analysis!")
    
    # Hourly trends
    st.subheader("📊 24-Hour Order Trends")
    hourly_trends = tracker.get_hourly_trends()
    
    if not hourly_trends.empty and hourly_trends['orders'].sum() > 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(range(len(hourly_trends)), hourly_trends['orders'], 
                color='#4facfe', linewidth=3, marker='o', markersize=6, label='Orders')
        ax2 = ax.twinx()
        ax2.plot(range(len(hourly_trends)), hourly_trends['revenue'], 
                color='#00f2fe', linewidth=2, marker='s', markersize=4, label='Revenue')
        
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax2.tick_params(colors='white')
        ax.set_xlabel('Hour (Last 24h)', color='white', fontweight='bold')
        ax.set_ylabel('Orders Count', color='white', fontweight='bold')
        ax2.set_ylabel('Revenue (₹)', color='white', fontweight='bold')
        ax.set_title('🔴 Real-Time 24-Hour Trends', color='white', fontsize=14, fontweight='bold')
        
        # Create legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        st.pyplot(fig)
    else:
        st.info("📊 No hourly data yet. Orders will appear here as they come in!")

elif selected_analysis == '📈 Order Trends':
    st.header('📈 Order Trends Analysis (Historical + Live)')
    
    # Combine historical and live data
    all_orders = pd.concat([orders, live_orders], ignore_index=True) if not live_orders.empty else orders
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('📊 Combined Orders by Food Item')
        item_counts = all_orders['food_item'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(len(item_counts)), item_counts.values, color='#4facfe')
        ax.set_xticks(range(len(item_counts)))
        ax.set_xticklabels(item_counts.index, rotation=45, ha='right')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_title('Top 10 Popular Items (All Data)', color='white', fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader('💰 Revenue by Payment Method')
        payment_revenue = all_orders.groupby('payment_method')['amount'].sum()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(payment_revenue.values, labels=payment_revenue.index, autopct='%1.1f%%',
               colors=['#4facfe', '#00f2fe', '#667eea', '#764ba2'])
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        plt.title('Revenue Distribution (All Data)', color='white', fontweight='bold')
        st.pyplot(fig)

elif selected_analysis == '💳 Payment Analysis':
    st.header('💳 Payment Analysis (Enhanced with Real-Time)')
    
    all_orders = pd.concat([orders, live_orders], ignore_index=True) if not live_orders.empty else orders
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader('Historical Payments')
        payment_counts = orders['payment_method'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        plt.title('Historical Payments', color='white', fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader('Live Payments Today')
        if not today_orders.empty:
            live_payments = today_orders['payment_method'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(live_payments.values, labels=live_payments.index, autopct='%1.1f%%',
                   colors=['#4facfe', '#00f2fe', '#667eea', '#764ba2'])
            ax.set_facecolor('none')
            fig.patch.set_facecolor('none')
            plt.title('🔴 Today\'s Live Payments', color='white', fontweight='bold')
            st.pyplot(fig)
        else:
            st.info("No live payments today yet!")
    
    with col3:
        st.subheader('Combined Analysis')
        combined_payments = all_orders['payment_method'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(combined_payments.index, combined_payments.values, color='#00f2fe')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_title('All Payment Methods', color='white', fontweight='bold')
        st.pyplot(fig)

elif selected_analysis == '📝 Customer Feedback':
    st.header('📝 Customer Feedback Analysis')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Rating Distribution')
        rating_counts = feedback['rating'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(rating_counts.index, rating_counts.values, color='#4facfe')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_xlabel('Rating', color='white')
        ax.set_ylabel('Count', color='white')
        ax.set_title('Customer Ratings Distribution', color='white', fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader('Feedback Insights')
        st.write("**Key Metrics:**")
        st.write(f"- Average Rating: {feedback['rating'].mean():.2f}/5")
        st.write(f"- Total Reviews: {len(feedback)}")
        st.write(f"- Positive Reviews (4-5): {len(feedback[feedback['rating'] >= 4])}")
        st.write(f"- Negative Reviews (1-2): {len(feedback[feedback['rating'] <= 2])}")
        
        st.write("**Recent Comments:**")
        for comment in feedback['comments'].tail(5):
            st.write(f"- {comment}")

elif selected_analysis == '🎯 Real-Time Orders':
    st.header('🎯 Real-Time Order Management')
    
    # Live orders table
    if not today_orders.empty:
        st.subheader("🔴 Today's Live Orders")
        
        # Display orders in a nice table
        display_orders = today_orders[['order_id', 'customer_name', 'food_item', 'amount', 'payment_method', 'status', 'timestamp']].copy()
        display_orders['timestamp'] = display_orders['timestamp'].dt.strftime('%H:%M:%S')
        
        st.dataframe(
            display_orders.sort_values('order_id', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🍽️ Orders Today", len(today_orders))
        with col2:
            st.metric("💰 Revenue Today", f"₹{today_orders['amount'].sum():.0f}")
        with col3:
            st.metric("📈 Avg Order", f"₹{today_orders['amount'].mean():.0f}")
        with col4:
            preparing = len(today_orders[today_orders.get('status', 'Delivered') == 'Preparing'])
            st.metric("🍳 Preparing", preparing)
        
    else:
        st.info("🛒 No live orders today yet!")
        st.markdown("""
        **To see real-time orders:**
        1. Use the 🎲 'Simulate 10 Orders' button in sidebar
        2. Or use the Customer Panel to place real orders
        3. Watch the data update in real-time!
        """)

# Show last updated time
if realtime_analytics.get('last_updated'):
    last_updated = datetime.fromisoformat(realtime_analytics['last_updated'])
    st.sidebar.markdown(f"**🔄 Last Updated:** {last_updated.strftime('%H:%M:%S')}")
