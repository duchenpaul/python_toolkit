from datetime import datetime
import sys
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Float
from sqlalchemy.sql import and_, or_, not_

DB_FILE = 'test.db'
engine = create_engine('sqlite:///{}'.format(DB_FILE))
metadata = MetaData(engine)

# status_history_table = Table('status_history_table', metadata, autoload=True)

status_history_table = Table(
    'status_history_table', metadata,
    Column('script_name', String),
    Column('load_name', String),
    Column('status', String),
    Column('start_date', DateTime),
    Column('end_date', DateTime),
    Column('duration', Float),
    Column('update_date', String),
)

metadata.create_all(engine)


def insert_status(script_name, load_name, status, duration, method='ins'):
    update_date = datetime.now()
    if method == 'ins':
        record_values = {
            'script_name': script_name,
            'load_name': load_name,
            'status': status,
            'start_date': update_date,
            'end_date': None,
            'duration': -1,
            'update_date': update_date,
        }
        query = status_history_table.insert().values(**record_values)

    elif method == 'upd':
        record_values = {
            'script_name': script_name,
            'load_name': load_name,
            'status': status,
            'end_date': update_date,
            'duration': duration,
            'update_date': update_date,
        }
        conditions = and_(
            status_history_table.c.status == 'RUNNING',
            status_history_table.c.script_name == script_name,
            status_history_table.c.load_name == load_name,
        )
        query = status_history_table.update().\
            values(**record_values).\
            where(conditions)

    with engine.connect() as conn:
        result = conn.execute(query)
        # print(result)


def logging_status(func):
    def wrapper(*args, **kwargs):
        loadName = func.__name__
        scriptName = os.path.basename(sys.argv[0].replace('.py', ''))
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
    import time
    time.sleep(2)
    print('qwe')


if __name__ == '__main__':
    testee()
