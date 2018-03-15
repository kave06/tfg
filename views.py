import os
from flask import Flask, render_template, request
from flask_script import Manager
from flask_bootstrap import Bootstrap

from app.model.database import ambient_days
from app.model.webserver_client_socket import led_on_off
from app.modules.logger import create_log

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

APP_DIR = os.path.dirname(os.path.realpath(__file__))
logger_name = APP_DIR + '/prototipo.log'
logger = create_log(logger_name)


@app.route('/button')
def button():
    return render_template('base_left_buttons.html')


@app.route('/temperature')
def temperature():
    data_list1 = ambient_days(1, 'sensor1_per_hour')
    data_list2 = ambient_days(1, 'sensor2_per_hour')
    list_temp1 = data_list1[0]
    list_temp2 = data_list2[0]
    logger.info(list_temp1)
    logger.info(list_temp2)
    list_hour1 = data_list1[2]
    logger.info(list_hour1)
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
    logger.info(list_humi1)
    logger.info(list_humi2)
    list_hour1 = data_list1[2]
    logger.info(list_hour1)
    list_hour2 = data_list2[2]
    # logger.debug(list_hour2)

    return render_template('humidity.html', list_humi1=list_humi1, list_hour1=list_hour1,
                           list_humi2=list_humi2, list_hour2=list_hour2)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    state = request.form['irrigation_state']
    logger.info('state is: {}'.format(state))
    logger.info(state)
    led_on_off(state)
    return render_template('irrigation.html')


@app.route('/irrigation')
def irrigation():
    return render_template('irrigation.html')


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


if __name__ == '__main__':
    # app.run()
    manager.run()
