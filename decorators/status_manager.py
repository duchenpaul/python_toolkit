from datetime import datetime
import sys, os

import toolkit_sqlite

DB_FILE = 'test.db'

def insert_status(scriptName, loadName, status, duration, method='ins'):
    UPDATE_DATE = datetime.now().strftime('%F %X')
    if method == 'ins':
        update_sql = '''INSERT INTO update_history VALUES ('{SCRIPT_NAME}', '{LOAD_NAME}', '{STATUS}', '{DURATION}', '{UPDATE_DATE}');'''.format(
            SCRIPT_NAME=scriptName, LOAD_NAME=loadName, STATUS=status, UPDATE_DATE=UPDATE_DATE, DURATION=duration)
    elif method == 'upd':
        update_sql = '''UPDATE update_history SET STATUS = '{STATUS}',
                               DURATION = '{DURATION}',
                               UPDATE_DATE = '{UPDATE_DATE}'
                         WHERE STATUS = 'RUNNING' AND SCRIPT_NAME= '{SCRIPT_NAME}' AND LOAD_NAME= '{LOAD_NAME}';'''.format(
            SCRIPT_NAME=scriptName, LOAD_NAME=loadName, STATUS=status, UPDATE_DATE=UPDATE_DATE, DURATION=duration)

    with toolkit_sqlite.SqliteDB(DB_FILE) as sqlitedb:
        sqlitedb.execute(update_sql)

def logging_status(func):
    def wrapper(*args, **kwargs):
        loadName = func.__name__
        scriptName = os.path.basename(sys.argv[0].replace('.py', ''))
        print(scriptName)
        try:
            t1 = datetime.now().timestamp()
            insert_status(scriptName, loadName, 'RUNNING', -1)
            x = func(*args, **kwargs)
        except Exception as e:
            status = 'FAILED'
            print(e)
        else:
            status = 'COMPLETED'
        finally:
            t2 = datetime.now().timestamp()
            insert_status(scriptName, loadName, status,
                          round(t2 - t1, 2), method='upd')
        return x
    return wrapper


@logging_status
def testee():
    print('qwe')


if __name__ == '__main__':
    testee()
