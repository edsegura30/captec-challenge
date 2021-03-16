import subprocess

from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from . import LOG_FILE_PATH

READ_CMD = ['cat', LOG_FILE_PATH]


def load_log_to_db():
    """
    Reads the log file using the path defined as an environment variable or
    on the default path ('order_log.csv' at this project root level).
    """
    monthly_revenues = {}
    db_order_values = []
    first_purchases = {}
    # print(read_file(LOG_FILE_PATH)[0])
    for line in read_file(LOG_FILE_PATH):
        line = line.split(',')
        try:
            # I assumed maybe there was sometimes not valid log lines and the
            # int at the beginning could be used to validate if the read line
            # should be processed
            int(line[0])
        except ValueError:
            print('Skipping not valid line')
            continue

        order_date = datetime.fromisoformat(line[4])
        order_user = line[2]

        date_key = f'{order_date.year}-{order_date.month}'
        if date_key in monthly_revenues:
            monthly_revenues[date_key] += Decimal(line[3])
        else:
            monthly_revenues[date_key] = Decimal(line[3])

        if order_user in first_purchases:
            if first_purchases[order_user] > order_date:
                first_purchases[order_user] = order_date
        else:
            first_purchases[order_user] = order_date

        db_order_values.append(
            (line[1], order_date.timestamp(), line[3],  order_user))

    db_user_values = [
        (user_id, date.timestamp()) for user_id, date in first_purchases.items()
    ]

    return monthly_revenues


def read_file(path):
    read_process = subprocess.Popen(
        READ_CMD, stdout=subprocess.PIPE)
    log_rows, _ = read_process.communicate()
    log_rows = log_rows.decode('utf-8')
    return log_rows.splitlines()

