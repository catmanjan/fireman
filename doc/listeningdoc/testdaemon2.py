import os
import time

from datetime import datetime
from daemon import runner


class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        filepath = '/tmp/currenttime.txt'
        while True:
            f = open(filepath, 'w')
            f.write(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
            f.write("\n")
            f.close()
            time.sleep(10)


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
