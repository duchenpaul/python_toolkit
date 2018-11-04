import logging
import MySQLdb
import configparser
import csv
import os
import sys


config_file = os.path.dirname(
    os.path.realpath(__file__)) + os.sep + 'config.ini'

try:
    print('Read config file: ' + config_file)
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
    print("Error read config file, check config.ini")
    sys.exit(1)


class MySQL(object):
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        self.conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            charset=charset)

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
            print('affected_rows: ' + str(affected_row))
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
            print('affected_rows: ' + str(affected_rows))
        return affected_rows

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def __del__(self):
        self.close()


mysql = _MySQL(**config)


def execute_sql(sql_stmt):
    logging.debug("mysql query statement: %s", sql_stmt)
    mysql.execute(sql_stmt)


def insert_data(header, tupleList):
    sql = "INSERT INTO `watchdog`(`name`,`price`) VALUES(%s{});".format(
        ',%s' * (len(tupleList(0)) - 1))
    mysql.executemany(sql, tupleList)


def csv2table(FILE, table_name):
    with open(FILE, encoding='utf-8') as csvfile:
        # Detect header, remove if exists
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)  # Rewind.
        reader = csv.reader(csvfile)
        if has_header:
            # print("Header detected, skip.")
            header = csvfile.readline().replace('\n', '')
        csv_reader = csv.reader(csvfile, delimiter=',')
        header_list = header.split(',')

        sql = '''REPLACE INTO {} VALUES (%s{},NULL,NULL,NULL) '''.format(
            table_name, ',%s' * (len(header_list) - 1))
        mysql.executemany(sql, csv_reader)


if __name__ == '__main__':
    FILE = './fileName.csv'
    csv2table(FILE, 'ssr_server_dyn')
