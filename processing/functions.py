from calendar import monthrange
from datetime import datetime

from db import ORDER_TABLE_NAME, USER_TABLE_NAME
from db.utils import get_connection


def get_new_customers_for_period(period):
    """
    Returns ids for customers aquired in the period selected
    """
    year, month = period.split('-')
    start_date = datetime(year, month, 1)
    _, last_month_day = monthrange(year, month)
    end_date = datetime(year, month, last_month_day)

    db = get_connection()
    USER_QUERY = (
        f'SELECT customer_id FROM {USER_TABLE_NAME} '
        f'WHERE first_purchase >= {start_date} '
        f'AND first_purchase < {last_date}')