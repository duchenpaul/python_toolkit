from datetime import datetime
import logging
import sys
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Float
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager


DB_FILE = 'bitmap_meta.db'
engine = create_engine('sqlite:///{}'.format(DB_FILE))
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)

# status_history_table = Table('status_history_table', metadata, autoload=True)

status_history_table_name = 'status_history_table'

status_history_table = Table(
    status_history_table_name, metadata,
    Column('run_id', Integer),
    Column('script_name', String(50)),
    Column('load_name', String(50)),
    Column('status', String(50)),
    Column('start_date', DateTime),
    Column('end_date', DateTime),
    Column('duration', Float),
    Column('update_date', DateTime),
)

metadata.create_all(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def insert_status(run_id, script_name, load_name, status, duration, method='ins'):
    update_date = datetime.now()
    if method == 'ins':
        record_values = {
            'run_id': run_id,
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
            'status': status,
            'end_date': update_date,
            'duration': duration,
            'update_date': update_date,
        }
        conditions = and_(
            status_history_table.c.run_id == run_id,
        )
        query = status_history_table.update().\
            values(**record_values).\
            where(conditions)

    with engine.connect() as conn:
        result = conn.execute(query)
        # print(result)


def logging_status(_func):
    def wrapper(*args, **kwargs):
        loadName = _func.__name__
        scriptName = os.path.basename(sys.argv[0].replace('.py', ''))
        try:
            t1 = datetime.now().timestamp()
            run_id = get_status_history_table_count()
            insert_status(run_id, scriptName, loadName, 'READY', -1)
            checking_status(loadName)
            insert_status(run_id, scriptName, loadName, 'RUNNING', -1, method='upd')
            x = _func(*args, **kwargs)
        except AssertionError as e:
            status = 'BLOCKED'
        except Exception as e:
            status = 'FAILED'
            logging.exception()
        else:
            status = 'COMPLETED'
        finally:
            t2 = datetime.now().timestamp()
            insert_status(run_id, scriptName, loadName, status,
                          round(t2 - t1, 2), method='upd')
            return x
    return wrapper


def checking_status(loadName):
    scriptName = os.path.basename(sys.argv[0].replace('.py', ''))
    with session_scope() as session:
        query = session.query(func.count(
            status_history_table.c.script_name))
        query = query.filter(status_history_table.c.status == 'RUNNING')
        count = query.scalar()
    try:
        assert count == 0
    except AssertionError as e:
        logging.error('There is another process running')
        raise


def get_status_history_table_count():
    with session_scope() as session:
        query = session.query(func.count(
            status_history_table.c.script_name))
        count = query.scalar()
    return count


@logging_status
def testee():
    import time
    time.sleep(2)
    print('qwe')


if __name__ == '__main__':
    testee()
