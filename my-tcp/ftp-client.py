#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time
sys.path.append("../lib")       # for params
import params
from message_handler import send_message, receive_message
from std_in import readline, readfile

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"

if sys.argv[0] = "Send":
    try:
        localfile = sys.argv[1]
        serverHost, serverPort = re.split(":", sys.argv[2])
        serverPort = 50001
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)
else:
    os.write(1, "Invalid command!".encode())
    sys.exit(1)
    
s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
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

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")

send_message(s,sys.argv[0].encode())
send_message(s,localfile.encode())
server_response = receive_message(s)
if server_response = "Okay":
    localfile_data = readfile(localfile)
    send_message(s,localfile_data.encode())
else:
    os.write(1, "File {} already exists!".format(localfile).encode())
s.close()
