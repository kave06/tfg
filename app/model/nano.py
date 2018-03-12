import re
import bluetooth
from configparser import ConfigParser
from bluetooth import BluetoothSocket, RFCOMM, BluetoothError
from bluetooth import BluetoothSocket, RFCOMM
from time import sleep
from serial import Serial

from app.modules.flags import Flag
from app.modules.logger import create_log

logger = create_log('prototype')

config = ConfigParser()
config.sections()
config.read('config.ini')
config.sections()
# serial_config = config['serial']

PORT = '/dev/ttyUSB0'
BD = 9600


def connect_bluetooth(db_addr, port) -> BluetoothSocket:
    sock = bluetooth.BluetoothSocket(RFCOMM)
    # logger.debug(sock)

    try:
        sock.connect((db_addr, port))
        # sock.listen(2)
        logger.info('socket connection successful in device: {}'.format(db_addr))
    except BluetoothError as err:
        logger.error(err)
        logger.info('error in device: {}'.format(db_addr))
        if db_addr == '98:D3:33:81:07:B3':
            Flag.sock_bluetooth1 = False
        elif db_addr == '98:D3:33:81:07:E8':
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

        # logger.info('Close sock if it is open and wait 5s to open socket')
        # sleep(5)

    return sock


def connect_serial(port, baud) -> Serial:
    serial_cnx = ''
    try:
        serial_cnx = Serial(port, baud)
        logger.info('connect to serial')
    except:
        # logger.info(type(errors))
        logger.error('Error')

    return serial_cnx


def send_signal(signal: bytes):
    arduino = connect_serial(PORT, BD)

    sleep(1)
    logger.info(signal)
    signal2 = signal.decode()
    logger.info(signal2)
    logger.info(signal2 == 'ON')
    if signal2 == 'ON':
        try:
            arduino.write('1'.encode())
            logger.info('Led is ON')
            arduino.close()
        except:
            # logger.error(errors)
            logger.info('errors')
    elif signal2 == 'OFF':
        try:
            arduino.write('0'.encode())
            logger.info('Led is OFF')
        except:
            # logger.error(errors)
            logger.info('errors')
            arduino.close()


def read_nano_bluetooth(sock: BluetoothSocket, device: int) -> dict:
    logger.debug('reading arduino {}'.format(device))
    # TODO tuve q cambiar y poner el primer dígito de t en 1 o 2 xq me fallo a menor tmp
    regex = '(\d{1}\s\T:\s\d{1,2}\.\d{2}\s\d{2}\.\d{2}\s:H)'
    regex1 = 'nan'
    regex = re.compile(regex)
    regex1 = re.compile(regex1)
    data = ''
    data1 = ''
    ambient = dict(sensor=0, temperature=100.0, humidity=0.0)

    # logger.info(sock.getpeername())
    try:
        sock.getpeername()
    except BluetoothError as err:
        logger.error(err)
        Flag.inner_while = False
        if device == 1:
            Flag.sock_bluetooth1 = False
        elif device == 2 :
            Flag.sock_bluetooth2 = False
        logger.debug('return ambient: {}'.format(ambient))
        return ambient

    # logger.debug('Flag.nano_recv: {}'.format(Flag.nano_recv))
    # while Flag.nano_recv:
    while True:
        try:
            # data = sock.recv(1024).decode('utf-8')
            data = sock.recv(1024)
            data = data.decode('unicode_escape')
            # data = unicode(data, errors='ignore').decode('utf-8')
            # logger.info('data: {}'.format(data))
            # if not receive any data from Arduino
            if re.search(regex1, data):
                logger.info('data nan')
                return ambient
        except BluetoothError as err:
            logger.error(err)
            # Flag.nano_recv = False
            Flag.inner_while = False
            if device == 1:
                Flag.sock_bluetooth1 = False
            elif device == 2 :
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

    # sock.close()
    # # Flag.sock_bluetooth1 = False
    #
    # logger.debug('last return')
    # return ambient


def main():
    # arduino = connect_serial(PORT,BD)
    # sleep(1)
    # arduino.write('1'.encode())
    # sleep(2 )
    # arduino.write('0'.encode())
    while True:
        arduino = connect_serial(PORT, BD)
        send_signal('ON'.encode(), arduino)
        sleep(2)
        arduino = connect_serial(PORT, BD)
        send_signal('OFF'.encode(), arduino)


if __name__ == '__main__':
    main()
