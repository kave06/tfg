from threading import Thread

from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_bootstrap import Bootstrap

from app.model.database import ambient_days
from app.model.webserver_client_socket_on_off import relay_on_off
from app.modules.logger import create_log

from app.model.rabbitMQ import start_consumer_ambient
from app.modules.flags import Var
from app.model.webserver_server_socket_state import launch_socket_relay_state
from app.modules.config import *

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

try:
    logger = create_log(webserver_logger)
except:
    logger = create_log(raspi_logger)


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
    relay_on_off(state)
    return render_template('irrigation.html', relay_state=Var.RELAY_STATE)


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


@app.route('/relay_state')
def relay_state():
    # logger.info(Var.RELAY_STATE)
    return jsonify(state=Var.RELAY_STATE)


if __name__ == '__main__':
    # app.run()
    # TODO delete consumer ambient
    # TODO change the name of modules to tools

    t1 = Thread(target=launch_socket_relay_state)
    t1.start()

    t2 = Thread(target=start_consumer_ambient)
    t2.start()

    manager.run()
