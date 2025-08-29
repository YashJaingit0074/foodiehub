import streamlit as st
import subprocess
import time
import threading
import pandas as pd
import json
from datetime import datetime, date
import os
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="FoodieHub Control Center",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh every 10 seconds to show real-time order count
import time
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Auto refresh every 10 seconds
if time.time() - st.session_state.last_refresh > 10:
    st.session_state.last_refresh = time.time()
    st.rerun()

# Manual refresh button for immediate updates
if st.button("🔄 Refresh Data", key="manual_refresh"):
    st.rerun()

# Custom CSS for control panel
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .control-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 30px;
    }
    .panel-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 15px 0;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .panel-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
    }
    .stButton button {
        background: linear-gradient(45deg, #ff6b6b, #ffa726);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 25px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="control-header">
    <h1 style="color: white; margin: 0; font-size: 3.5em;">🎛️ FoodieHub Control Center</h1>
    <p style="color: white; margin: 15px 0; font-size: 1.3em;">One-Click Panel Management System</p>
    <p style="color: rgba(255,255,255,0.8); margin: 0;">Launch • Switch • Monitor</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for running apps
if 'running_apps' not in st.session_state:
    st.session_state.running_apps = {}

# Panel Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="panel-card">
        <h2 style="color: white; margin: 0;">🍕 Customer Panel</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 15px 0;">Browse menu, place orders, leave reviews</p>
        <p style="color: #ffd700; margin: 10px 0;">🎯 For Customers</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Open Customer Panel", key="customer"):
        st.markdown("""
        <script>
        window.open('http://localhost:8511', '_blank');
        </script>
        """, unsafe_allow_html=True)
        st.success("🍕 Opening Customer Panel in new tab...")
        
    # Also show link as backup
    st.markdown("**Direct Link:** [🍕 Customer Panel](http://localhost:8511)")

with col2:
    st.markdown("""
    <div class="panel-card">
        <h2 style="color: white; margin: 0;">📊 Analytics Dashboard</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 15px 0;">Business insights, charts, live data</p>
        <p style="color: #4ecdc4; margin: 10px 0;">📈 For Data Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Analytics Dashboard", key="analytics"):
        st.markdown("""
        <script>
        window.open('http://localhost:8509', '_blank');
        </script>
        """, unsafe_allow_html=True)
        st.success("� Opening Analytics Dashboard in new tab...")
        
    # Also show link as backup
    st.markdown("**Direct Link:** [📊 Analytics](http://localhost:8509)")

with col3:
    st.markdown("""
    <div class="panel-card">
        <h2 style="color: white; margin: 0;">🔐 Admin Panel</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 15px 0;">Restaurant management, settings, controls</p>
        <p style="color: #ff6b6b; margin: 10px 0;">👨‍💼 For Administrators</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔐 Open Admin Panel", key="admin"):
        st.markdown("""
        <script>
        window.open('http://localhost:8503', '_blank');
        </script>
        """, unsafe_allow_html=True)
        st.success("� Opening Admin Panel in new tab...")
        
    # Also show link as backup  
    st.markdown("**Direct Link:** [🔐 Admin Panel](http://localhost:8503)")
    st.info("🔑 Password: admin123 (enter in sidebar)")

# URL Reference Card - HIDDEN PER USER REQUEST
# st.markdown("---")
# st.markdown("""
# <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
#     <h4 style="color: white; text-align: center; margin: 0;">🌐 Quick Access Portal</h4>
#     Quick Access Portal HTML code hidden from frontend
# </div>
# """, unsafe_allow_html=True)

# System Status
st.markdown("---")
st.subheader("⚡ System Information")

# Excel Export Section
st.markdown("---")
st.subheader("📊 Today's Orders Export")

# Debug Information - Show real-time file status
with st.expander("🔍 Debug Info (Click to expand)", expanded=False):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"🕐 **Last Updated:** {current_time}")
    
    # Check live_orders.json
    if os.path.exists('live_orders.json'):
        with open('live_orders.json', 'r', encoding='utf-8') as f:
            live_data = json.load(f)
            st.write(f"📋 **Live Orders File:** {len(live_data)} total orders found")
            
            # Count today's orders
            today = date.today().strftime('%Y-%m-%d')
            todays_count = 0
            for order in live_data:
                timestamp = order.get('timestamp', '')
                if 'T' in timestamp:
                    order_date = timestamp.split('T')[0]
                else:
                    order_date = timestamp.split(' ')[0]
                if order_date == today:
                    todays_count += 1
            
            st.write(f"📅 **Today's Orders ({today}):** {todays_count} orders")
            
            # Show last 3 orders
            if live_data:
                st.write("🔄 **Last 3 Orders:**")
                for i, order in enumerate(live_data[-3:]):
                    st.write(f"   {i+1}. Order #{order.get('order_id')} - {order.get('food_item')} - ₹{order.get('amount')} - {order.get('timestamp', '')[:19]}")
    else:
        st.write("❌ **live_orders.json not found**")

def get_todays_orders():
    """Get all orders from today from all data sources"""
    today = date.today().strftime('%Y-%m-%d')
    all_orders = []
    
    # Load from live_orders.json
    try:
        if os.path.exists('live_orders.json'):
            with open('live_orders.json', 'r', encoding='utf-8') as f:
                live_orders = json.load(f)
                for order in live_orders:
                    # Handle ISO format timestamps (2025-08-26T16:10:33.123456)
                    timestamp = order.get('timestamp', '')
                    if 'T' in timestamp:
                        order_date = timestamp.split('T')[0]  # Get date part before 'T'
                    else:
                        order_date = timestamp.split(' ')[0]  # Fallback for space-separated format
                    
                    if order_date == today:
                        all_orders.append({
                            'Order ID': order.get('order_id', order.get('id', f"L{len(all_orders)+1}")),
                            'Time': timestamp,
                            'Customer Name': order.get('customer_name', order.get('user_name', 'N/A')),
                            'Food Item': order.get('food_item', order.get('meal', 'Mixed Order')),
                            'Quantity': order.get('quantity', 1),
                            'Amount (₹)': order.get('amount', order.get('total', 0)),
                            'Status': order.get('status', 'Completed'),
                            'Source': 'Live Orders'
                        })
    except Exception as e:
        st.error(f"Error loading live orders: {e}")
    
    # Load from models/sample_data.json
    try:
        if os.path.exists('models/sample_data.json'):
            with open('models/sample_data.json', 'r', encoding='utf-8') as f:
                sample_orders = json.load(f)
                for order in sample_orders:
                    timestamp = order.get('order_date', '')
                    if 'T' in timestamp:
                        order_date = timestamp.split('T')[0]
                    else:
                        order_date = timestamp.split(' ')[0]
                    
                    if order_date == today:
                        all_orders.append({
                            'Order ID': order.get('order_id', f"S{len(all_orders)+1}"),
                            'Time': timestamp,
                            'Customer Name': order.get('customer_name', 'N/A'),
                            'Food Item': order.get('item_name', 'N/A'),
                            'Quantity': order.get('quantity', 1),
                            'Amount (₹)': order.get('total_amount', 0),
                            'Status': order.get('status', 'Completed'),
                            'Source': 'Sample Data'
                        })
    except Exception as e:
        st.error(f"Error loading sample orders: {e}")
    
    return all_orders

def create_excel_download(orders_data):
    """Create Excel file for download"""
    if not orders_data:
        return None
    
    # Create DataFrame
    df = pd.DataFrame(orders_data)
    
    # Create a bytes buffer
    buffer = BytesIO()
    
    # Write to Excel
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Today_Orders')
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Today_Orders']
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        money_format = workbook.add_format({
            'num_format': '₹#,##0',
            'border': 1
        })
        
        # Set column widths and apply formats
        for idx, col in enumerate(df.columns):
            if 'Amount' in col:
                worksheet.set_column(idx, idx, 12, money_format)
            else:
                worksheet.set_column(idx, idx, 15)
            worksheet.write(0, idx, col, header_format)
    
    buffer.seek(0)
    return buffer.getvalue()

# Display today's orders count and export option
col1, col2, col3 = st.columns(3)

todays_orders = get_todays_orders()
total_orders = len(todays_orders)
total_amount = sum(order.get('Amount (₹)', 0) for order in todays_orders)

with col1:
    st.markdown("""
    <div style="background: rgba(76, 175, 80, 0.2); padding: 20px; border-radius: 15px; text-align: center;">
        <h2 style="color: #4CAF50; margin: 0;">{}</h2>
        <p style="color: white; margin: 10px 0;">📅 Today's Orders</p>
    </div>
    """.format(total_orders), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: rgba(255, 193, 7, 0.2); padding: 20px; border-radius: 15px; text-align: center;">
        <h2 style="color: #FFC107; margin: 0;">₹{:,}</h2>
        <p style="color: white; margin: 10px 0;">💰 Total Revenue</p>
    </div>
    """.format(total_amount), unsafe_allow_html=True)

with col3:
    if total_orders > 0:
        excel_data = create_excel_download(todays_orders)
        if excel_data:
            today_str = date.today().strftime('%Y-%m-%d')
            st.download_button(
                label="📊 Download Excel Report",
                data=excel_data,
                file_name=f"Orders_Report_{today_str}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download today's orders in Excel format"
            )
    else:
        st.markdown("""
        <div style="background: rgba(158, 158, 158, 0.2); padding: 20px; border-radius: 15px; text-align: center;">
            <p style="color: white; margin: 0;">📝 No orders today</p>
            <small style="color: rgba(255,255,255,0.7);">Place some orders first</small>
        </div>
        """, unsafe_allow_html=True)

# Show preview if orders exist
if total_orders > 0:
    st.markdown("### 📋 Today's Orders Preview")
    
    # Create preview DataFrame (limit to 10 rows for display)
    preview_df = pd.DataFrame(todays_orders[:10])
    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True
    )
    
    if total_orders > 10:
        st.info(f"📊 Showing first 10 orders. Total: {total_orders} orders. Download Excel for complete data!")
else:
    st.info("📝 No orders today yet. Place some orders using the Customer Panel to see data here!")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.metric("🍕 Customer Features", "100%", help="Order system, cart, reviews")

with status_col2:
    st.metric("📊 Analytics Features", "100%", help="Charts, live data, insights")

with status_col3:
    st.metric("🔐 Admin Features", "100%", help="Management, reports, settings")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h4 style="color: white;">🎛️ FoodieHub Control Center - Manage Everything from One Place!</h4>
    <p style="color: rgba(255,255,255,0.8);">🚀 Launch panels • 🔄 Monitor systems • 📊 Track performance</p>
</div>
""", unsafe_allow_html=True)
