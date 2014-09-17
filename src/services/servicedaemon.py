# https://pypi.python.org/pypi/python-daemon/
"""
    Watches processes as they go up and down using a daemon
"""
# Dependencies: 
# yum install python-daemon

from daemon import runner
from subprocess import Popen, PIPE
import os
import sys
import datetime
import time
import sys
import logging

# Bad, but works for now. Sets path in order to import core
sys.path.append(".")
sys.path.append("..")
from core import core_api

# programs is a list of the process names to track
# PIDCache is a list of the process Ipython callDs associated with these processes
programs = []
PIDCache = []

# Set true to stop daemon at next chance
_stop_daemon = False

def check_process_id(program):
    """ Check if an input program is running if it is, return PID,
        if not, return -1
        (String) -> int

        Oliver's thoughts:
            - no error handling
    """
    # Uses the Popen functionality to simulate terminal commands
    # 'ps aux' returns a list of running daemons
    ps = Popen(['ps', 'aux'], stdout=PIPE)
    # grep the list to find the program you want
    grep = Popen(['grep', program], stdin=ps.stdout, stdout=PIPE)
    # Output the 11th column - in this case, the service command
    awk = Popen(['awk', '{print $11}'], stdin=grep.stdout, stdout=PIPE)

    # Close the unnecessary open pipes
    grep.stdout.close()

    # Get the output of the last pipe, and put it in a character array
    grepCheck = awk.communicate()[0]
    # Split the character array based on the newline character
    # Put the results in a list
    # Remove the last value of the list as it will always be a blank line
    processList = grepCheck.split('\n')[:-1]
    # Filter out the processes created by
    # running this program, calling grep, and calling sudo

    #grepFiltered = [v for v in processList if not v.startswith('grep')]
    #pythonFiltered = [v for v in grepFiltered if not v.startswith('python')]
    #sudoFiltered = [v for v in pythonFiltered if not v.startswith('sudo')]

    prefixes = ['grep', 'python', 'sudo']
    sudoFiltered = processList
    for prefix in prefixes:
        sudoFiltered = [v for v in sudoFiltered if not v.startswith(prefix)]

    # if the list is empty, return -1
    if not sudoFiltered:
        return -1

    # Now we have a filtered list of the commands for each process
    # We can use this to get a more accurate output from grep

    # TODO: Currently only returns PID of first service in list
    #       Need to make program return PID of all services as a list

    # Use the list of commands to output PIDs
    grep = Popen(['grep', sudoFiltered[0]], stdin=ps.stdout, stdout=PIPE)
    awk = Popen(['awk', '{print $2}'], stdin=grep.stdout, stdout=PIPE)
    # Just get the first value for now - will upgrade later
    first = Popen(['head', '-n1'], stdin=awk.stdout, stdout=PIPE)

    # Close unused pipes
    ps.stdout.close()
    grep.stdout.close()
    awk.stdout.close()
    # put the output from p5's pipe into output as a tuple
    output = first.communicate()
    first.stdout.close()

    # take just the head of the tuple
    head = output[0]
    # remove the newline character
    PID = head[:-1]
    return PID


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
    def __init__(self, programList=[], PIDs=[]):
        """
            Set up the daemons paths
        """
        self.PIDCache = PIDs
        self.programs = programList
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/serviceListener.pid'
        self.pidfile_timeout = 5

    def run(self):
        """
            This will be invoked when the daemon is started
        """
        # Write current process ID to a file for later use in shutting down
        # or detecting an already running daemon.
        pid = str(os.getpid())
        pidfile = "/tmp/firemandaemon.pid"
        file(pidfile, "w").write(pid)

        timer = 1                 # Wait time before checking for changes
        PIDList = list(self.PIDCache)  # Temp list for PID updates

        # tell core that the daemon has started
        _stop = False
        while(not _stop_daemon):
            x = 0
            time.sleep(timer)
            for processTuples in self.programs:
                program = processTuples[1]
                # See if the process is running
                PIDList[x] = (check_process_id(program))

                # If value is different, state of process has changed
                if (PIDList[x] != self.PIDCache[x]):
                    # check if process has gone up
                    if (PIDList[x] > 0):
                        # get current time to write to log file
                        now = datetime.datetime.now()
                        currentTime = datetime.time(now.hour, now.minute,
                                                    now.second)

                        # Prints to be replaced by log file script
                        logging.debug("%s started - \n\tTime: %s \n\tPID: %s"
                            % (program, currentTime, PIDList[x]))
                        self.PIDCache[x] = PIDList[x]
                        print 'starting '+str(processTuples) 
                        # TODO not sure if this is how the API is intended
                        core_api.start_service(processTuples[0])
                    # or down
                    elif (PIDList[x] != -1):
                        # get current time to write to log file
                        now = datetime.datetime.now()
                        currentTime = datetime.time(now.hour, now.minute,
                                                    now.second)
                        # Prints to be replaced by log file script
                        logging.debug("%s stopped - \n\tTime: %s"
                            % (program, currentTime))
                        self.PIDCache[x] = PIDList[x]
                        # TODO not sure if this is how the API is intended
                        core.core_api.stop_service(processTuples)
                x += 1

def runDaemon(programList, PIDs):
    """ Started by core to provide updates on specific processed going up and down.
        'programLists' is a list of the process names
        'PIDs' is a list of the process IDs associated with
        these names (-1 if not running)
        ([String], [int]) -> None
    """
    # programs is a list of the process names to track
    # PIDCache is a list of the process IDs associated with these processes
    programs = programList
    PIDCache = PIDs

    # Start the daemon
    daemonApp = Daemon(programs, PIDCache)
    daemon_runner = runner.DaemonRunner(daemonApp)
    daemon_runner.do_action()


# Used for testing - needs calls to core commented out to function
def main():
   programList = ["bluetooth"]
   PIDs = ["-1"]
   runDaemon(programList, PIDs)

if __name__ == '__main__':
    main()
