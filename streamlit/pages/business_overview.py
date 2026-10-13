import streamlit as st
from database.database import get_data


def show():
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

    seller_query = """
        SELECT COUNT(DISTINCT seller_id) AS total_sellers
        FROM seller_features
    """

    overview_df = get_data(overview_query)
    seller_df = get_data(seller_query)

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