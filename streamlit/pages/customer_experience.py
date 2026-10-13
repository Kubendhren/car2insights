
import streamlit as st
from database.database import get_data


def show():
    st.header("⭐ Customer Experience")

    # ==========================================
    # 1. REVIEW SCORE DISTRIBUTION
    # ==========================================

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

    review_distribution_df = get_data(review_distribution_query)

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

    # ==========================================
    # 2. REVIEWS BY PRODUCT CATEGORY
    # ==========================================

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

    category_reviews_df = get_data(category_reviews_query)

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

    # ==========================================
    # 3. RATING VS DELIVERY PERFORMANCE
    # ==========================================

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

    rating_delivery_df = get_data(rating_delivery_query)

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
