from datetime import time, datetime

try:
    from app.model.nano import send_signal
except:
    from model.nano import send_signal



class Irrigation:

    def __init__(self, start_hour: datetime, end_hour: datetime):
        self.start = start_hour
        self.end = end_hour
        self.duration = end_hour - start_hour



    def start_irrigation(self):
        print('start irrigation')
        send_signal('ON'.encode())

    def stop_irrigation(self):
        print('stop irrigation')
        send_signal('OFF'.encode())
