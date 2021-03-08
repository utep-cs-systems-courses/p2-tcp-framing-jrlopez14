#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from message_handler import send_message, receive_message

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        # print('Connected by', addr)

        request = receive_message(conn)

        if request == "Send":
            file_name = receive_message(conn)
            if os.path.isfile(file_name)_:
                send_message(conn, b"Error")
            else:
                send_message(conn, b"Okay")
                fd = os.open(file_name, os.O_CREAT | os.O_WRONLY)
                os.write(fd, recieve_message(conn).encode())
                os.close(fd)
                send_message(conn,b"Complete")
        else:
            os.write(1, "Invalid Request!".encode())
        conn.shutdown(socket.SHUT_WR)


