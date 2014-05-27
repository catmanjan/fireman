#!/usr/bin/python

import argparse
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

# This variable is just a placeholder for now. I am waiting on an API call
# by Matthew to check if Fireman is applying any rules to iptables or not.
started = False

# Below is the parsing logic for removing a service.
if (args.removeservice is not None):
    check_rm = args.removeservice
    check_rm_lower = check_rm.lower()
    service_list = ["default_service"]  # TODO API call for a list of services
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
    service_list = ["default_service"]  # TODO API call for a list of services
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
    service_list = ["default_service"]
    # TODO call API function for a list of services ^^^ on line above.
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
    if (started):
        print("fireman is currently active.")
    else:
        started = True
        print("Starting fireman.")
        # TODO Call matthews API to start Fireman.

elif (args.control == "stop"):
    if not (started):
        print("fireman is not currently active.")
    else:
        started = False
        print ("Stopping fireman.")
        # TODO API call

elif (args.control == "refresh"):
    if not (started):
        print("""fireman is not currently active
              , please start fireman before refreshing."""
              )
    else:
        print ("Refreshing fireman rules.")
        # TODO API call

elif args.control:
    # If argument is non empty and not one of the above,
    # refer user to the usage in help.
    print("Invalid control command, please see help for usage.")
