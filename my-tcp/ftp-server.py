#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
import framed_socket

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "ftp-server"
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
    f_socket = framed_socket.Framed_Socket(conn)
    
    if os.fork() == 0:      # child becomes server
        # print('Connected by', addr)
        request = f_socket.receive_message()
        os.write(1, "Recieved Message: {}\n".format(request).encode())
        if request == "Send":
            filename = f_socket.receive_message()
            os.write(1, "Received Message: {}\n".format(filename).encode())
            if os.path.isfile("./server_files/" + filename):
                os.write(1, ("Sent Message" + f_socket.send_message("Error: Duplicate File") + '\n'                ).encode())
            else:
                os.write(1, ("Sent Message: " + f_socket.send_message("Okay") + '\n').encode())
                fd = os.open("./server_files/" + filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, (f_socket.receive_message()).encode())
                os.close(fd)
                os.write(1, ("Created File: {}\n").format(filename).encode())
                f_socket.send_message("Complete")
        else:
            os.write(1, "Invalid Request!".encode())
        #conn.shutdown(socket.SHUT_WR)
