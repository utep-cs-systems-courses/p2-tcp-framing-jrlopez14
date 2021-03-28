#! /usr/bin/env python3

class Framed_Socket:
    def __init__(self, socket, limit = 100):
        self.socket = socket
        self.limit = limit
        self.sbuf = ""
    
    def send_message(self,message):
        bytes_sent = 0
        byte_array = str(len(message)).encode() + b':' + message.encode()
        message_sent = ""
        while len(byte_array):
            bytes_sent = self.socket.send(byte_array)
            message_sent += byte_array[:bytes_sent].decode()
            byte_array = byte_array[bytes_sent:]
        return message_sent

    def receive_message(self):
        if self.sbuf == "":
            self.sbuf = self.socket.recv(self.limit).decode()    
        message_start = self.sbuf.index(':')
        length_message = int(self.sbuf[:message_start])
        self.sbuf = self.sbuf[message_start+1:]
        message = ""
        while len(message) != length_message:
            if self.sbuf == "":
                self.sbuf = self.socket.recv(self.limit).decode()
            message += self.sbuf[0]
            self.sbuf = self.sbuf[1:]
        return message
