import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from models.data_models import load_orders, load_feedback
from models.live_orders import save_order
from models.realtime_tracker import tracker, add_live_order

# Set page configuration
st.set_page_config(
    page_title="FoodieHub - Order & Review",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for user panel
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stApp header {
        background-color: transparent;
    }
    .block-container {
        padding: 2rem 1rem;
        border-radius: 15px;
    }
    h1, h2, h3 {
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    .stButton button {
        background: linear-gradient(45deg, #ff6b6b, #ffa726);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    .food-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    .food-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
    }
    .user-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 30px;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for cart (move this to the top)
if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'cart_total' not in st.session_state:
    st.session_state.cart_total = 0

# User Header
st.markdown("""
<div class="user-header">
    <h1 style="color: white; margin: 0; font-size: 3em;">🍕 FoodieHub</h1>
    <p style="color: white; margin: 10px 0; font-size: 1.2em;">Delicious meals delivered to your doorstep!</p>
    <p style="color: rgba(255,255,255,0.8); margin: 0;">Order • Review • Enjoy</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user options
st.sidebar.markdown("## 🍽️ User Menu")

# User simulation
user_name = st.sidebar.text_input("👤 Enter your name", value="John Doe")
user_phone = st.sidebar.text_input("📱 Phone number", value="+91 98765-43210")
user_address = st.sidebar.text_area("🏠 Delivery address", value="123 Food Street, Delicious City")

st.sidebar.markdown(f"**Welcome, {user_name}! 👋**")

# Cart summary in sidebar
if st.session_state.cart:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛒 Cart Summary")
    st.sidebar.markdown(f"**Items:** {len(st.session_state.cart)}")
    st.sidebar.markdown(f"**Total:** ₹{st.session_state.cart_total}")
    
    if st.sidebar.button("🛒 View Cart"):
        st.sidebar.success("Scroll down to see your cart!")
else:
    st.sidebar.markdown("---")
    st.sidebar.info("🛒 Cart is empty")

# User menu sections
user_section = st.sidebar.selectbox(
    "What would you like to do?",
    ["🍽️ Browse Menu & Order", "📝 My Orders", "⭐ Leave Review", "💝 Special Offers", "👤 My Profile"]
)

# Load data
orders = load_orders()
feedback = load_feedback()

if user_section == "🍽️ Browse Menu & Order":
    st.header("🍽️ Our Delicious Menu")
    
    # Menu categories
    menu_tabs = st.tabs(["🍕 Popular", "🍔 Fast Food", "🥗 Healthy", "🍝 Italian", "🍛 Indian"])
    
    # Sample menu data with prices and descriptions
    menu_items = {
        "Pizza": {"price": 299, "description": "Cheesy margherita with fresh basil", "emoji": "🍕", "rating": 4.5},
        "Burger": {"price": 199, "description": "Juicy beef burger with crispy fries", "emoji": "🍔", "rating": 4.2},
        "Salad": {"price": 149, "description": "Fresh garden salad with olive oil", "emoji": "🥗", "rating": 4.0},
        "Pasta": {"price": 249, "description": "Creamy alfredo pasta with herbs", "emoji": "🍝", "rating": 4.3},
        "Sandwich": {"price": 129, "description": "Grilled chicken sandwich", "emoji": "🥪", "rating": 4.1},
        "Rice Bowl": {"price": 179, "description": "Teriyaki chicken rice bowl", "emoji": "🍛", "rating": 4.4},
        "Noodles": {"price": 169, "description": "Spicy hakka noodles", "emoji": "🍜", "rating": 4.2},
        "Biryani": {"price": 329, "description": "Aromatic chicken biryani", "emoji": "🍛", "rating": 4.6}
    }
    
    with menu_tabs[0]:  # Popular items
        st.subheader("🔥 Most Popular Items")
        
        popular_items = ["Pizza", "Biryani", "Burger"]
        
        for item in popular_items:
            details = menu_items[item]
            
            col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
            
            with col1:
                st.markdown(f"<h1 style='text-align: center; margin: 0;'>{details['emoji']}</h1>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="food-card">
                    <h3 style="margin: 0; color: white;">{item}</h3>
                    <p style="margin: 5px 0; color: rgba(255,255,255,0.8);">{details['description']}</p>
                    <p style="margin: 0; color: #ffd700;">⭐ {details['rating']}/5</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"<h3 style='text-align: center; color: #ffd700;'>₹{details['price']}</h3>", unsafe_allow_html=True)
            
            with col4:
                if st.button(f"🛒 Add", key=f"add_{item}"):
                    # Add item to cart
                    cart_item = {
                        'name': item,
                        'price': details['price'],
                        'quantity': 1,
                        'total': details['price']
                    }
                    
                    # Check if item already in cart
                    existing_item = next((x for x in st.session_state.cart if x['name'] == item), None)
                    if existing_item:
                        existing_item['quantity'] += 1
                        existing_item['total'] = existing_item['quantity'] * existing_item['price']
                    else:
                        st.session_state.cart.append(cart_item)
                    
                    # Update total
                    st.session_state.cart_total = sum(item['total'] for item in st.session_state.cart)
                    
                    st.success(f"✅ {item} added to cart! Total: ₹{st.session_state.cart_total}")
                    st.rerun()
    
    # Shopping cart simulation
    st.markdown("---")
    st.subheader("🛒 Your Cart")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display cart items from session state
        if st.session_state.cart:
            cart_df = pd.DataFrame(st.session_state.cart)
            cart_df = cart_df[['name', 'quantity', 'price', 'total']]
            cart_df.columns = ['Item', 'Quantity', 'Price (₹)', 'Total (₹)']
            
            st.dataframe(cart_df, use_container_width=True, hide_index=True)
            
            # Cart controls
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("🗑️ Clear Cart"):
                    st.session_state.cart = []
                    st.session_state.cart_total = 0
                    st.success("🗑️ Cart cleared!")
                    st.rerun()
            
            with col_b:
                if st.session_state.cart:
                    selected_item = st.selectbox("Remove item:", [item['name'] for item in st.session_state.cart])
                    if st.button("➖ Remove"):
                        st.session_state.cart = [item for item in st.session_state.cart if item['name'] != selected_item]
                        st.session_state.cart_total = sum(item['total'] for item in st.session_state.cart)
                        st.success(f"❌ {selected_item} removed!")
                        st.rerun()
            
            st.markdown(f"### 💰 Total: ₹{st.session_state.cart_total}")
        else:
            st.info("Your cart is empty. Add some delicious items!")
    
    with col2:
        st.markdown("### 🚀 Quick Order")
        
        if st.session_state.cart:
            # Order summary
            st.markdown(f"**📦 Items:** {len(st.session_state.cart)}")
            st.markdown(f"**💰 Total:** ₹{st.session_state.cart_total}")
            
            # Delivery charges
            delivery_charge = 40 if st.session_state.cart_total < 299 else 0
            final_total = st.session_state.cart_total + delivery_charge
            
            if delivery_charge > 0:
                st.markdown(f"**🚚 Delivery:** ₹{delivery_charge}")
            else:
                st.markdown("**🚚 Delivery:** FREE ✅")
            
            st.markdown(f"**🎯 Final Total:** ₹{final_total}")
            
        if st.button("🎯 Place Order", use_container_width=True):
            # Save order to live orders
            order_data = {
                'customer_name': user_name,
                'user_name': user_name,
                'user_phone': user_phone,
                'user_address': user_address,
                'items': st.session_state.cart,
                'food_item': st.session_state.cart[0]['name'] if st.session_state.cart else 'Mixed Order',
                'meal': st.session_state.cart[0]['name'] if st.session_state.cart else 'Mixed Order',
                'amount': final_total,  # This is what realtime_tracker expects
                'total': final_total,   # Keep for compatibility
                'subtotal': st.session_state.cart_total,
                'delivery_charge': delivery_charge,
                'payment_method': 'Card'  # Default payment method
            }
            
            # Save to both old and new tracking systems
            order_id = save_order(order_data)
            realtime_order_id = add_live_order(order_data)
            
            st.balloons()
            st.success(f"🎉 Order #{order_id} placed successfully for ₹{final_total}!")
            st.success(f"🔴 Real-time tracking ID: #{realtime_order_id}")
            st.info("📱 Order is now live in analytics dashboard!")
            
            # Show real-time integration message
            st.markdown("""
            <div style='background-color: #e8f5e8; padding: 15px; border-radius: 10px; margin-top: 10px;'>
                <h4 style='color: #2d5a2d; margin: 0;'>📊 Real-time Analytics Updated!</h4>
                <p style='color: #2d5a2d; margin: 5px 0;'>✅ Your order is now visible in the analytics dashboard</p>
                <p style='color: #2d5a2d; margin: 5px 0;'>📈 Charts will update with your order data</p>
                <p style='color: #2d5a2d; margin: 0;'>🔄 Refresh the analytics dashboard to see changes</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Clear cart after order
            st.session_state.cart = []
            st.session_state.cart_total = 0
            
            # Trigger rerun to update cart display
            st.rerun()
        else:
            st.info("Add items to cart first!")
        
        if st.button("💳 Payment Options", use_container_width=True):
            st.markdown("""
            **💳 Payment Methods:**
            - 💳 Credit/Debit Card
            - 📱 UPI (GPay, PhonePe)
            - 💰 Cash on Delivery
            - 🎫 Wallet
            """)

elif user_section == "📝 My Orders":
    st.header("📝 My Order History")
    
    # Simulate user's orders
    user_orders = orders.head(5).copy()
    user_orders['Status'] = ['Delivered ✅', 'Preparing 🍳', 'Ready 🟢', 'Delivered ✅', 'Cancelled ❌']
    user_orders['Order Date'] = user_orders['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    
    # Order status summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📦 Total Orders", len(user_orders))
    with col2:
        delivered = user_orders['Status'].str.contains('Delivered').sum()
        st.metric("✅ Delivered", delivered)
    with col3:
        total_spent = user_orders['amount'].sum()
        st.metric("💰 Total Spent", f"₹{total_spent}")
    
    st.markdown("---")
    
    # Order details
    st.subheader("📋 Recent Orders")
    
    for _, order in user_orders.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.markdown(f"**🍽️ {order['meal']}**")
            st.text(f"Order #{order['order_id']}")
        
        with col2:
            st.text(f"📅 {order['Order Date']}")
            st.text(f"💳 {order['payment_method']}")
        
        with col3:
            st.markdown(f"**₹{order['amount']}**")
        
        with col4:
            st.markdown(f"**{order['Status']}**")
        
        st.markdown("---")
    
    # Track order button
    if st.button("🔍 Track Current Order", use_container_width=True):
        st.success("📍 Your order is being prepared! Estimated delivery: 25 minutes")

elif user_section == "⭐ Leave Review":
    st.header("⭐ Share Your Experience")
    
    # Review form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Write a Review")
        
        # Order selection
        recent_orders = ["Pizza - Order #001", "Burger - Order #002", "Biryani - Order #003"]
        selected_order = st.selectbox("🍽️ Select your recent order", recent_orders)
        
        # Rating
        rating = st.slider("⭐ Rate your experience", 1, 5, 5)
        
        # Review text
        review_text = st.text_area("💭 Tell us about your experience", 
                                 placeholder="The food was amazing! Great taste and quick delivery...")
        
        # Photo upload simulation
        st.markdown("📷 **Upload a photo of your meal** (optional)")
        uploaded_file = st.file_uploader("Choose a photo", type=['jpg', 'jpeg', 'png'])
        
        if st.button("📨 Submit Review", use_container_width=True):
            st.balloons()
            st.success("🎉 Thank you for your review!")
            st.info("💝 You've earned 50 reward points!")
    
    with col2:
        st.subheader("🏆 Your Reviews")
        
        # Sample previous reviews
        user_reviews = [
            {"item": "Pizza", "rating": 5, "date": "2025-08-20"},
            {"item": "Burger", "rating": 4, "date": "2025-08-18"},
            {"item": "Salad", "rating": 5, "date": "2025-08-15"}
        ]
        
        for review in user_reviews:
            st.markdown(f"""
            <div class="food-card">
                <h4 style="margin: 0; color: white;">{review['item']}</h4>
                <p style="color: #ffd700; margin: 5px 0;">{'⭐' * review['rating']}</p>
                <p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9em;">{review['date']}</p>
            </div>
            """, unsafe_allow_html=True)

elif user_section == "💝 Special Offers":
    st.header("💝 Special Offers & Deals")
    
    # Offers carousel
    offer_tabs = st.tabs(["🔥 Today's Deals", "💰 Combo Offers", "🎉 Loyalty Rewards"])
    
    with offer_tabs[0]:
        st.subheader("🔥 Limited Time Offers")
        
        offers = [
            {"title": "Pizza Blast", "discount": "50% OFF", "desc": "On all pizzas above ₹200", "code": "PIZZA50"},
            {"title": "Burger Bonanza", "discount": "Buy 1 Get 1", "desc": "Free burger on orders above ₹300", "code": "BURGER1"},
            {"title": "Healthy Monday", "discount": "30% OFF", "desc": "All salads and healthy meals", "code": "HEALTH30"}
        ]
        
        for offer in offers:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="food-card">
                    <h3 style="color: #ffd700; margin: 0;">{offer['title']}</h3>
                    <h2 style="color: #ff6b6b; margin: 5px 0;">{offer['discount']}</h2>
                    <p style="color: white; margin: 5px 0;">{offer['desc']}</p>
                    <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9em;">Use code: <strong>{offer['code']}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"🎫 Claim", key=f"claim_{offer['code']}"):
                    st.success(f"✅ {offer['code']} applied!")
    
    with offer_tabs[1]:
        st.subheader("💰 Value Combo Meals")
        
        combos = [
            {"name": "Classic Combo", "items": "Burger + Fries + Coke", "price": "₹249", "save": "₹50"},
            {"name": "Pizza Party", "items": "2 Pizzas + Garlic Bread", "price": "₹499", "save": "₹100"},
            {"name": "Healthy Box", "items": "Salad + Juice + Soup", "price": "₹299", "save": "₹75"}
        ]
        
        for combo in combos:
            st.markdown(f"""
            <div class="food-card">
                <h3 style="color: white; margin: 0;">{combo['name']}</h3>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">{combo['items']}</p>
                <h3 style="color: #ffd700; margin: 5px 0;">{combo['price']} <span style="color: #ff6b6b; font-size: 0.8em;">Save {combo['save']}</span></h3>
            </div>
            """, unsafe_allow_html=True)

elif user_section == "👤 My Profile":
    st.header("👤 My Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="food-card" style="text-align: center;">
            <h1 style="margin: 0;">👤</h1>
            <h3 style="color: white; margin: 10px 0;">{user_name}</h3>
            <p style="color: #ffd700; margin: 5px 0;">⭐ Premium Member</p>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">Member since: Aug 2025</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Loyalty points
        st.markdown("### 💎 Loyalty Points")
        st.metric("Current Points", "1,250", delta="+50")
        
        if st.button("🎁 Redeem Points"):
            st.success("Points redeemed for ₹125 discount!")
    
    with col2:
        st.subheader("📝 Profile Information")
        
        # Editable profile
        name = st.text_input("Full Name", value=user_name)
        email = st.text_input("Email", value="john.doe@email.com")
        phone = st.text_input("Phone", value=user_phone)
        address = st.text_area("Address", value=user_address)
        
        # Preferences
        st.subheader("🍽️ Food Preferences")
        
        col1, col2 = st.columns(2)
        with col1:
            veg = st.checkbox("🥗 Vegetarian", value=False)
            spicy = st.checkbox("🌶️ Spicy Food", value=True)
        with col2:
            healthy = st.checkbox("🏃 Healthy Options", value=True)
            fast = st.checkbox("⚡ Quick Delivery", value=True)
        
        if st.button("💾 Save Profile", use_container_width=True):
            st.success("✅ Profile updated successfully!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h4 style="color: white;">🍕 FoodieHub - Delicious Food, Happy You!</h4>
    <p style="color: rgba(255,255,255,0.8);">📞 Call us: 1800-FOODIE | 📧 support@foodiehub.com</p>
    <p style="color: rgba(255,255,255,0.6);">🚚 Free delivery on orders above ₹299</p>
</div>
""", unsafe_allow_html=True)
