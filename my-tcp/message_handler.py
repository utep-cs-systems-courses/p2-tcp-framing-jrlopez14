#! /usr/bin/env python3


def send_message(socket,byte_array):
    bytes_sent = 0
    byte_array = str(len(message)).encode()+b':' + message
    while byte_array != []:
        bytes_sent = socket.send(byte_array)
        byte_array = byte_array[bytes_sent:]

sbuf = ""

def recieve_message(socket):
    global ibuf
    sbuf = socket.recv(100).decode()
    message_start  = sbuf.index(':')
    message = sbuf[message_start+1:]
    length_message = int(sbuf[message_start-1])
    if message == "":
        return ""
    while len(message) != length_message:
        if sbuf == "":
            sbuf = socket.recv(100).decode()
        message += sbuf[0]
        sbuf = sbuf[1:]
    return message    
    
    
