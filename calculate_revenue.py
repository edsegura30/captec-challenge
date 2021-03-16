from db import utils
from reader.utils import load_log_to_db

if __name__ == '__main__':
    print('Initializing DB')
    utils.init_db_schema()
    print('Reading log file')
    revenue_breakdown = load_log_to_db()
    print('Showing revenue periods')
    for period, total in  revenue_breakdown.items():
        print(f'Revenue placed for orders on {period}: ${total} \n')