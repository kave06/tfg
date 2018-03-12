import socket
import sys

# HOST, PORT = '157.88.58.134', 5578
HOST, PORT = '89.128.192.144', 1100
# data = " ".join(sys.argv[1:])
data = 'ON'.encode()

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # sock.sendall(bytes(data + "\n", "utf-8"))
    sock.sendall(bytes(data))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
finally:
    sock.close()

print("Sent:     {}".format(data))
print("Received: {}".format(received))

