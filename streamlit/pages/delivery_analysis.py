
import streamlit as st
from database.database import get_data


def show():
    st.header("🚚 Delivery Analysis")

    # ==========================================
    # 1. AVERAGE DELIVERY TIME
    # ==========================================

    st.subheader("Average Delivery Time")

    delivery_kpi_query = """
        SELECT
            ROUND(AVG(delivery_days), 2) AS average_delivery_days,
            ROUND(AVG(delivery_delay_days), 2) AS average_delay_days,
            COUNT(*) AS total_orders
        FROM order_features
        WHERE delivery_days IS NOT NULL
    """

    delivery_kpi_df = get_data(delivery_kpi_query)

    if not delivery_kpi_df.empty:
        row = delivery_kpi_df.iloc[0]

        col1, col2, col3 = st.columns(3)

        average_days = row["average_delivery_days"]
        average_delay = row["average_delay_days"]
        total_orders = row["total_orders"]

        col1.metric(
            "Average Delivery Time",
            f"{average_days:.2f} days"
            if average_days is not None
            else "N/A"
        )

        col2.metric(
            "Average Delivery Delay",
            f"{average_delay:.2f} days"
            if average_delay is not None
            else "N/A"
        )

        col3.metric(
            "Delivered Orders",
            f"{total_orders:,.0f}"
            if total_orders is not None
            else "0"
        )
    else:
        st.info("No delivery KPI data found.")

    # ==========================================
    # 2. ON-TIME VS DELAYED ORDERS
    # ==========================================

    st.subheader("On-Time vs Delayed Orders")

    delivery_status_query = """
        SELECT
            delivery_status,
            COUNT(*) AS total_orders
        FROM order_features
        GROUP BY delivery_status
        ORDER BY total_orders DESC
    """

    delivery_status_df = get_data(delivery_status_query)

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
    else:
        st.info("No delivery status data found.")

    # ==========================================
    # 3. DELIVERY PERFORMANCE BY CUSTOMER STATE
    # ==========================================

    st.subheader("Delivery Performance by Customer State")

    delivery_location_query = """
        SELECT
            c.customer_state,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(
                AVG(
                    DATEDIFF(
                        o.order_delivered_customer_date,
                        o.order_purchase_timestamp
                    )
                ),
                2
            ) AS average_delivery_days,
            ROUND(
                AVG(
                    CASE
                        WHEN o.order_delivered_customer_date IS NOT NULL
                         AND o.order_estimated_delivery_date IS NOT NULL
                         AND o.order_delivered_customer_date
                             <= o.order_estimated_delivery_date
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS on_time_percentage
        FROM orders o
        INNER JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_status = 'delivered'
        GROUP BY c.customer_state
        ORDER BY average_delivery_days DESC
    """

    delivery_location_df = get_data(delivery_location_query)

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
    else:
        st.info("No customer state delivery data found.")

    # ==========================================
    # 4. DELIVERY PERFORMANCE VS REVIEW SCORE
    # ==========================================

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

    delivery_review_df = get_data(delivery_review_query)

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
    else:
        st.info("No delivery review data found.")
