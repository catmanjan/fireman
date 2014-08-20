#!/bin/python2
"""
This file is run as a daemon. It accepts requests for rule changes over
SSL (two party authentication). These are pushed to the server's firewall
using the core api. 
"""

import sys
import socket
import ssl

keyFile = "priv.key"
certFile = "cert.crt" 

def SSLListener(certFile,keyFile,authorisedUserDir=None):
    """Returns a listening socket that accepts ssl/tcp/ipv4
    """
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    myssl = ssl.wrap_socket(s,
                            keyfile=keyFile,
                            certfile=certFile,
                            server_side=True)
    myssl.bind(("localhost",7777))
    myssl.listen(64)
    return myssl

if __name__ == "__main__":
    print("Testing server")
    if sys.argv[1] == "sslsock":
        print("making listener")
        l = SSLListener(certFile,keyFile)
        print("got listener, accepting")
        s.addr = l.accept()
        print("accepted connection, sending hello")
        s.send("Hello client!")
        print("send message, trying to receive")
        print(s.recv(1024))
