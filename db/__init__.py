import os


DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'captec_challenge')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USER', 'postgres')

ORDER_TABLE_NAME = 'captec_order_log_esd'
USER_TABLE_NAME = 'captec_users_esd'

ORDER_TABLE_COLUMNS = (
    f'order_id varchar(40) primary key, '
    f'amount numeric(10,2), '
    f'customer varchar(35) REFERENCES {USER_TABLE_NAME}(customer_id), '
    f'placed_on timestamp default NULL'
)

USER_TABLE_COLUMNS =(
    f'customer_id varchar(35) primary key, '
    f'first_purchase timestamp default NULL'
)