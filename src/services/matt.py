#!/usr/bin/python2.7
# TODO add error checking/doc strings
# figure out when to lock core
# how the fuk to import?
# get emitter isnt working. am i sure tmpname is ok to use?
# catch all kill signals?
# maybe each systemd service can map to multiple fireman services?
# Filter seems to be not working? Systemd updates my file descriptor
#   even when filtered actions occur. Its fault. Wasting resources.

import systemd.journal as journal
import logging
import select
import os
import sys

sys.path.append("core")
import core_api as core

# Systemd journal object
global j
# Mapping from systemd service names to fireman service names 
global services
services = {} 
# File descriptor to select journal changes
global journal_fd
# File descriptor to select core changes
global core_fd
# Maps systemd service names to status
global service_statuses
service_statuses = {}


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
    read_journal()

def cleanup():
    global j
    try:
        core.get_lock()
        core.drop_service_emitter(core_fd)
        core.release_lock()
    except:
        pass
    j.close()

def read_journal():
    global j
    global services
    global core_fd
    global journal_fd
    j.process()
    if(services != {}):
        new_service_statuses = {}
        for entry in j:
            if entry['UNIT'] in services:
                m = entry['MESSAGE']
                logging.debug("Got journal message: " + m)
                # Is this good? What if their output format changes?
                action = m.split(None,1)
                if action[0] in ["Starting","Started",
                                 "Stopping","Stopped"]:
                    new_service_statuses[entry['UNIT']] = action[0] 
                    logging.debug("It's a " + action[0] + " message.")
                else:
                    logging.debug("Unknown message: " + entry['MESSAGE'])                        
            else:
                logging.debug("This shouldn't happen. Does it matter?")
        # We stored all changes. Now we check if we need to update.
        # This handles multiple changes well.
        core.get_lock()
        for s in new_service_statuses:
            status = new_service_statuses[s]
            if s in service_statuses:
                # Previous status of this service
                s_old = service_statuses[s]
            else:
                s_old = None
            if((status in ["Starting","Started"])
               and (s_old in ["Stopping","Stopped",None])):
                logging.debug("Asking core to start " + services[s])
                core.start_service(services[s])
            elif((status in ["Stopping","Stopped"])
               and (s_old in ["Starting","Started",None])):
                logging.debug("Asking core to stop " + services[s])
                core.stop_service(services[s])
            # Update the status
            service_statuses[s] = status
        core.release_lock()

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
            read_journal()
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
try:
    startup()
    while True:
        body()
except Exception as e:
    logging.debug("Service listener closing.")
    cleanup()
    raise
    exit(0)

