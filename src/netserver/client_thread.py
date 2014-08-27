#!/usr/bin/python

import threading
import time
import json
import socket

exitFlag = 0

class client_thread (threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        while True:
            # data = self.client_socket.recv(1024) 
            obj = socket_recv(self.client_socket)
            print repr(obj)


def read_exactly(sock, buflen):
    data = ''
    while len(data) != buflen:
        data += sock.recv(buflen - len(data))
    return data

def peek(sock, buflen):
    data = sock.recv(buflen, socket.MSG_PEEK)
    return data

def socket_recv(sock):
    peekdata = peek(sock, 1024)
    if peekdata == '':
        raise ConnectionClosed
    sizepos = peekdata.find("\n")
    if sizepos == -1:
        raise MalformedMessage('Did not find CRLF in message %r' % peekdata)
    sizedata = read_exactly(sock, sizepos)
    read_exactly(sock, len("\n"))
    print sizedata
    try:
        size = int(sizedata)
    except ValueError:
        raise MalformedMessage(
            'size data %r could not be converted to an int' % sizedata)
    data = read_exactly(sock, size)
    return json.loads(data)

