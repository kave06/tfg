import os
from threading import Thread
from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_bootstrap import Bootstrap

from app.model.database import ambient_days
from app.model.webserver_client_socket import led_on_off
from app.modules.logger import create_log

from app.model.rabbitMQ import start_consumer_ambient, start_consumer_realy_state
from app.modules.flags import Var

from app.test_server_consumer import count_state

from time import sleep


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/app/logs/prototype_view'
logger = create_log(logger_name)

# print(RELAY_STATE)
# print('--------------------------------------------------')
# start_consumer()
# print('--------------------------------------------------')
# sleep(5)
# print(RELAY_STATE)

@app.route('/button')
def button():
    return render_template('app/basura/base_left_buttons.html')


@app.route('/temperature')
def temperature():
    data_list1 = ambient_days(1, 'sensor1_per_hour')
    data_list2 = ambient_days(1, 'sensor2_per_hour')
    list_temp1 = data_list1[0]
    list_temp2 = data_list2[0]
    # logger.info(list_temp1)
    # logger.info(list_temp2)
    list_hour1 = data_list1[2]
    # logger.info(list_hour1)
    list_hour2 = data_list2[2]
    # logger.debug(list_hour2)
    return render_template('temperature.html', list_temp1=list_temp1, list_hour1=list_hour1,
                           list_temp2=list_temp2, list_hour2=list_hour2)


@app.route('/humidity')
def humidity():
    data_list1 = ambient_days(1, 'sensor1_per_hour')
    data_list2 = ambient_days(1, 'sensor2_per_hour')
    list_humi1 = data_list1[1]
    list_humi2 = data_list2[1]
    # logger.info(list_humi1)
    # logger.info(list_humi2)
    list_hour1 = data_list1[2]
    # logger.info(list_hour1)
    list_hour2 = data_list2[2]
    # logger.debug(list_hour2)

    return render_template('humidity.html', list_humi1=list_humi1, list_hour1=list_hour1,
                           list_humi2=list_humi2, list_hour2=list_hour2)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    state = request.form['irrigation_state']
    logger.info('state is: {}'.format(state))
    # logger.info(state)
    led_on_off(state)
    return render_template('irrigation.html',relay_state=Var.RELAY_STATE)


@app.route('/irrigation')
def irrigation():
    return render_template('irrigation.html', relay_state=Var.RELAY_STATE)


# @app.route('/ambient/days/<int:days>')
# def ambient_days_views(days):
#     logger.info('ambient_days_view')
#     table = 'sensor1_per_hour'
#     series = ambient_days(days, table)
#     return jsonify(series)

@app.route('/')
def dashboard():
    data_list1 = ambient_days(1, 'sensor1_per_hour')
    data_list2 = ambient_days(1, 'sensor2_per_hour')
    list_temp1 = data_list1[0]
    list_temp2 = data_list2[0]
    logger.info(list_temp1)
    list_hour1 = data_list1[2]
    logger.info(list_hour1)
    list_hour2 = data_list2[2]
    logger.info(list_hour2)
    return render_template('temperature.html', list_temp1=list_temp1, list_hour1=list_hour1,
                           list_temp2=list_temp2, list_hour2=list_hour2)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result= a + b)


@app.route('/add')
def index():
    return render_template('index.html')


@app.route('/suma')
def blank():
    return render_template('index2.html')

if __name__ == '__main__':
    # app.run()
    t1 = Thread(target=start_consumer_realy_state)
    t1.start()
    t2 = Thread(target=start_consumer_ambient)
    t2.start()
    # t1 = Thread(target=count_state)
    # t1.start()

    manager.run()
