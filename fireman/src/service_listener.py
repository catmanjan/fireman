# Author: Jack Rutherford
# Project: Project Fireman
# Purpose: Monitor input processIDs to see when they go up and down
# Usage: python service_listener arg1 arg2 ...
# Usage Note: services input as keywords, not .service files.

# Imports
from subprocess import Popen, PIPE
import datetime
import time
import sys


# Check if an input program is running
# If it is, return PID
# If not, return 0
def checkPID(program):

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
        return 0

    # Now we have a list of the commands for each process
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


# Provide an update every time
# a process goes up or down
def Monitor_Procs(programs, PIDCache):

    y = 0
    timer = 3       # Wait time before checking for changes
    PIDList = []    # Temp list for PID updates
    # Populate the list
    for elements in PIDCache:
        PIDList.append(PIDCache[y])
        y += 1

    print "Monitor Phase: "
    while(1):
        try:
            x = 0
            time.sleep(timer)
            for program in programs:
                # See if the process is running
                PIDList[x] = (checkPID(program))
                # If value is different, state of process has changed
                if (PIDList[x] != PIDCache[x]):
                    # check if process has gone up
                    if (PIDList[x] > 0):
                        # get current time, print out results
                        now = datetime.datetime.now()
                        currentTime = datetime.time(now.hour, now.minute,
                                                    now.second)
                        print ("'" + program + "'" +
                               " started - \n\tTime: %s \n\tPID: %s "
                               % (currentTime, PIDList[x]))
                        PIDCache[x] = PIDList[x]
                    # or down
                    else:
                        # get current time, print out results
                        now = datetime.datetime.now()
                        currentTime = datetime.time(now.hour, now.minute,
                                                    now.second)
                        print ("'" + program + "'"
                               + " stopped - \n\tTime: %s"
                               % currentTime)
                        PIDCache[x] = PIDList[x]
                x += 1
        except KeyboardInterrupt:
            print "\nShutdown requested... exiting."
            sys.exit(0)


# Provide initial report of
# the state of input processes
def Initial():

    # Local declarations
    programs = sys.argv		# list of args - process names
    programs.pop(0)			# remove the first arg (program name)
    PIDCache = []			# list for PIDs
    x = 0					# simple counter

    print "Starting... Exit with '^C'"

    # Check for arguments
    if not programs:
        print "Error: No args given."
        print "Usage: 'python service_listener arg1 arg2 ...'"
        sys.exit(1)

    print "Initial Report: "
    for program in programs:
        # See if the process is running
        PIDCache.append(checkPID(program))
        # If 0 is returned, process not active.
        if (PIDCache[x] == 0):
            print ("'" + program + "'" + " not currently active.")
        else:
            print ("'" + program + "'" + " process ID is: " + PIDCache[x])
        x += 1

    # begin to monitor the input processes
    Monitor_Procs(programs, PIDCache)

Initial()