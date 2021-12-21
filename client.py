import socket
import time

HOST = '192.168.0.114'
PORT = 6666

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))


i = 0
o = 0
c = 125
w = 0
e_1 = 0
e_2 = 0


for x in range(1, 300): 
   #  client_socket.send(message.encode())
    message = '{} {} {} {} {} {} '.format(i, o, c, w, e_1, e_2)
    client_socket.send(message.encode()) 

    data = client_socket.recv(1024)
    time.sleep(1)

    i += 1
    o += 1
    c += 0.009
    if w < 40:
       w += 1
    e_1 += 1
    if e_1 == 6:
       e_1 = 0
    e_2 += 1
    if e_2 == 12:
       e_2 = 0


client_socket.close()
