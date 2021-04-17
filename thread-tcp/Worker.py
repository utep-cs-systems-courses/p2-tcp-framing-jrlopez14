#! /usr/bin/env python3

import sys, os
import socket
from time import time
from threading import Thread, enumerate, Lock
import framed_socket

threadNum = 0
inTransfer = set()
transferLock = Lock()

class Worker(Thread):
    def __init__(self, conn, addr):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum)
        threadNum += 1
        self.conn = conn
        self.addr = addr

    def check_transfer(self,filename):
        global inTransfer
        global transferLock
        transferLock.acquire()
        if filename in inTransfer:
            transferLock.release()
            return False
        inTransfer.add(filename)
        transferLock.release()
        return True
    
    def end_transfer(self,filename):
        global inTransfer
        return inTransfer.remove(filename)
        
    def run(self):
        f_socket = framed_socket.Framed_Socket(self.conn)

        request = f_socket.receive_message()
        os.write(1, "Recieved Message: {}\n".format(request).encode())
        if request == "Send":
            filename = f_socket.receive_message()

            os.write(1, "Recieved Message: {}\n".format(filename).encode())
            if (self.check_transfer(filename) == False):
                os.write(1, ("File: {} is currently in transfer!".format(filename)).encode())
            elif os.path.isfile("./server_files/" +  filename):
                os.write(1, ("Sent Message" + f_socket.send_message("Error: Duplicate File") + '\n'                ).encode())
            else:
                os.write(1, ("Sent Message: " + f_socket.send_message("Okay") + "\n").encode())
                fd = os.open("./server_files/" + filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, (f_socket.receive_message()).encode())
                os.close(fd)
                os.write(1, ("Created File: {}\n").format(filename).encode())
                f_socket.send_message("Complete")
        else:
            os.write(1, "Invalid Request!".encode())
        self.conn.shutdown(socket.SHUT_WR)
