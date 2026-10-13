
import streamlit as st
from database.database import get_data


def show():
    st.header("🏪 Seller & Product Analysis")

    # ==========================================
    # 1. TOP 10 SELLERS BY REVENUE
    # ==========================================

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

    seller_revenue_df = get_data(seller_revenue_query)

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
    else:
        st.info("No seller revenue data found.")

    # ==========================================
    # 2. TOP 10 SELLERS BY ORDER COUNT
    # ==========================================

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

    seller_orders_df = get_data(seller_orders_query)

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
    else:
        st.info("No seller order data found.")

    # ==========================================
    # 3. PRODUCT CATEGORY PERFORMANCE
    # ==========================================

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

    category_performance_df = get_data(category_performance_query)

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
    else:
        st.info("No product category performance data found.")

    # ==========================================
    # 4. SELLER RATINGS
    # ==========================================

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

    seller_rating_df = get_data(seller_rating_query)

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
