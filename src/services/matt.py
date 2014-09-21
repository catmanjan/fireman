#!/usr/bin/python
# TODO add error checking/doc strings
# figure out when to lock core
# how the fuk to import?

import systemd.journal as journal
import logging
import select
import os

global j
global services
global journal_fd
global core_fd


def update_services():
    # Re-initialise
    services = {}
    j = journal.Reader()
    j.this_boot()
    j.this_machine()
    # Only listen to messages from init. It's trustworthy.
    j.add_match(_PID="1")
    service_tuples = core.get_service_names()
    for name,systemd_name in service_tuples:
        logging.debug("Service found. Name: " + name + ", systemd name: "
                      + systemd_name)
        # Store the service information
        services[systemd_name] = name
        # Add a filter. This is the efficient place to filter.
        j.add_match(UNIT=systemd_name)

def startup():
    logging.debug("Listener started. Getting service list.")
    # These two actions must occur "atomically"
    core.get_lock()
    update_services()
    core_fd = core.get_service_emitter()
    core.release_lock()
    journal_fd = j.fileno()

def cleanup():
    core.drop_service_emitter(core_fd)
    j.close()

def body():
    logging.debug("Entering listener body. Going to select")
    ready = select.select([journal_fd,core_fd])
    for r in ready:
        if r == journal_fd:
            logging.debug("New journal entries!")
        if r == core_fd:
            logging.debug("New services!")
            # We need to update services. First we must lock and read data.
            core.get_lock()
            while os.read(core_fd,1) != "":
                    pass
            update_services()
            core.release_lock()

update_services()
j.add_match(UNIT="httpd.service")

for entry in j:
        s=entry['MESSAGE']
        ss = s.encode('ascii','ignore')
        print(entry['UNIT'].encode('ascii','ignore')  + ss)
