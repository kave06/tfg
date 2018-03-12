from __future__ import print_function
from pymysql import MySQLError
import configparser
from pymysql import connect
from datetime import datetime, timedelta

from app.modules.flags import Flag
from app.modules.logger import create_log

logger = create_log('prototype')

# config = configparser.ConfigParser()
# config.read('config.ini')
# db_config = config['MySQL']
# variables = config['variables']
# reconnect = variables['reconnect']


def connect_db() -> connect:
    # host = db_config['host']
    # port = int(db_config['port'])
    # user = db_config['user']
    # passw = db_config['pass']
    # db_name = db_config['db_name']

    host = 'gui.uva.es'
    port = 5584
    # host = 'localhost'
    # port = 3306

    user = 'kave'
    passw = 'hola'
    db_name = 'prototipo'

    cnx = ''

    try:
        cnx = connect(host=host, port=port, user=user, password=passw, db=db_name)
        logger.info('Connect to DB: ' + db_name)
    except MySQLError as err:
        Flag.connect_db = False
        logger.error(err)
        # logger.info('Wait 30s to try to reconnect database')
        # sleep(30)

    return cnx


def send_data(cnx: connect, ambient: dict):
    if ambient['temperature'] != 100.0:
        logger.info(ambient)
        # date_time = datetime.datetime.now()
        # sensor = ambient['sensor']
        # temperature = ambient['temperature']
        # humidity = ambient['humidity']

        query = "INSERT INTO ambient_data " \
                "VALUES ('{}', '{}', '{}', '{}')" \
            .format(ambient['sensor'], datetime.now(),
                    ambient['temperature'], ambient['humidity'])
        # .format(sensor, date_time, temperature, humidity)

        send_query(query, cnx)


# TODO clean function
def send_query(query: str, cnx: connect):

    try:
        # logger.info('entro en try')
        # logger.info('query:  {}'.format(query))
        cursor = cnx.cursor()

        # If the connection to the net
        # the program stop here
        # TODO why don't launch an exception?
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        # cnx.close()

    except MySQLError as err:
        # logger.info('entro en except')
        logger.info(type(err))
        logger.error(err)
        # logger.info(err.args[0])
        # MySQL time out, lost connection
        # (2013, 'Lost connection to MySQL server during query ([Errno 110] Connection timed out)')
        if err.args[0] == 110 or 2013:
            Flag.connect_db = False
            logger.info('Flag.connect_db: {}'.format(Flag.connect_db))
            # logger.info('Tengo q salir while ext')
        # 1062, "Duplicate entry
        elif err.args[0] == 1062:
            logger.error(err)
            # don't do anything
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
            # 'current_datetime': rows[2],
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
    logger.info(query)
    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        # result_set = cursor.fetchmany(size=1)
        result_set = cursor.fetchall()
        cursor.close()
        logger.info('result_set: {}'.format(result_set))
    except Exception as err:
        logger.error(err)

    return result_set
