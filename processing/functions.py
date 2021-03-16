from calendar import monthrange
from datetime import datetime, timedelta
from decimal import Decimal

from db import ORDER_TABLE_NAME, USER_TABLE_NAME
from db.utils import get_connection

USER_COUNT = (
    "SELECT COUNT(customer_id) FROM captec_users_esd "
    "WHERE first_purchase >= '%(start)s' "
    "AND first_purchase < '%(end)s'")
USER_QUERY = (
    "SELECT DISTINCT customer_id FROM captec_users_esd "
    "WHERE first_purchase >= '%(start)s' "
    "AND first_purchase < '%(end)s'")

def __extract_month_and_year_from_period(period):
    year, month = period.split('-')
    return int(month), int(year)


def __get_start_and_end_date_for_period(period):
    month, year = __extract_month_and_year_from_period(period)
    start_date = datetime(year, month, 1)
    _, last_month_day = monthrange(year, month)
    end_date = start_date + timedelta(days=last_month_day)
    return start_date, end_date


def get_sum_of_orders_for_period(period, new_users=False):
    """
    Returns a Decimal with the total value for the orders in the period
    selected. If an array of customer_ids is received, then the order list
    will be limited to the ones placed by the new users.
    """
    start_date, end_date = __get_start_and_end_date_for_period(period)
    order_gross = 0
    if new_users:
        subquery = USER_QUERY % {'start': start_date, 'end': end_date}
        ORDER_QUERY = (
        f'SELECT SUM(amount) FROM {ORDER_TABLE_NAME} '
        f'WHERE customer IN ({subquery})'
        f"AND placed_on < '{end_date}' "
        f"AND placed_on >= '{start_date}'")
    else:
        ORDER_QUERY = (
        f'SELECT SUM(amount) FROM {ORDER_TABLE_NAME} '
        f"WHERE placed_on >= '{start_date}' "
        f"AND placed_on <= '{end_date}';")

    db = get_connection()
    cursor = db.cursor()
    cursor.execute(ORDER_QUERY)
    order_gross = cursor.fetchone()[0]
    db.close()
    return order_gross


def get_sum_of_user_orders(period):
    orders_sum = 0
    start_date, end_date = __get_start_and_end_date_for_period(period)
    subquery = USER_QUERY % {'start': start_date, 'end': end_date}
    query = (
        f'SELECT SUM(amount) FROM {ORDER_TABLE_NAME} '
        f'WHERE customer IN ({subquery});')
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(query)
    orders_sum = cursor.fetchone()[0]
    db.close()
    return orders_sum


def get_users_acquired_in_period(period):
    """
    Returns a COUNT of the users that were acquired on period
    """
    start_date, end_date = __get_start_and_end_date_for_period(period)
    count = 0
    db = get_connection()
    cursor = db.cursor()
    query = USER_COUNT % {'start': start_date, 'end': end_date}
    cursor.execute(query)
    user_count = cursor.fetchone()[0]
    db.close()
    return user_count
