import streamlit as st
import pandas as pd
from sqlalchemy import text

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================


DB_USER = "root"
DB_PASSWORD = "Kuber@123"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "Car2Insights"


@st.cache_resource
def get_engine():
    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    return create_engine(connection_url)


engine = get_engine()



st.sidebar.title("🛒 Cart2Insights")

st.sidebar.caption("E-Commerce Analytics")

page = st.sidebar.radio(
    "Navigate Dashboard",
    [
        "Business Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Seller & Product Analysis",
        "Delivery Analysis",
        "Customer Experience"
    ]
)

st.sidebar.divider()
st.sidebar.info("AIML_Cart2Insights | 2026")


# ==========================================
# PREMIUM DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>
/* Main application background */
.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #eef2ff 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #202b49 100%);
    border-right: 1px solid #293654;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc;
}

section[data-testid="stSidebar"] h1 {
    color: #ffffff;
    font-size: 1.45rem;
    font-weight: 800;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 5px;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(129, 140, 248, 0.24);
}

/* Dashboard title banner */
.dashboard-banner {
    background: linear-gradient(120deg, #172554 0%, #4338ca 55%, #6366f1 100%);
    padding: 30px 32px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(67, 56, 202, 0.20);
}

.dashboard-banner h1 {
    color: white;
    font-size: 30px;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -0.7px;
}

.dashboard-banner p {
    color: #e0e7ff;
    font-size: 15px;
    margin: 0;
}

/* Section headings */
h1, h2, h3 {
    color: #172554;
    font-weight: 750 !important;
    letter-spacing: -0.3px;
}

h2 {
    padding-bottom: 8px;
}

/* KPI metric cards */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #e3e8f5;
    padding: 20px 20px 18px 20px;
    border-radius: 17px;
    box-shadow: 0 5px 18px rgba(30, 41, 59, 0.055);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(67, 56, 202, 0.12);
}

div[data-testid="stMetricLabel"] {
    color: #64748b;
    font-size: 14px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #312e81;
    font-size: 27px;
    font-weight: 800;
}

/* Charts and data containers */
div[data-testid="stPlotlyChart"],
div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    background: white;
    border: 1px solid #e5eaf5;
    border-radius: 16px;
    padding: 10px;
    box-shadow: 0 5px 18px rgba(30, 41, 59, 0.04);
}

/* Dataframe header */
div[data-testid="stDataFrame"] {
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(110deg, #4338ca, #6366f1);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 9px 18px;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    color: white;
    border: none;
    box-shadow: 0 5px 15px rgba(67, 56, 202, 0.25);
    transform: translateY(-1px);
}

/* Inputs */
.stSelectbox div[data-baseweb="select"],
.stTextInput input,
.stDateInput input {
    border-radius: 10px;
}

/* Divider */
hr {
    border-color: #dce3f2;
    margin-top: 22px;
    margin-bottom: 22px;
}

/* Informational messages */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Mobile adjustments */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .dashboard-banner {
        padding: 22px;
        border-radius: 16px;
    }

    .dashboard-banner h1 {
        font-size: 23px;
    }

    div[data-testid="stMetric"] {
        padding: 14px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 21px;
    }
}
</style>
""", unsafe_allow_html=True)


if page == "Business Overview":
    st.header("📊 Business Overview")
    overview_query = """
        SELECT
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(DISTINCT customer_id) AS total_customers,
            COALESCE(SUM(total_order_value), 0) AS total_revenue,
            COALESCE(AVG(total_order_value), 0) AS average_order_value,
            COALESCE(AVG(avg_review_score), 0) AS average_review_score
        FROM order_features
        """

    overview_df = pd.read_sql(text(overview_query),
            engine
        )
    seller_query = """
        SELECT COUNT(DISTINCT seller_id) AS total_sellers
        FROM seller_features
        """

    seller_df = pd.read_sql(
            text(seller_query),
            engine
        )

    row = overview_df.iloc[0]
    total_sellers = seller_df.iloc[0]["total_sellers"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"R$ {row['total_revenue']:,.2f}")
    col2.metric("Total Orders", f"{row['total_orders']:,.0f}")
    col3.metric("Total Customers", f"{row['total_customers']:,.0f}")

    col4, col5, col6 = st.columns(3)

    col4.metric("Total Sellers", f"{total_sellers:,.0f}")
    col5.metric(
            "Average Order Value",
            f"R$ {row['average_order_value']:,.2f}"
        )
    col6.metric(
            "Average Review Score",
            f"{row['average_review_score']:.2f} / 5"
        )

    st.divider()
    st.subheader("Business Summary")
    st.dataframe(overview_df, use_container_width=True, hide_index=True)


elif page == "Sales Analysis":

        st.header("💰 Sales Analysis")

        # --------------------------------------
        # 1. Monthly Revenue Trend
        # --------------------------------------

        st.subheader("Monthly Revenue Trend")

        monthly_query = """
        SELECT
            DATE_FORMAT(order_purchase_timestamp, '%%Y-%%m') AS sales_month,
            SUM(total_order_value) AS total_revenue,
            COUNT(DISTINCT order_id) AS total_orders
        FROM order_features
        WHERE order_purchase_timestamp IS NOT NULL
        GROUP BY DATE_FORMAT(order_purchase_timestamp, '%%Y-%%m')
        ORDER BY sales_month
        """

        monthly_df = pd.read_sql(text(monthly_query), engine)

        if not monthly_df.empty:
            st.line_chart(
                monthly_df.set_index("sales_month")[["total_revenue"]]
            )
            st.dataframe(monthly_df, use_container_width=True, hide_index=True)

        # --------------------------------------
        # 2. Revenue by Category
        # --------------------------------------

        st.subheader("Revenue by Product Category")

        category_query = """
        SELECT
            product_category_name,
            category_revenue,
            item_count,
            avg_item_value
        FROM category_features
        ORDER BY category_revenue DESC
        LIMIT 15
        """

        category_df = pd.read_sql(text(category_query), engine)

        if not category_df.empty:
            st.bar_chart(
                category_df.set_index("product_category_name")[
                    ["category_revenue"]
                ]
            )
            st.dataframe(category_df, use_container_width=True, hide_index=True)

        # --------------------------------------
        # 3. Top-Selling Products
        # --------------------------------------

        st.subheader("Top 10 Products by Revenue")

        products_query = """
        SELECT
            p.product_id,
            COALESCE(
                t.product_category_name_english,
                p.product_category_name,
                'Unknown'
            ) AS product_category,
            COUNT(DISTINCT oi.order_id) AS total_orders,
            SUM(oi.price + oi.freight_value) AS total_revenue,
            SUM(oi.order_item_id) AS total_items
        FROM order_items oi
        INNER JOIN products p
            ON oi.product_id = p.product_id
        LEFT JOIN product_category_translation t
            ON p.product_category_name = t.product_category_name
        GROUP BY
            p.product_id,
            COALESCE(
                t.product_category_name_english,
                p.product_category_name,
                'Unknown'
            )
        ORDER BY total_revenue DESC
        LIMIT 10
        """

        products_df = pd.read_sql(text(products_query), engine)

        if not products_df.empty:
            st.bar_chart(
                products_df.set_index("product_id")[["total_revenue"]]
            )
            st.dataframe(products_df, use_container_width=True, hide_index=True)

        # --------------------------------------
        # 4. Sales by Customer Location
        # --------------------------------------

        st.subheader("Sales by Customer State")

        location_query = """
        SELECT
            c.customer_state,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(oi.price + oi.freight_value) AS total_revenue
        FROM orders o
        INNER JOIN customers c
            ON o.customer_id = c.customer_id
        INNER JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY c.customer_state
        ORDER BY total_revenue DESC
        LIMIT 15
        """

        location_df = pd.read_sql(text(location_query), engine)

        if not location_df.empty:
            st.bar_chart(
                location_df.set_index("customer_state")[["total_revenue"]]
            )
        st.dataframe(location_df, use_container_width=True, hide_index=True)
            
    # ==========================================
    # 3. CUSTOMER ANALYSIS
    # ==========================================

elif page == "Customer Analysis":

        st.header("👥 Customer Analysis")

        # --------------------------------------
        # 1. Customer Distribution by State
        # --------------------------------------

        st.subheader("Customer Distribution by State")

        customer_location_query = """
        SELECT
            customer_state,
            COUNT(DISTINCT customer_unique_id) AS total_customers
        FROM customers
        GROUP BY customer_state
        ORDER BY total_customers DESC
        LIMIT 15
        """

        customer_location_df = pd.read_sql(
            text(customer_location_query), engine
        )

        if not customer_location_df.empty:
            st.bar_chart(
                customer_location_df.set_index("customer_state")[
                    ["total_customers"]
                ]
            )
            st.dataframe(
                customer_location_df,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 2. Customer Spending
        # --------------------------------------

        st.subheader("Customer Spending Distribution")

        spending_query = """
        SELECT
            customer_id,
            customer_order_count,
            customer_total_spending,
            average_order_value
        FROM customer_features
        ORDER BY customer_total_spending DESC
        """

        spending_df = pd.read_sql(text(spending_query), engine)

        if not spending_df.empty:
            st.line_chart(
                spending_df["customer_total_spending"]
                .reset_index(drop=True)
            )

            st.caption(
                "Spending values are ordered from highest to lowest."
            )

            st.dataframe(
                spending_df.head(20),
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 3. New vs Repeat Customers
        # --------------------------------------

        st.subheader("New vs Repeat Customers")

        repeat_query = """
        SELECT
            repeat_customer,
            COUNT(*) AS total_customers
        FROM customer_features
        GROUP BY repeat_customer
        ORDER BY repeat_customer
        """

        repeat_df = pd.read_sql(text(repeat_query), engine)

        if not repeat_df.empty:
            repeat_df["customer_type"] = repeat_df[
                "repeat_customer"
            ].map({
                0: "New / One-time",
                1: "Repeat"
            })

            st.bar_chart(
                repeat_df.set_index("customer_type")[
                    ["total_customers"]
                ]
            )

            st.dataframe(
                repeat_df[["customer_type", "total_customers"]],
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 4. Top 10 Customers
        # --------------------------------------

        st.subheader("Top 10 Customers by Spending")

        top_customers_query = """
        SELECT
            customer_id,
            customer_order_count,
            customer_total_spending,
            average_order_value,
            repeat_customer
        FROM customer_features
        ORDER BY customer_total_spending DESC
        LIMIT 10
        """

        top_customers_df = pd.read_sql(
            text(top_customers_query), engine
        )

        if not top_customers_df.empty:
            st.bar_chart(
                top_customers_df.set_index("customer_id")[
                    ["customer_total_spending"]
                ]
            )

        st.dataframe(
                top_customers_df,
                use_container_width=True,
                hide_index=True
            )
    # ==========================================
    # 4. SELLER & PRODUCT ANALYSIS
    # ==========================================

elif page == "Seller & Product Analysis":

        st.header("🏪 Seller & Product Analysis")

        # --------------------------------------
        # 1. Top 10 Sellers by Revenue
        # --------------------------------------

        st.subheader("Top 10 Sellers by Revenue")

        seller_revenue_query = """
        SELECT
            seller_id,
            seller_order_count,
            seller_revenue,
            average_item_value
        FROM seller_features
        ORDER BY seller_revenue DESC
        LIMIT 10
        """

        seller_revenue_df = pd.read_sql(
            text(seller_revenue_query), engine
        )

        if not seller_revenue_df.empty:
            st.bar_chart(
                seller_revenue_df.set_index("seller_id")[
                    ["seller_revenue"]
                ]
            )

            st.dataframe(
                seller_revenue_df,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 2. Top 10 Sellers by Order Count
        # --------------------------------------

        st.subheader("Top 10 Sellers by Order Count")

        seller_orders_query = """
        SELECT
            seller_id,
            seller_order_count,
            seller_revenue
        FROM seller_features
        ORDER BY seller_order_count DESC
        LIMIT 10
        """

        seller_orders_df = pd.read_sql(
            text(seller_orders_query), engine
        )

        if not seller_orders_df.empty:
            st.bar_chart(
                seller_orders_df.set_index("seller_id")[
                    ["seller_order_count"]
                ]
            )

            st.dataframe(
                seller_orders_df,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 3. Product Category Performance
        # --------------------------------------

        st.subheader("Product Category Performance")

        category_performance_query = """
        SELECT
            product_category_name,
            order_count,
            item_count,
            category_revenue,
            avg_item_value
        FROM category_features
        ORDER BY category_revenue DESC
        LIMIT 15
        """

        category_performance_df = pd.read_sql(
            text(category_performance_query), engine
        )

        if not category_performance_df.empty:
            st.bar_chart(
                category_performance_df.set_index(
                    "product_category_name"
                )[["category_revenue"]]
            )

            st.dataframe(
                category_performance_df,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 4. Seller Ratings
        # --------------------------------------

        st.subheader("Seller Ratings")

        seller_rating_query = """
        SELECT
            oi.seller_id,
            COUNT(DISTINCT oi.order_id) AS total_orders,
            ROUND(AVG(r.review_score), 2) AS average_review_score,
            COUNT(r.review_id) AS review_records
        FROM order_items oi
        INNER JOIN orders o
            ON oi.order_id = o.order_id
        INNER JOIN order_reviews r
            ON o.order_id = r.order_id
        GROUP BY oi.seller_id
        HAVING COUNT(r.review_id) > 0
        ORDER BY average_review_score DESC, total_orders DESC
        LIMIT 10
        """

        seller_rating_df = pd.read_sql(
            text(seller_rating_query), engine
        )

        if not seller_rating_df.empty:
            st.bar_chart(
                seller_rating_df.set_index("seller_id")[
                    ["average_review_score"]
                ]
            )

            st.dataframe(
                seller_rating_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No seller review data found.")
       # ==========================================
    # 5. DELIVERY ANALYSIS
    # ==========================================

elif page == "Delivery Analysis":

        st.header("🚚 Delivery Analysis")

        # --------------------------------------
        # 1. Average Delivery Time
        # --------------------------------------

        st.subheader("Average Delivery Time")

        delivery_kpi_query = """
        SELECT
            ROUND(AVG(delivery_days), 2) AS average_delivery_days,
            ROUND(AVG(delivery_delay_days), 2) AS average_delay_days,
            COUNT(*) AS total_orders
        FROM order_features
        WHERE delivery_days IS NOT NULL
        """

        delivery_kpi_df = pd.read_sql(
            text(delivery_kpi_query), engine
        )

        if not delivery_kpi_df.empty:
            row = delivery_kpi_df.iloc[0]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Average Delivery Time",
                f"{row['average_delivery_days']:.2f} days"
                if pd.notna(row["average_delivery_days"])
                else "N/A"
            )

            col2.metric(
                "Average Delivery Delay",
                f"{row['average_delay_days']:.2f} days"
                if pd.notna(row["average_delay_days"])
                else "N/A"
            )

            col3.metric(
                "Delivered Orders",
                f"{row['total_orders']:,.0f}"
            )

        # --------------------------------------
        # 2. On-Time vs Delayed Orders
        # --------------------------------------

        st.subheader("On-Time vs Delayed Orders")

        delivery_status_query = """
        SELECT
            delivery_status,
            COUNT(*) AS total_orders
        FROM order_features
        GROUP BY delivery_status
        ORDER BY total_orders DESC
        """

        delivery_status_df = pd.read_sql(
            text(delivery_status_query), engine
        )

        if not delivery_status_df.empty:
            st.bar_chart(
                delivery_status_df.set_index("delivery_status")[
                    ["total_orders"]
                ]
            )

            st.dataframe(
                delivery_status_df,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 3. Delivery Performance by State
        # --------------------------------------

        st.subheader("Delivery Performance by Customer State")

        delivery_location_query = """
        SELECT
            c.customer_state,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(AVG(
                DATEDIFF(
                    o.order_delivered_customer_date,
                    o.order_purchase_timestamp
                )
            ), 2) AS average_delivery_days,
            ROUND(AVG(
                CASE
                    WHEN o.order_delivered_customer_date IS NOT NULL
                     AND o.order_estimated_delivery_date IS NOT NULL
                     AND o.order_delivered_customer_date
                         <= o.order_estimated_delivery_date
                    THEN 1
                    ELSE 0
                END
            ) * 100, 2) AS on_time_percentage
        FROM orders o
        INNER JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_status = 'delivered'
        GROUP BY c.customer_state
        ORDER BY average_delivery_days DESC
        """

        delivery_location_df = pd.read_sql(
            text(delivery_location_query), engine
        )

        if not delivery_location_df.empty:
            st.bar_chart(
                delivery_location_df.set_index("customer_state")[
                    ["average_delivery_days"]
                ]
            )

            st.dataframe(
                delivery_location_df,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------
        # 4. Delivery Delay vs Review Score
        # --------------------------------------

        st.subheader("Delivery Performance vs Review Score")

        delivery_review_query = """
        SELECT
            delivery_status,
            ROUND(AVG(avg_review_score), 2) AS average_review_score,
            COUNT(*) AS total_orders
        FROM order_features
        WHERE avg_review_score IS NOT NULL
        GROUP BY delivery_status
        ORDER BY average_review_score DESC
        """

        delivery_review_df = pd.read_sql(
            text(delivery_review_query), engine
        )

        if not delivery_review_df.empty:
            st.bar_chart(
                delivery_review_df.set_index("delivery_status")[
                    ["average_review_score"]
                ]
            )

            st.dataframe(
                delivery_review_df,
                use_container_width=True,
                hide_index=True
            )
    # ==========================================
    # 6. CUSTOMER EXPERIENCE
    # ==========================================

elif page == "Customer Experience":

        st.header("⭐ Customer Experience")

        # --------------------------------------
        # 1. Review Score Distribution
        # --------------------------------------

        st.subheader("Review Score Distribution")

        review_distribution_query = """
        SELECT
            review_score,
            COUNT(*) AS total_reviews
        FROM order_reviews
        WHERE review_score IS NOT NULL
        GROUP BY review_score
        ORDER BY review_score
        """

        review_distribution_df = pd.read_sql(
            text(review_distribution_query), engine
        )

        if not review_distribution_df.empty:
            st.bar_chart(
                review_distribution_df.set_index("review_score")[
                    ["total_reviews"]
                ]
            )

            st.dataframe(
                review_distribution_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No review score data found.")

        # --------------------------------------
        # 2. Reviews by Product Category
        # --------------------------------------

        st.subheader("Reviews by Product Category")

        category_reviews_query = """
        SELECT
            COALESCE(
                t.product_category_name_english,
                p.product_category_name,
                'Unknown'
            ) AS product_category,
            COUNT(DISTINCT r.review_id) AS total_reviews,
            ROUND(AVG(r.review_score), 2) AS average_review_score
        FROM order_reviews r
        INNER JOIN order_items oi
            ON r.order_id = oi.order_id
        INNER JOIN products p
            ON oi.product_id = p.product_id
        LEFT JOIN product_category_translation t
            ON p.product_category_name = t.product_category_name
        WHERE r.review_score IS NOT NULL
        GROUP BY
            COALESCE(
                t.product_category_name_english,
                p.product_category_name,
                'Unknown'
            )
        ORDER BY average_review_score DESC
        LIMIT 15
        """

        category_reviews_df = pd.read_sql(
            text(category_reviews_query), engine
        )

        if not category_reviews_df.empty:
            st.bar_chart(
                category_reviews_df.set_index("product_category")[
                    ["average_review_score"]
                ]
            )

            st.dataframe(
                category_reviews_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No category review data found.")

        # --------------------------------------
        # 3. Rating vs Delivery Performance
        # --------------------------------------

        st.subheader("Rating vs Delivery Performance")

        rating_delivery_query = """
        SELECT
            delivery_status,
            COUNT(*) AS total_orders,
            ROUND(AVG(avg_review_score), 2) AS average_review_score,
            ROUND(AVG(delivery_days), 2) AS average_delivery_days
        FROM order_features
        WHERE avg_review_score IS NOT NULL
        GROUP BY delivery_status
        ORDER BY average_review_score DESC
        """

        rating_delivery_df = pd.read_sql(
            text(rating_delivery_query), engine
        )

        if not rating_delivery_df.empty:
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown("**Average Review Score**")

                st.bar_chart(
                    rating_delivery_df.set_index("delivery_status")[
                        ["average_review_score"]
                    ]
                )

            with chart_col2:
                st.markdown("**Average Delivery Days**")

                st.bar_chart(
                    rating_delivery_df.set_index("delivery_status")[
                        ["average_delivery_days"]
                    ]
                )

            st.dataframe(
                rating_delivery_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No delivery and review data available.")