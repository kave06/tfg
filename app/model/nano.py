import re
import bluetooth
from bluetooth import BluetoothSocket, RFCOMM, BluetoothError
from time import sleep
from serial import Serial, SerialException

try:
    from app.modules.flags import Flag
    from app.modules.logger import create_log
    from app.modules.config import *
except ImportError:
    from modules.flags import Flag
    from modules.logger import create_log
    from modules.config import *

logger = create_log('prototype')


def connect_bluetooth(db_addr, port) -> BluetoothSocket:
    sock = bluetooth.BluetoothSocket(RFCOMM)

    try:
        sock.connect((db_addr, port))
        logger.info('socket connection successful in device: {}'.format(db_addr))
    except BluetoothError as err:
        logger.error(err)
        logger.info('error in device: {}'.format(db_addr))
        if db_addr == bluetooth_module1:
            Flag.sock_bluetooth1 = False
        elif db_addr == bluetooth_module2:
            Flag.sock_bluetooth2 = False

        err = str(err).replace('(', '')
        err = err.replace(')', '')
        err = err.split(',')
        # (16, 'Device or resource busy')
        if int(err[0]) == 16:
            logger.info('Device or resource busy')
            sock.close()
        # (112, 'Host is down')
        if int(err[0]) == 112:
            logger.info('Host is down')
            return sock

    return sock


def connect_serial(port, baud) -> Serial:
    serial_cnx = ''
    try:
        serial_cnx = Serial(port, baud)
        # logger.debug('connect to serial')
    except SerialException as err:
        logger.error(err)

    return serial_cnx


def send_signal(signal: bytes):
    arduino = connect_serial(serial_port, serial_bd)

    sleep(0.1)
    # logger.debug(signal)
    signal2 = signal.decode()
    # logger.debug(signal2)
    if signal2 == 'ON':
        try:
            arduino.write('1'.encode())
            arduino.close()
        except SerialException as err:
            logger.error(err)
    elif signal2 == 'OFF':
        try:
            arduino.write('0'.encode())
            arduino.close()
        except SerialException as err:
            logger.error(err)
    # logger.info('Led is {}'.format(signal2))


def read_nano_bluetooth(sock: BluetoothSocket, device: int) -> dict:
    logger.debug('reading arduino {}'.format(device))
    regex = '(\d{1}\s\T:\s\d{1,2}\.\d{2}\s\d{2}\.\d{2}\s:H)'
    regex1 = 'nan'
    regex = re.compile(regex)
    regex1 = re.compile(regex1)
    data = ''
    data1 = ''
    ambient = dict(sensor=0, temperature=100.0, humidity=0.0)

    try:
        sock.getpeername()
    except BluetoothError as err:
        logger.error(err)
        Flag.inner_while = False
        if device == 1:
            Flag.sock_bluetooth1 = False
        elif device == 2:
            Flag.sock_bluetooth2 = False
        logger.debug('return ambient: {}'.format(ambient))
        return ambient

    while True:
        try:
            data = sock.recv(1024)
            data = data.decode('unicode_escape')

            # if not receive any data from Arduino
            if re.search(regex1, data):
                logger.info('data nan')
                return ambient
        except BluetoothError as err:
            logger.error(err)
            Flag.inner_while = False
            if device == 1:
                Flag.sock_bluetooth1 = False
            elif device == 2:
                Flag.sock_bluetooth2 = False
            logger.debug('return ambient: {}'.format(ambient))
            return ambient

        data1 = data1 + data

        if re.search(regex, data1):
            m = re.search(regex, data1)
            line = m.group()
            list_values = line.split()
            ambient['sensor'] = list_values[0]
            ambient['temperature'] = list_values[2]
            ambient['humidity'] = list_values[3]
            data1 = ''
            # logger.debug('return ambient: {}'.format(ambient))
            return ambient

# def main():
#     # arduino = connect_serial(PORT,BD)
#     # sleep(1)
#     # arduino.write('1'.encode())
#     # sleep(2 )
#     # arduino.write('0'.encode())
#     while True:
#         arduino = connect_serial(PORT, BD)
#         send_signal('ON'.encode(), arduino)
#         sleep(2)
#         arduino = connect_serial(PORT, BD)
#         send_signal('OFF'.encode(), arduino)
#
#
# if __name__ == '__main__':
#     main()
