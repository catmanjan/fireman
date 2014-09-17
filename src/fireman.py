#!/usr/bin/python

import os
import signal
import sys
import argparse
import time
import logging
import threading
from core import core_api as core
from services import servicedaemon as daemon

logging.basicConfig(filename='fireman.log',level=logging.DEBUG)

parser = argparse.ArgumentParser(description=
                                 """Help screen for fireman.
                                 fireman is a high level management tool
                                 for configuring firewall rules.
                                 It uses a responsive daemon to listen for
                                 services and applies/removes rules
                                 accordingly."""
                                 )
parser.add_argument('-v', '--version', action='version', version="""
                    release 0.1""")
parser.add_argument('-vi', '--view', help="""View either rules or services
                    saved in fireman, usage: rules, services.""")
parser.add_argument('-as', '--addservice', help="""
                    Add a custom service, usage: -as [name]""")
parser.add_argument('-rs', '--removeservice', help="""Removes a custom
                    service, usage: -rs [name]""")
parser.add_argument('-rr', '--removerule', nargs=2, help="""
                    Removes a firewall service, usage: -rr [service] [id]"""
                    )
parser.add_argument('-s', '--service', default='default_service', help=
                    """All firewall rules must have an associated service
                    , usage: -s [name], default = default_service"""
                    )
parser.add_argument('-i', '--ip', default='0.0.0.0', help=
                    """Specify an ip address for a firewall rule
                    , usage: -i [address], default = 0.0.0.0"""
                    )
parser.add_argument('-p', '--port', type=int, default='80', help=
                    """Specify a port for a firewall rule, usage: -p [port]
                    , default = 80"""
                    )
parser.add_argument('-a', '--action', default='deny', help=
                    """Specify an action for a firewall rule, usage: -a
                    [ACTION], options are: allow and deny, default = deny"""
                    )
parser.add_argument("control", nargs='?', help=
                    """Control argument, usage: start, stop or refresh"""
                    )
args = parser.parse_args()

# Path to a lock file which contains the process ID of a running fireman
# daemon. If it exists, another daemon should not be created until the
# current one is stopped.
_daemon_pid_file_path = "/tmp/firemandaemon.pid"

def pid_is_running(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

# Below is the parsing logic for removing a service.
if (args.removeservice is not None):
    check_rm = args.removeservice
    check_rm_lower = check_rm.lower()
    service_list = core.get_services()
# First check for any services with the same service
# name you are trying to add, check for lower or uppercase variants.
    if (any(check_rm_lower == val.lower() for val in service_list)):
        print("""TODO Call the API Function here to
              remove 'check_rm' from the list of services."""
              )
        # TODO Call the API Function here to remove 'check_rm'
        # from the list of services. Also will need to have any
        # firewall rules associated with this service change
        # their associated service to the 'default_service'.
    else:
        print("The service " + check_rm + " doesn't exist.")

# Below is the parsing logic for adding a new service.
if (args.addservice is not None):
    check = args.addservice
    check_lower = check.lower()
    service_list = core.get_services()
    # First check for any services with the same service name you are trying
    # to add, check for lower or uppercase variants.
    if (any(check_lower == val.lower() for val in service_list)):
        print("""The service name " + check + " is already being used
              , please choose another."""
              )
    else:
        print("""TODO Call the API Function here
              to add 'check' to the list of services."""
              )
        # TODO Call the API Function here to add
        # 'check' to the list of services.

# Below is the parsing logic for adding a new firewall rule.
temp_service = args.service
temp_ip = args.ip
temp_port = args.port
temp_action = args.action
# TODO: Call API function to add a new firewall rule here.
# For now there are 3 parameters to add a new firewall rule:
#					associated service, ip, port, action
# Each rule will automatically be given an ID in the core, which
# can be looked up using the CLI. This ID is used to modify and delete rules.

# Below is the parsing logic for removing a firewall rule.
if (args.removerule is not None):
    temp = args.removerule[0]
    temp_id = args.removerule[1]
    service_list = core.get_services()
    # First stage is to check if the service name even exists.
    temp_lower = temp.lower()
    if (any(temp_lower == val.lower() for val in service_list)):
        # Now try to remove the rule from the associated service.
        # Or catch any errors (which means the
        # service didn't have this rule ID)
        try:
            print("""TODO Call API function to remove rule.
                  This requires a service and an ID."""
                  )
            # TODO Call API function to remove rule.
            # This requires a service and an ID.
        except Exception as e:
            print("This rule ID doesn't exist for this service.")
    else:
        print("""This service " + temp + " does not exist
              , unable to remove rule."""
              )

# Below is the parsing logic of some more general arguments.
if (args.view == "rules"):
    print("Rules:")
    # TODO call API to print current rules saved
    # in Fireman and their associated services.
elif (args.view == "services"):
    print("Services:")
    # TODO call API to print current services saved in Fireman.
elif args.view:
    print("Incorrect usage of -vi, please check usage in help -h.")

# Below is the logic for the parsing of the control arguments.
if (args.control == "start"):
    """ Start service listener daemon in it's own thread.
    """
    core.set_master_config("core/master.conf")

    if os.path.isfile(_daemon_pid_file_path):
        with open (_daemon_pid_file_path, "r") as pid_file:
            pid = int(pid_file.read().replace('\n', ''))
            logging.debug("fireman daemon had already started! (PID %s)" % pid)
            print "fireman daemon had already started! (PID %s)" % pid
    else:
        core.get_lock()
        programs = core.get_service_names()
        core.release_lock()

        # JM: This list seems to have to be the same length as programs
        # Need to confirm with Jack what this is meant to be...
        pids = [ -1 ] * len(programs)

        logging.debug("fireman daemon started.")
        print "fireman daemon started."

        daemon.runDaemon(programs, pids)

elif (args.control == "stop"):
    """ Ask service listener daemon to stop responding to service triggers.
    """
    logging.debug("Trying to stop fireman daemon.")
    
    # No PID file found, daemon is not running
    if not os.path.isfile(_daemon_pid_file_path):
        logging.debug("fireman daemon not started yet!")
        print "fireman daemon not started yet!"
    else:
        # Read PID from file
        with open (_daemon_pid_file_path, "r") as pid_file:
            # Convert PID to int for kill
            pid = int(pid_file.read().replace('\n', ''))

            logging.debug("fireman daemon PID %s, attempting to shut down." % pid)
            print "fireman daemon PID %s, attempting to shut down." % pid

            # Send a quit signal to the daemon process
            if pid_is_running(pid):
                os.kill(pid, signal.SIGQUIT)

            # Give the daemon time to die
            time.sleep(1)

            # Check and confirm that the process is not running, remove temp file
            if pid_is_running(pid):
                logging.debug("Sent quit signal to fireman daemon but it failed!")
                print "Sent quit signal to fireman daemon but it failed!"
            else:
                os.unlink(_daemon_pid_file_path)

                logging.debug("fireman daemon successfully shut down.")
                print "fireman daemon successfully shut down."

elif (args.control == "refresh"):
    print ("Refreshing fireman rules.")

elif args.control:
    # If argument is non empty and not one of the above,
    # refer user to the usage in help.
    print("Invalid control command, please see help for usage.")
