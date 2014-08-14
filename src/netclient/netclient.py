#!/bin/python2

import sys
import socket
import ssl

def connectTo(server,port,certdir):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    myssl = ssl.wrap_socket(s,ca_certs=certdir,cert_reqs=ssl.CERT_REQUIRED)
    myssl.connect((server,port))
    return myssl

if __name__ == "__main__":
    s = connectTo("localhost",7777,"certs/cert.crt")
    s.send("Hello server!")
    print(s.recv(1024))
    
    
