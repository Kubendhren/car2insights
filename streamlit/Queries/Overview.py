# queries/overview.py
from database.database import get_data

def get_overview_kpis():
    query = """
        SELECT
            COUNT(*) AS total_orders
        FROM ORDERS
    """
    return get_data(query)