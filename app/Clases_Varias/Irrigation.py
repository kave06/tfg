from app.model.nano import send_signal


class Irrigation:

    def __init__(self, start_hour, duration):
        self.start = start_hour
        self.duration = duration


    def start_irrigation(self):
        print('start irrigation')
        send_signal('ON'.encode())

    def stop(self):
        print('stop irrigation')
        send_signal('OFF'.encode())
