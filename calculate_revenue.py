from db import utils
from processing import functions
from reader.utils import load_log_to_db

if __name__ == '__main__':
    print('Initializing DB')
    utils.init_db_schema()
    print('Reading log file')
    revenue_breakdown = load_log_to_db()
    print('Showing revenue periods')
    for period, total in  revenue_breakdown.items():
        print(f'Showing insights on period {period}')
        total_for_new_users = functions.get_sum_of_orders_for_period(
            period, new_users=True)
        new_users = functions.get_users_acquired_in_period(period)
        revenue_for_users_acquired = functions.get_sum_of_user_orders(period)
        percentage_for_new_users = round(total_for_new_users / total, 2) * 100
        print(f'Total revenue in period: ${total}')
        print(f'Users acquired: {new_users}')
        print(f"Month's revenue by new customers: ${total_for_new_users}'")
        print(f'PErcentage: {percentage_for_new_users}%')
        print(f'Total revenue for new customers: ${revenue_for_users_acquired}')
        print()

