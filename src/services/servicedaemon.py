# https://pypi.python.org/pypi/python-daemon/

from daemon import runner
from subprocess import Popen, PIPE
import datetime
import time
import sys

# Bad, but works for now. Sets path in order to import core
sys.path.append("..")
import core

# programs is a list of the process names to track
# PIDCache is a list of the process IDs associated with these processes
programs = []
PIDCache = []


def check_process_id(program):

    """ Check if an input program is running if it is, return PID,
        if not, return -1
    """
    # Uses the Popen functionality to simulate terminal commands
    # 'ps aux' returns a list of running daemons
    p1 = Popen(['ps', 'aux'], stdout=PIPE)
    # grep the list to find the program you want
    p2 = Popen(['grep', program], stdin=p1.stdout, stdout=PIPE)
    # Output the 11th column - in this case, the service command
    p3 = Popen(['awk', '{print $11}'], stdin=p2.stdout, stdout=PIPE)

    # Close the unnecessary open pipes
    p1.stdout.close()
    p2.stdout.close()

    # Get the output of the last pipe, and put it in a character array
    grepCheck = p3.communicate()[0]
    # Split the character array based on the newline character
    # Put the results in a list
    # Remove the last value of the list as it will always be a blank line
    processList = grepCheck.split('\n')[:-1]
    # Filter out the processes created by
    # running this program, calling grep, and calling sudo
    grepFiltered = [v for v in processList if not v.startswith('grep')]
    pythonFiltered = [v for v in grepFiltered if not v.startswith('python')]
    sudoFiltered = [v for v in pythonFiltered if not v.startswith('sudo')]

    # if the list is empty, return 0
    if not sudoFiltered:
        return -1

    # Now we have a filtered list of the commands for each process
    # We can use this to get a more accurate output from grep

    # TODO: Currently only returns PID of first service in list
    #       Need to make program return PID of all services as a list

    # Use the list of commands to output PIDs
    p1 = Popen(['ps', 'aux'], stdout=PIPE)
    p2 = Popen(['grep', sudoFiltered[0]], stdin=p1.stdout, stdout=PIPE)
    p4 = Popen(['awk', '{print $2}'], stdin=p2.stdout, stdout=PIPE)
    # Just get the first value for now - will upgrade later
    p5 = Popen(['head', '-n1'], stdin=p4.stdout, stdout=PIPE)

    # Close unused pipes
    p1.stdout.close()
    p2.stdout.close()
    p4.stdout.close()
    # put the output from p5's pipe into output as a tuple
    output = p5.communicate()
    p5.stdout.close()

    # take just the head of the tuple
    head = output[0]
    # remove the newline character
    PID = head[:-1]
    return PID


class Daemon():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/serviceListener.pid'
        self.pidfile_timeout = 5

    def run(self):
        timer = 1                 # Wait time before checking for changes
        PIDList = list(PIDCache)  # Temp list for PID updates

        # tell core that the daemon has started
        _stop = False
        while(not core.core_api._stop_daemon):
            x = 0
            time.sleep(timer)
            for program in programs:
                # See if the process is running
                PIDList[x] = (check_process_id(program))
                # If value is different, state of process has changed
                if (PIDList[x] != PIDCache[x]):
                    # check if process has gone up
                    if (PIDList[x] > 0):
                        # get current time to write to log file
                        now = datetime.datetime.now()
                        currentTime = datetime.time(now.hour, now.minute,
                                                    now.second)

                        # Prints to be replaced by log file script
                        # print ("'" + program + "'" +
                        #        " started - \n\tTime: %s \n\tPID: %s "
                        #        % (currentTime, PIDList[x]))
                        PIDCache[x] = PIDList[x]

                        # TODO not sure if this is how the API is intended
                        core.core_api.start_service(program)
                    # or down
                    elif (PIDList[x] != -1):
                        # get current time to write to log file
                        now = datetime.datetime.now()
                        currentTime = datetime.time(now.hour, now.minute,
                                                    now.second)
                        # Prints to be replaced by log file script
                        # print ("'" + program + "'"
                        #        + " stopped - \n\tTime: %s"
                        #        % currentTime)
                        PIDCache[x] = PIDList[x]
                        # TODO not sure if this is how the API is intended
                        core.core_api.stop_service(program)
                x += 1


def runDaemon(programList, PIDs):

    """ Started by core to provide updates on specific processed going up and down.
        'programLists' is a list of the process names
        'PIDs' is a list of the process IDs associated with
        these names (-1 if not running)
        ([String], [int]) -> None
    """
    # Set global variables to input variables to enable use in daemon
    global programs
    global PIDCache
    programs = programList
    PIDCache = PIDs

    # Start the daemon
    daemonApp = Daemon()
    daemon_runner = runner.DaemonRunner(daemonApp)
    daemon_runner.do_action()


# Used for testing - needs calls to core commented out to function
# def Initialise():
#    programList = ["bluetooth"]
#    PIDs = ["-1"]
#    runDaemon(programList, PIDs)

# Initialise()
