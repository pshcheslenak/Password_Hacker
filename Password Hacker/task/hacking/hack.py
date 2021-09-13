import sys
import socket

args = sys.argv
address = (args[1], int(args[2]))

with socket.socket() as client_socket:
    client_socket.connect(address)

    message_bytes = args[3].encode()
    client_socket.send(message_bytes)

    response = client_socket.recv(1024).decode()
    print(response)
