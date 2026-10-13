
import streamlit as st
from database.database import get_data


def show():
    st.header("👥 Customer Analysis")

    # ==========================================
    # 1. CUSTOMER DISTRIBUTION BY STATE
    # ==========================================

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

    customer_location_df = get_data(customer_location_query)

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
    else:
        st.info("No customer location data found.")

    # ==========================================
    # 2. CUSTOMER SPENDING DISTRIBUTION
    # ==========================================

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

    spending_df = get_data(spending_query)

    if not spending_df.empty:
        st.line_chart(
            spending_df["customer_total_spending"].reset_index(drop=True)
        )

        st.caption(
            "Spending values are ordered from highest to lowest."
        )

        st.dataframe(
            spending_df.head(20),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No customer spending data found.")

    # ==========================================
    # 3. NEW VS REPEAT CUSTOMERS
    # ==========================================

    st.subheader("New vs Repeat Customers")

    repeat_query = """
        SELECT
            repeat_customer,
            COUNT(*) AS total_customers
        FROM customer_features
        GROUP BY repeat_customer
        ORDER BY repeat_customer
    """

    repeat_df = get_data(repeat_query)

    if not repeat_df.empty:
        repeat_df["customer_type"] = repeat_df[
            "repeat_customer"
        ].map({
            0: "New / One-time",
            1: "Repeat"
        }).fillna("Unknown")

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
    else:
        st.info("No repeat customer data found.")

    # ==========================================
    # 4. TOP 10 CUSTOMERS BY SPENDING
    # ==========================================

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

    top_customers_df = get_data(top_customers_query)

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
    else:
        st.info("No top customer data found.")
