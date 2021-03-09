#! /usr/bin/env python3

import os

# Reads the next line entered by user.

curr = 0
ibuf = ""
sbuf = ""

def readline(fd = 0, limit = 100):
    global curr
    global ibuf
    global sbuf

    if ibuf == "":
        ibuf = os.read(fd,limit)
        sbuf = ibuf.decode()  
    line = ""
    while curr < len(sbuf): 
        line += sbuf[curr] # adds each character to line
        if sbuf[curr] == '\n': # if character is '\n' return line
            curr += 1
            return line
        curr += 1
        if curr == limit:  # if end of buffer is reached, read again.
            ibuf =  os.read(fd,limit)
            sbuf = ibuf.decode()
            curr = 0

    return ""

def readfile(filename):
    fd = os.open(filename, os.O_RDONLY)
    lines = ""
    line = readline(fd)
    while line != "":
        lines += line
        line = readline(fd)
    return lines
