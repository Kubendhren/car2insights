
import streamlit as st

from database.database import test_connection
from utils.styles import apply_styles

from pages.business_overview import show as show_business_overview
from pages.sales_analysis import show as show_sales_analysis
from pages.customer_analysis import show as show_customer_analysis
from pages.seller_product_analysis import show as show_seller_product_analysis
from pages.delivery_analysis import show as show_delivery_analysis
from pages.customer_experience import show as show_customer_experience


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Cart2Insights",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styles()


# ==========================================
# MENU ITEMS
# ==========================================

MENU_ITEMS = [
    ("Business Overview", "📊"),
    ("Sales Analysis", "💰"),
    ("Customer Analysis", "👥"),
    ("Seller & Product Analysis", "🏪"),
    ("Delivery Analysis", "🚚"),
    ("Customer Experience", "⭐")
]

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Business Overview"


# ==========================================
# SIDEBAR HEADER AND MENU
# ==========================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 8px 4px 18px;">
            <div style="
                font-size: 27px;
                font-weight: 800;
                color: white;
                white-space: nowrap;
            ">
                🛒 Cart2Insights
            </div>
            <div style="
                color: #a5b4fc;
                font-size: 13px;
                margin-top: 6px;
            ">
                E-Commerce Analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div style="
            color: #93c5fd;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.8px;
            padding: 8px 4px 12px;
        ">
            MAIN MENU
        </div>
        """,
        unsafe_allow_html=True
    )

    for menu_name, menu_icon in MENU_ITEMS:

        is_selected = (
            st.session_state.selected_page == menu_name
        )

        if st.button(
            f"{menu_icon}   {menu_name}",
            key=f"menu_{menu_name}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            st.session_state.selected_page = menu_name
            st.rerun()

    st.divider()

   


# ==========================================
# DATABASE CONNECTION
# ==========================================

try:
    test_connection()
except Exception as e:
    st.error("Database connection failed.")

    with st.expander("Technical details"):
        st.code(str(e))

    st.stop()


# ==========================================
# PAGE ROUTING
# ==========================================

page = st.session_state.selected_page

if page == "Business Overview":
    show_business_overview()

elif page == "Sales Analysis":
    show_sales_analysis()

elif page == "Customer Analysis":
    show_customer_analysis()

elif page == "Seller & Product Analysis":
    show_seller_product_analysis()

elif page == "Delivery Analysis":
    show_delivery_analysis()

elif page == "Customer Experience":
    show_customer_experience()
