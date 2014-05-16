# Compile c program to print output of journal file
# Run c program with service input
# Parse results and output whenever they change

# Imports
from subprocess import Popen, PIPE
import sys


def compile():

    p1 = Popen(['gcc', '-o', 'parseJournal',
                '-lsystemd-journal', 'parseJournal.c'])
    p1.communicate()
    run()


def run():

    p2 = Popen(['./parseJournal'], stdout=PIPE)
    p2.communicate()

compile()