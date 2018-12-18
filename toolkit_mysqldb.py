import MySQLdb
import csv
import os
import sys
import logging

import pandas as pd


class MySQL(object):
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        self.conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            charset=charset)

    def __enter__(self):
        return self

    def __exit__(self, Type, value, traceback):
        '''
        Executed after "with"
        '''
        if hasattr(self, 'self.cursor'):
            logging.info('Close the DB')
            self.cursor.close()

    def get_cursor(self):
        return self.conn.cursor()

    def query(self, sql):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, None)
            result = cursor.fetchall()
        except Exception as e:
            logging.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return result

    def query2dict(self, sql):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, None)
            desc = cursor.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in cursor.fetchall()]
        except Exception as e:
            logging.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return data

    def query2dataframe(self, sql):
        cursor = self.get_cursor()
        try:
            df = pd.read_sql(sql, self.conn)
        except Exception as e:
            logging.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return df

    def execute(self, sql, param=None):
        affected_row = 0
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, param)
            self.conn.commit()
            affected_row = cursor.rowcount
        except Exception as e:
            logging.error("mysql execute error: %s", e)
            return 0
        finally:
            cursor.close()
            logging.info('affected_rows: ' + str(affected_row))
        return affected_row

    def executemany(self, sql, params=None):
        cursor = self.get_cursor()
        affected_rows = 0
        try:
            cursor.executemany(sql, params)
            self.conn.commit()
            affected_rows = cursor.rowcount
        except Exception as e:
            logging.error("mysql executemany error: %s", e)
            return 0
        finally:
            cursor.close()
            logging.info('affected_rows: ' + str(affected_rows))
        return affected_rows

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def __del__(self):
        self.close()


if __name__ == '__main__':
    import configparser

    config_file = os.path.dirname(
        os.path.realpath(__file__)) + os.sep + 'config.ini'

    try:
        logging.debug('Read config file: ' + config_file)
        configRead = configparser.ConfigParser()
        configRead.read(config_file)
        config = {
            'host': configRead['database']['host'],
            'port': int(configRead['database']['port']),
            'user': configRead['database']['user'],
            'passwd': configRead['database']['passwd'],
            'db': configRead['database']['db'],
            'charset': 'utf8'
        }
    except Exception as e:
        logging.error("Error read config file, check config.ini")
        sys.exit(1)

    query_sql = '''SELECT * FROM Other.test;'''

    with MySQL(**config) as mysql:
        result = mysql.query2dataframe(query_sql)
        print(result)
