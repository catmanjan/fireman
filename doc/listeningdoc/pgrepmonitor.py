# Author: Jack Rutherford
# Project: Project Fireman
# Purpose: Monitor processIDs to see when they go up and down

# Extension of monitor2 which enables command line args


from subprocess import Popen, PIPE
import time
import sys

programName = str(sys.argv[0])


def checkPID(program):

    p1 = Popen(['pgrep', '-f', program], stdout=PIPE)

    output = p1.communicate()
    print output
    head = output[0]
    if head is None:
        return 0
    else:
        PID = head[:-1]
        p2 = Popen(['pgrep', '-f', programName])
        output2 = p2.communicate()
        print output2
        head2 = output2[0]
        if head2 is None:
            print "HEAD2 = NONE"
            return PID
        else:
            PID2 = head2[:-1]
            if (PID == PID2):
                return 0
            else:
                return PID

    # pgrep commandMonitor.py and see if that equals PID. If so, return 0.


def Monitor_Process():

    timer = 3
    # program = 'bluetoothd'
    # args = sys.argv
    # args.pop(0)

    input = str(sys.argv[1])
    print input
    # for element in args:
    #    print element
    #    res = checkPID(element)
    #    print res

    # if (res == 0):
    # print ("'" + element + "'" + " not currently active.")
    # time.sleep(timer)
    # else:
    # print ("'" + element + "'" + " PID is: " + res)
    # time.sleep(timer)
    # continue

    while(1):
        # See if the process is running
        res = checkPID(input)
        # if res is 0 then program is not running so schedule it
        if (res == 0):
            print ("'" + input + "'" + " not currently active.")
            time.sleep(timer)
        else:
            print ("Process ID is: " + res)
            time.sleep(timer)
            continue

# start the program
Monitor_Process()