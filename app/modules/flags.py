# True -> correct
# False -> something is wrong

class Flag(object):
    connect_db = True
    serial = True
    sock_bluetooth1 = True
    sock_bluetooth2 = True
    inner_while = True
    rabbit_cnx_relay_state = True


class Var(object):
    STACK_STATE = []
    RELAY_STATE = 'empty'


    def get_relay_state(self):
        return self.RELAY_STATE
