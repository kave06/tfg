import socket

HOST, PORT = '89.128.192.144', 1100


def led_on_off(state: str):
    # data = " ".join(sys.argv[1:])
    # data = 'ON'.encode()
    data = state.encode()

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data))

        # Receive data from the server and shut down
        # received = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()
