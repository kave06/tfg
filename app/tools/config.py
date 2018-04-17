# [MySQL]
# mysql_host = 'gui.uva.es'
# mysql_port = 5584
mysql_host = 'localhost'
mysql_port = 3306
mysql_user = 'kave'
mysql_pass = 'hola'
mysql_db_name = 'prototipo'

# [bluetooth]
bluetooth_module1 = '98:D3:33:81:07:B3'
bluetooth_module2 = '98:D3:33:81:07:E8'
bluetooth_port1 = 1
bluetooth_port2 = 2

# [serial]
serial_port = '/dev/ttyUSB0'
serial_bd = 9600

# [rabbitMQ]
rabbit_user = 'kave'
rabbit_pass = 'hola'
rabbit_queue_ambient = 'sensors_data'
rabbit_queue_relay_state = 'relay_state'
# TODO check vatiables
# rabbit_callback_ambient = 'callback_ambient'
# rabbit_callback_relay_state = callback_relay_state()
rabbit_host = '157.88.58.134'
rabbit_port = 5578

# [socket]
raspi_ip = '89.128.192.144'
webserver_ip = '157.88.58.134'
webserver_socket_port_relay_state_out = 5576
webserver_socket_port_relay_state_in = 1101
raspi_socket_port_on_off = 1100


name_logger = 'prototype'
webserver_logger = '/home/kave/1tfg/prototipo/tfg/app/logs/prototype'
raspi_logger = '/home/pi/1tfg/prototipo/tfg/app/logs/prototype'
