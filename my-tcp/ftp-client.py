#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time, os
sys.path.append("../lib")       # for params
import params
import framed_socket
from std_in import readline, readfile

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "ftp-client"
if sys.argv[0] == "Send":
    try:
        localfile = sys.argv[1]
        serverHost, remoteFile = re.split(":", sys.argv[2])
        serverPort = 50001
    except:
        #print("Can't parse server:port from '%s'" % server)
        sys.exit(1)
else:
    sys.exit(1)

#localfile = "test.txt"
#serverHost = "127.0.0.1"
#serverPort = 50001
#remoteFile = "test1.txt"

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        #print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        #print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

# delay = float(paramMap['delay']) # delay before reading (default = 0s)
# if delay != 0:
#   print(f"sleeping for {delay}s")
#    time.sleep(delay)
#    print("done sleeping")

f_socket = framed_socket.Framed_Socket(s)
os.write(1, ("Sent Message: " + f_socket.send_message('Send') + '\n').encode())
os.write(1, ("Sent Message: " + f_socket.send_message(remoteFile) + '\n').encode())
server_response = f_socket.receive_message()
os.write(1, ("Recieved Messaged: " + server_response + '\n').encode())
if server_response == "Okay":
    localfile_data = readfile(localfile)
    f_socket.send_message(localfile_data)
    os.write(1, "Sent File: {} \n".format(localfile).encode())
else:
    os.write(1, "File {} already exists!\n".format(localfile).encode())
s.close()
