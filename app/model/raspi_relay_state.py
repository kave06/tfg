# import os
# from time import sleep
# from datetime import datetime
#
# try:
#     from app.model.nano import connect_serial, read_serial_state
#     from app.model.rabbitMQ import connect_queue_sender, send_queue_relay
#     from app.modules.logger import create_log
#     from app.modules.flags import Flag
#     from app.modules.config import *
#     from app.modules.manage_file import write_file
# except ImportError:
#     from model.nano import connect_serial, read_serial_state
#     from model.rabbitMQ import connect_queue_sender, send_queue_relay
#     from modules.logger import create_log
#     from modules.flags import Flag
#     from modules.config import *
#     from modules.manage_file import write_file
#
#
# APP_DIR = os.getcwd()
# logger_name = APP_DIR + '/../logs/prototype'
# logger = create_log(logger_name)
#
# def relay_state_______():
#     path = os.getcwd()
#     file = path + '/logs/relay_state'
#     print(file)
#     while True:
#
#         ser = connect_serial(serial_port, serial_bd)
#         cnx = connect_queue_sender()
#
#         while Flag.serial and cnx.is_open:
#             state = read_serial_state(ser)
#             # logger.debug(state)
#             send_queue_relay(cnx, state)
#             write_file(file, '{} {}'.format(datetime.now(), state))
#             sleep(1)
#
#         try:
#             # cnx.close()
#             ser.close()
#         except Exception as err:
#             logger.error(err)
#
#         Flag.serial = True
