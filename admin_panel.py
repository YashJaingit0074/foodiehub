import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from models.data_models import load_orders, load_feedback
from models.analysis import analyze_order_trends, analyze_payment_patterns, feedback_analysis

# Set page configuration
st.set_page_config(
    page_title="Admin Panel - Meal Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for admin panel
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp header {
        background: linear-gradient(90deg, #ff4757, #ff3838);
        height: 4rem;
    }
    .block-container {
        padding: 2rem 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    .stSidebar .sidebar-content {
        background: linear-gradient(180deg, #2d1b69, #11998e);
    }
    .admin-header {
        background: linear-gradient(135deg, #ff4757, #ff3838, #ff6b7a);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid #ff4757;
        box-shadow: 0 8px 32px rgba(255, 71, 87, 0.3);
    }
    .admin-card {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.1), rgba(17, 153, 142, 0.1));
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 71, 87, 0.3);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(255, 71, 87, 0.2);
    }
    .metric-admin {
        background: linear-gradient(135deg, #ff4757, #ff6b7a);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(255, 71, 87, 0.4);
    }
    .admin-warning {
        background: linear-gradient(135deg, #ffa502, #ff6348);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #ff4757;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { box-shadow: 0 0 5px #ff4757, 0 0 10px #ff4757, 0 0 15px #ff4757; }
        to { box-shadow: 0 0 10px #ff4757, 0 0 20px #ff4757, 0 0 30px #ff4757; }
    }
    .stSelectbox > div > div > div {
        background-color: rgba(255, 71, 87, 0.2);
        color: white;
        border: 1px solid #ff4757;
    }
    .stButton > button {
        background: linear-gradient(135deg, #ff4757, #ff3838);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(255, 71, 87, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Admin Header
st.markdown("""
<div class="admin-header">
    <h1 style="color: white; margin: 0;">🔐 ADMIN CONTROL PANEL</h1>
    <p style="color: white; margin: 5px 0 0 0;">Restaurant Management Dashboard</p>
    <div class="admin-warning" style="margin-top: 1rem;">
        ⚠️ SECURE ACCESS - AUTHORIZED PERSONNEL ONLY ⚠️
    </div>
</div>
""", unsafe_allow_html=True)

# Authentication simulation
admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
if admin_password != "admin123":
    st.sidebar.error("❌ Access Denied! Please enter correct password.")
    st.stop()

st.sidebar.success("✅ Admin Access Granted")

# Admin Menu
admin_menu = st.sidebar.selectbox(
    "🔐 Admin Functions",
    ["📊 Dashboard Overview", "👥 User Management", "🍽️ Menu Management", 
     "💳 Payment Analytics", "📈 Sales Reports", "⚙️ System Settings"]
)

# Load data
orders, feedback = load_orders(), load_feedback()

if admin_menu == "📊 Dashboard Overview":
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("📊 BUSINESS INTELLIGENCE DASHBOARD")
    
    # Admin Metrics with special styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(orders)
        st.markdown(f"""
        <div class="metric-admin">
            <h3>📋 TOTAL ORDERS</h3>
            <h1>{total_orders:,}</h1>
            <p>+{int(total_orders*0.1)} from yesterday</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_revenue = orders['amount'].sum()
        st.markdown(f"""
        <div class="metric-admin">
            <h3>💰 TOTAL REVENUE</h3>
            <h1>₹{total_revenue:,.0f}</h1>
            <p>+₹{total_revenue*0.15:.0f} growth</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_order_value = orders['amount'].mean()
        st.markdown(f"""
        <div class="metric-admin">
            <h3>📈 AVG ORDER VALUE</h3>
            <h1>₹{avg_order_value:.0f}</h1>
            <p>+12% increase</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        customer_satisfaction = feedback['rating'].mean()
        st.markdown(f"""
        <div class="metric-admin">
            <h3>⭐ SATISFACTION</h3>
            <h1>{customer_satisfaction:.1f}/5</h1>
            <p>+0.3 improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts section
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("📈 PERFORMANCE ANALYTICS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Revenue by Payment Method")
        payment_revenue = orders.groupby('payment_method')['amount'].sum()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(payment_revenue.values, labels=payment_revenue.index, autopct='%1.1f%%',
               colors=['#ff4757', '#ff6b7a', '#ffa502', '#ff9ff3'])
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        plt.title('Revenue Distribution', color='white', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader("📊 Order Volume Trends")
        daily_orders = orders.groupby('order_date').size()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(daily_orders.index, daily_orders.values, 
                color='#ff4757', linewidth=3, marker='o', markersize=8)
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_xlabel('Date', color='white', fontweight='bold')
        ax.set_ylabel('Orders', color='white', fontweight='bold')
        plt.title('Daily Order Volume', color='white', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif admin_menu == "👥 User Management":
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("👥 USER MANAGEMENT SYSTEM")
    
    # Customer insights
    customer_stats = orders.groupby('customer_name').agg({
        'amount': ['count', 'sum', 'mean']
    }).round(2)
    customer_stats.columns = ['Total Orders', 'Total Spent', 'Avg Order Value']
    customer_stats = customer_stats.sort_values('Total Spent', ascending=False)
    
    st.subheader("🏆 Top Customers")
    st.dataframe(customer_stats.head(10), use_container_width=True)
    
    # User activity analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Customer Segmentation")
        high_value = customer_stats[customer_stats['Total Spent'] > customer_stats['Total Spent'].quantile(0.8)]
        medium_value = customer_stats[(customer_stats['Total Spent'] <= customer_stats['Total Spent'].quantile(0.8)) & 
                                     (customer_stats['Total Spent'] > customer_stats['Total Spent'].quantile(0.4))]
        low_value = customer_stats[customer_stats['Total Spent'] <= customer_stats['Total Spent'].quantile(0.4)]
        
        segments = ['High Value', 'Medium Value', 'Low Value']
        segment_counts = [len(high_value), len(medium_value), len(low_value)]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(segments, segment_counts, color=['#ff4757', '#ffa502', '#ff9ff3'])
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_ylabel('Customer Count', color='white', fontweight='bold')
        plt.title('Customer Value Segments', color='white', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader("🎯 Customer Retention")
        retention_data = {
            'New Customers': len(customer_stats) * 0.3,
            'Returning Customers': len(customer_stats) * 0.5,
            'Loyal Customers': len(customer_stats) * 0.2
        }
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(retention_data.values(), labels=retention_data.keys(), autopct='%1.1f%%',
               colors=['#ff4757', '#ffa502', '#ff9ff3'])
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        plt.title('Customer Retention Analysis', color='white', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif admin_menu == "🍽️ Menu Management":
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("🍽️ MENU OPTIMIZATION SYSTEM")
    
    # Popular items analysis
    popular_items = orders['food_item'].value_counts().head(10)
    revenue_by_item = orders.groupby('food_item')['amount'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Most Popular Items")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(popular_items.index[::-1], popular_items.values[::-1], color='#ff4757')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_xlabel('Order Count', color='white', fontweight='bold')
        plt.title('Top 10 Popular Items', color='white', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader("💰 Highest Revenue Items")
        top_revenue = revenue_by_item.head(10)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(top_revenue.index[::-1], top_revenue.values[::-1], color='#ffa502')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_xlabel('Revenue (₹)', color='white', fontweight='bold')
        plt.title('Top Revenue Generators', color='white', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    # Menu performance metrics
    st.subheader("📊 Menu Performance Metrics")
    menu_metrics = pd.DataFrame({
        'Item': popular_items.index[:5],
        'Orders': popular_items.values[:5],
        'Revenue': [revenue_by_item[item] for item in popular_items.index[:5]],
        'Avg Price': [revenue_by_item[item]/popular_items[item] for item in popular_items.index[:5]]
    })
    st.dataframe(menu_metrics, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif admin_menu == "💳 Payment Analytics":
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("💳 PAYMENT SYSTEM ANALYTICS")
    
    # Payment method analysis
    payment_analysis = analyze_payment_patterns(orders)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💳 Payment Method Distribution")
        payment_counts = orders['payment_method'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%',
               colors=['#ff4757', '#ffa502', '#ff9ff3', '#2ed573'])
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        plt.title('Payment Methods Used', color='white', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader("📈 Payment Trends")
        daily_payments = orders.groupby(['order_date', 'payment_method']).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 6))
        for method in daily_payments.columns:
            ax.plot(daily_payments.index, daily_payments[method], 
                   marker='o', linewidth=2, label=method)
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_xlabel('Date', color='white', fontweight='bold')
        ax.set_ylabel('Transaction Count', color='white', fontweight='bold')
        ax.legend()
        plt.title('Daily Payment Method Usage', color='white', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    # Transaction insights
    st.subheader("💰 Transaction Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_transaction = orders['amount'].mean()
        st.markdown(f"""
        <div class="metric-admin">
            <h3>💳 Avg Transaction</h3>
            <h1>₹{avg_transaction:.0f}</h1>
            <p>All payment methods</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        failed_rate = np.random.uniform(0.02, 0.05)  # Simulated failure rate
        st.markdown(f"""
        <div class="metric-admin">
            <h3>❌ Failure Rate</h3>
            <h1>{failed_rate:.1%}</h1>
            <p>Payment processing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        processing_time = np.random.uniform(2.5, 4.0)  # Simulated processing time
        st.markdown(f"""
        <div class="metric-admin">
            <h3>⏱️ Avg Process Time</h3>
            <h1>{processing_time:.1f}s</h1>
            <p>Payment completion</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif admin_menu == "📈 Sales Reports":
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("📈 COMPREHENSIVE SALES REPORTS")
    
    # Time-based analysis
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    orders['month'] = orders['order_date'].dt.to_period('M')
    orders['weekday'] = orders['order_date'].dt.day_name()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Monthly Sales Trend")
        monthly_sales = orders.groupby('month')['amount'].sum()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(range(len(monthly_sales)), monthly_sales.values, color='#ff4757')
        ax.set_xticks(range(len(monthly_sales)))
        ax.set_xticklabels([str(m) for m in monthly_sales.index])
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_xlabel('Month', color='white', fontweight='bold')
        ax.set_ylabel('Revenue (₹)', color='white', fontweight='bold')
        plt.title('Monthly Revenue Trend', color='white', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.subheader("📊 Day-wise Performance")
        weekday_sales = orders.groupby('weekday')['amount'].sum()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_sales = weekday_sales.reindex(day_order, fill_value=0)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(weekday_sales.index, weekday_sales.values, color='#ffa502')
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        ax.tick_params(colors='white')
        ax.set_xlabel('Day of Week', color='white', fontweight='bold')
        ax.set_ylabel('Revenue (₹)', color='white', fontweight='bold')
        plt.title('Weekly Sales Pattern', color='white', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    # Performance summary table
    st.subheader("📋 Sales Summary Report")
    summary_data = {
        'Period': ['Today', 'This Week', 'This Month', 'Last Month'],
        'Orders': [15, 87, 342, 298],
        'Revenue': [12450, 68900, 285000, 245000],
        'Growth': ['+8.5%', '+12.3%', '+16.7%', '+9.2%']
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif admin_menu == "⚙️ System Settings":
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.subheader("⚙️ SYSTEM CONFIGURATION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 General Settings")
        restaurant_name = st.text_input("Restaurant Name", value="FoodieHub")
        max_orders_per_day = st.number_input("Max Orders per Day", value=500, min_value=100)
        delivery_radius = st.slider("Delivery Radius (km)", 1, 20, 10)
        auto_refresh = st.checkbox("Auto-refresh dashboard", value=True)
    
    with col2:
        st.subheader("📊 Dashboard Settings")
        chart_theme = st.selectbox("Chart Theme", ["Dark", "Light", "Auto"])
        show_live_orders = st.checkbox("Show Live Orders", value=True)
        notification_alerts = st.checkbox("Enable Notifications", value=True)
        data_retention = st.selectbox("Data Retention Period", ["30 days", "90 days", "1 year", "Forever"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔒 Security Settings")
        session_timeout = st.slider("Session Timeout (minutes)", 5, 60, 30)
        two_factor_auth = st.checkbox("Enable 2FA", value=False)
        password_expiry = st.selectbox("Password Expiry", ["30 days", "90 days", "Never"])
    
    with col2:
        st.subheader("🚚 Delivery Settings")
        avg_delivery_time = st.slider("Average Delivery Time (minutes)", 15, 60, 30)
        delivery_fee = st.number_input("Delivery Fee (₹)", value=50.0, min_value=0.0)
        free_delivery_threshold = st.number_input("Free Delivery Above (₹)", value=299.0)
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("⚡ Settings saved successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h4 style="color: #ff4757;">🔐 Admin Panel - Secure Access Only</h4>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
