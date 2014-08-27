#!/bin/python2
"""
This file is run as a daemon. It accepts requests for rule changes over
SSL (two party authentication). These are pushed to the server's firewall
using the core api. 
"""

import sys
import socket
import ssl
from daemon import runner
import time
import client_thread

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


"""
    print("Testing server")
    if sys.argv[1] == "sslsock":
        print("making listener")
        l = SSLListener(certFile,keyFile)
        print("got listener, accepting")
        s.addr = l.accept()
        print("accepted connection, sending hello")
        s.send("Hello client!")
        print("send message, trying to recieve")
        print(s.recv(1024))
"""
class Daemon():
    """
        Daemon class that can be run as a daemon
        This class must have the following attributes:

            * `stdin_path`, `stdout_path`, `stderr_path`: Filesystem
              paths to open and replace the existing `sys.stdin`,
              `sys.stdout`, `sys.stderr`.

            * `pidfile_path`: Absolute filesystem path to a file that
              will be used as the PID file for the daemon. If
              ``None``, no PID file will be used.

            * `pidfile_timeout`: Used as the default acquisition
              timeout value supplied to the runner's PID lock file.

            * `run`: Callable that will be invoked when the daemon is
              started.
    """
    def __init__(self):
        """
            Set up the daemons paths
        """
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/serviceListener.pid'
        self.pidfile_timeout = 5

    def run(self):
        """
            This will be invoked when the daemon is started
        """
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        myssl = ssl.wrap_socket(s,
                                keyfile=keyFile,
                                certfile=certFile,
                                server_side=True)
        myssl.bind(("localhost",7777))
        myssl.listen(64)
        while True:
            #accept connections from outside
            (clientsocket, address) = s.accept()
            ct = client_thread.client_thread(clientsocket)
            ct.run()


def runDaemon():

    """ Started by core to provide updates on specific processed going up and down.
        None -> None
    """
    # Start the daemon
    daemonApp = Daemon()
    daemon_runner = runner.DaemonRunner(daemonApp)
    daemon_runner.do_action()

if __name__ == "__main__":
    runDaemon()
