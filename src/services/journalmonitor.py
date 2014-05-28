# Compile c program to print output of journal file
# Run c program with service input
# Parse results and output whenever they change

# Imports
from subprocess import Popen, PIPE
import sys


def compile():

    p1 = Popen(['cc', '-o', 'parseJournal',
                'parseJournal.c', '-lsystemd-journal'])

    p1.communicate()
    run()


def run():

    p2 = Popen(['./parseJournal'])
    p2.communicate()

compile()
