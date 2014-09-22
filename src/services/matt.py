#!/usr/bin/python2.7
# TODO add error checking/doc strings
# figure out when to lock core
# how the fuk to import?
# get emitter isnt working. am i sure tmpname is ok to use?
# catch all kill signals?

import systemd.journal as journal
import logging
import select
import os
import sys

sys.path.append("core")
import core_api as core


global j
global services
global journal_fd
global core_fd


def update_services():
    global services
    global j

    # Re-initialise
    services = {}
    j = journal.Reader()
    j.this_boot()
    j.this_machine()
    # Only listen to messages from init. It's trustworthy.
    j.add_match(_PID="1")
    logging.debug("Getting services.")
    service_tuples = core.get_service_names()
    for name,systemd_name in service_tuples:
        logging.debug("Service found. Name: " + name + ", systemd name: "
                      + systemd_name)
        # Store the service information
        services[systemd_name] = name
        # Add a filter. This is the efficient place to filter.
        j.add_match(UNIT=systemd_name)

def startup():
    global journal_fd
    global core_fd

    logging.debug("Listener started. Getting service list.")

    core.set_master_config("core/master.conf")
    # These two actions must occur "atomically"
    core.get_lock()
    update_services()
    core_fd = core.get_service_emitter()
    core.release_lock()
    journal_fd = j.fileno()

def cleanup():
    global j
    core.get_lock()
    core.drop_service_emitter(core_fd)
    core.release_lock()
    j.close()

def body():
    global j
    global services
    global core_fd
    global journal_fd

    ready = []

    logging.debug("Entering listener body. Going to select")
    while ready == []:
        try:
            ready,_,_ = select.select([journal_fd,core_fd],[],[])
        except:
            pass

    for r in ready:
        # Process journal
        if r == journal_fd:
            logging.debug("New journal entries!")
            j.process()
            if(services != {}):
                for entry in j:
                    if entry['UNIT'] in services:
                        m = entry['MESSAGE']
                        logging.debug("Got journal message: " + m)
                        # Is this good? What if their output format changes?
                        action = m.split(None,1)
                        if action[0] == "Starting":
                            logging.debug("It's a starting message.")
                        elif action[0] == "Started":
                            logging.debug("It's a started message.")
                            core.start_service(services[entry['UNIT']])
                        elif action[0] == "Stopping":
                            logging.debug("It's a stopping message.")
                        elif action[0] == "Stopped":
                            logging.debug("It's a stopped message.")
                            core.stop_service(services[entry['UNIT']])
                        else:
                            logging.debug("Unknown message.")
                        
                    else:
                        logging.debug("This shouldn't happen. Does it matter?")

        # Check for core changes
        if r == core_fd:
            logging.debug("New services!")
            # We need to update services. First we must lock and read data.
            core.get_lock()
            while os.read(core_fd,1) != "":
                    pass
            update_services()
            core.release_lock()

logging.basicConfig(level=logging.DEBUG)
#try:
startup()
while True:
    body()
#except:
cleanup()
exit(0)
j.add_match(UNIT="httpd.service")

while True:
    for entry in j:
            s=entry['MESSAGE']
            ss = s.encode('ascii','ignore')
            print(entry['UNIT'].encode('ascii','ignore')  + ss)

core.release_lock()
