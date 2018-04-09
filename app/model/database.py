from __future__ import print_function
from pymysql import MySQLError
from pymysql import connect
from datetime import datetime, timedelta
import sys

# comentar no funciona
sys.path.append('../modules')

try:
    from app.modules.logger import create_log
    from app.modules.flags import Flag
    from app.modules.config import *
except ImportError:
    from modules.logger import create_log
    from modules.flags import Flag
    from modules.config import *

logger = create_log('prototype')


def connect_db() -> connect:
    cnx = ''

    try:
        cnx = connect(host=mysql_host, port=mysql_port,
                      user=mysql_user, password=mysql_pass, db=mysql_db_name)
        # logger.info('Connect to DB: ' + db_name)
    except MySQLError as err:
        Flag.connect_db = False
        logger.error(err)

    return cnx


def send_data(cnx: connect, ambient: dict):
    if ambient['temperature'] != 100.0:
        # logger.info(ambient)

        query = "INSERT INTO ambient_data " \
                "VALUES ('{}', '{}', '{}', '{}')" \
            .format(ambient['sensor'], ambient['date'],
                    ambient['temperature'], ambient['humidity'])

        send_query(query, cnx)


def send_query(query: str, cnx: connect):
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()

    except MySQLError as err:
        logger.info(type(err))
        logger.error(err)
        # (2013, 'Lost connection to MySQL server during query ([Errno 110] Connection timed out)')
        if err.args[0] == 110 or 2013:
            Flag.connect_db = False
            logger.info('Flag.connect_db: {}'.format(Flag.connect_db))
        # 1062, "Duplicate entry
        elif err.args[0] == 1062:
            logger.error(err)
        else:
            Flag.connect_db = True


def ambient_days(days, table) -> list:
    list_temp = []
    list_humi = []
    list_hour = []
    list_total = []
    list_current = []

    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)

    query = "SELECT temp, humi, date " \
            "FROM {} " \
            "WHERE date BETWEEN '{}' AND '{}'" \
        .format(table, from_date, to_date)

    result_set = query_select(query)

    for rows in result_set:
        current = {
            'current_temp': rows[0],
            'current_humi': rows[1],
            'hour': rows[2].hour
        }
        list_current.append(current)

    for item in list_current:
        list_temp.append(item['current_temp'])
        list_humi.append(item['current_humi'])
        list_hour.append(item['hour'])

    list_total.append(list_temp)
    list_total.append(list_humi)
    list_total.append(list_hour)

    return list_total


def query_select(query):
    result_set = ''
    # logger.debug(query)
    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        # result_set = cursor.fetchmany(size=1)
        result_set = cursor.fetchall()
        cursor.close()
        # logger.debug('result_set: {}'.format(result_set))
    except Exception as err:
        logger.error(err)

    return result_set
