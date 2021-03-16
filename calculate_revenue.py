from db import utils

if __name__ == '__main__':
    print('Initializing DB')
    utils.init_db_schema()
    print('Reading log file')