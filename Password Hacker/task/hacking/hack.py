import string
import sys
import socket
import itertools

args = sys.argv
address = (args[1], int(args[2]))

chars = list(string.ascii_lowercase) + [str(d) for d in range(10)]

with socket.socket() as client_socket:
    client_socket.connect(address)

    list_of_iters = []
    flag = True
    while flag:
        list_of_iters.append(chars)
        my_iter = itertools.product(*list_of_iters)
        for pwd in my_iter:
            message_bytes = ''.join(pwd).encode()
            client_socket.send(message_bytes)

            response = client_socket.recv(1024).decode()
            if response == "Connection success!":
                print(''.join(pwd))
                flag = False
                break
            elif response == "Too many attempts":
                exit(0)
