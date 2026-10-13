import streamlit as st
from database.database import get_data


def show():
    st.header("💰 Sales Analysis")

    # ==========================================
    # 1. MONTHLY REVENUE TREND
    # ==========================================

    st.subheader("Monthly Revenue Trend")

    monthly_query = """
        SELECT
            DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS sales_month,
            SUM(total_order_value) AS total_revenue,
            COUNT(DISTINCT order_id) AS total_orders
        FROM order_features
        WHERE order_purchase_timestamp IS NOT NULL
        GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m')
        ORDER BY sales_month
    """

    monthly_df = get_data(monthly_query)

    if not monthly_df.empty:
        st.line_chart(
            monthly_df.set_index("sales_month")[["total_revenue"]]
        )
        st.dataframe(
            monthly_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No monthly revenue data found.")

    # ==========================================
    # 2. REVENUE BY PRODUCT CATEGORY
    # ==========================================

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

    category_df = get_data(category_query)

    if not category_df.empty:
        st.bar_chart(
            category_df.set_index("product_category_name")[
                ["category_revenue"]
            ]
        )
        st.dataframe(
            category_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No product category data found.")

    # ==========================================
    # 3. TOP 10 PRODUCTS BY REVENUE
    # ==========================================

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
            COUNT(*) AS total_items
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

    products_df = get_data(products_query)

    if not products_df.empty:
        st.bar_chart(
            products_df.set_index("product_id")[["total_revenue"]]
        )
        st.dataframe(
            products_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No product sales data found.")

    # ==========================================
    # 4. SALES BY CUSTOMER STATE
    # ==========================================

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

    location_df = get_data(location_query)

    if not location_df.empty:
        st.bar_chart(
            location_df.set_index("customer_state")[["total_revenue"]]
        )
        st.dataframe(
            location_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No customer location sales data found.")