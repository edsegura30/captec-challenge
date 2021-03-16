import psycopg2

from db import (
    DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, 
    ORDER_TABLE_COLUMNS, ORDER_TABLE_NAME, USER_TABLE_COLUMNS, USER_TABLE_NAME
)


def __create_order_table(connection):
    """
    Creates the required table to store the hist. Returns a boolean
    to tell if the table was created or not.
    """
    created = False
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                f"CREATE TABLE {ORDER_TABLE_NAME} ({ORDER_TABLE_COLUMNS});")
            cursor.close()
            connection.commit()
        except Exception as e:
            print('Error type: ', type(e))
            print('Could not create order table: ', str(e))
        else:
            created = True
            print('Order table created')

    return created


def __create_user_table(connection):
    """
    Creates the required table to store basic customer data. Returns a boolean
    to tell if the table was created or not.
    """
    created = False
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                f"CREATE TABLE {USER_TABLE_NAME} ({USER_TABLE_COLUMNS});")
            connection.commit()
        except Exception as e:
            print('Error type: ', type(e))
            print('Could not create user table: ', str(e))
        else:
            created = True
            print('User table created')

    return created


def check_db_status():
    try:
        # Connect to DB
        connection = get_connection()
        with connection.cursor() as cursor:
            # Print DB connectet information
            print("PostgreSQL server information")
            print(connection.get_dsn_parameters(), "\n")
            # Show version used
            cursor.execute("SELECT version();")
            row = cursor.fetchone()
            print("Connected arguments: ", row, "\n")
    except Exception as error:
        print("Error while checking DB status to PostgreSQL", error)
    else:
        if connection:
            connection.close()
            print("Closing used PSQL connection")


def check_table_exists(connection, table_name):
    """
    Returns a Boolean to tell if a certain table exists already.
    """
    data = None
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * '
            f'FROM information_schema.tables '
            f"WHERE table_schema = 'public' AND table_name = '{table_name}'"
            'LIMIT 1;')
        data = cursor.fetchone()
    return data is not None


def get_connection(
    database=DB_NAME, host=DB_HOST, password=DB_PASSWORD):
    """
    Returns a connection object to interact with the DB
    """
    try:
        connection = psycopg2.connect(
                database=DB_NAME,
                host=DB_HOST,
                password=DB_PASSWORD,
                port=DB_PORT,
                user=DB_USER)
        print(f'Connection stablished to DB on {DB_HOST}')
    except psycopg2.Error as e:
        print(f'Could not connect to DB: {e}')
        connection = None
    finally:
        return connection


def init_db_schema():
    connection = get_connection()
    if not check_table_exists(connection, USER_TABLE_NAME):
        print('Creating user table')
        __create_user_table(connection)
    if not check_table_exists(connection, ORDER_TABLE_NAME):
        print('Creating order table')
        __create_order_table(connection)
    connection.close()