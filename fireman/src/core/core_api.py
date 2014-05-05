# Lots of this code is just stubs for now.
# Many comments will be removed when the stubs are expanded.
# Config parser will parse whatever format we use.
# Main config file location will be set on installation.
# This will contain the location of services config folder(s).
#   (Probably /etc/fireman/services)

# import master_conf
# import service_conf 

 __all__ = [
    "get_lock",
    "release_lock",
    "get_service_names",
    "force_core",
    "start_service",
    "stop_service",
    "get_service_emitter",
    "refresh",
    "generate_default_conf"
]
# if __name__ ==... run tests?

# Whether or not we hold a lock on the core lock file.
# Internal.
_has_lock=False;
# Whether or not we are forcing the program (ignoring locks).
# Internal.
_force=False;
# Location of master config file on filesystem.
# Internal.
_master_conf="/etc/fireman/master.conf"

def get_lock():
    """Attempts to wait and hold the core lock file. This is probably
       /var/www/fireman/lock, but can be set in the master
       configuration file.
       Throws:
    """
    lock_file = core_conf.get("lock_file");
    if(!lock_file)
        pass# throw an exception
    else 
        pass# use system call to open lock file. throw exception if applic

def release_lock():
    """Releases hold on core lock file. Throws an exception if the lock
       isn't already held. The lock will be released afterwards
       regardless.
       Throws:
    """
    lock_file = core_conf.get("lock_file");
    if(!lock_file)
        pass# throw an exception
    else
        pass#use system call to unlock file

def get_service_names():
    """Returns a list containing string representations of all
       registered service names (this includes registered but
       stopped services). These names are fetched from service
       config files.
    """
    pass 

def force_core(mode):
    """Initiates or deinitiates core force mode. In force mode the lock
       file is ignored. This is not generally recommended. If a program
       uses the lock incorrectly it may be necessary.
       mode:
         True - set to force.
         False - remove force mode.
    """
    _force=mode;

def start_service(service):
    """Adds all the rules associated with string:service using the
       underlying firewall software.
       Throws:
    """
    # get all the rules associated with service from config file
    # remove them if they exist already, or check state of service
    # add rules to firewall
    pass

def stop_service(service):
    """Removes  all the rules associated with string:service using the
       underlying firewall software.
       Throws:
    """
    # get all the rules associated with service from config file
    # removes rules from firewall
    pass

def get_service_emitter():
    """Returns a file descriptor. A byte of data will be read to this
       descriptor whenever a new service is defined, or a service is
       undefined. This allows a service listener to adjust the events
       it listens for appropriately.
       
       The service listener is expected to grab the core lock, read out
       any data present on this file descriptor, grab the list of
       current services, then release the core lock.
    """
    pass

def refresh():
    """Clears all rules from firewall. Reparses configuration file to
       and reincludes all the rules.
    """
    pass

def generate_default_conf():
    """Imports all the scripts in default_conf_scripts directory
       (defined in master configuration file). Runs each import's
       generate function. This function returns a string containing
       the generated config file for the service with the same name
       as the scripts file name. This config file is added to the
       default_services directory.
       Example:
           Assume default_conf_scripts contains a file called 
             apache2.py.
           default_conf_scripts/apache2.py is imported. 
           apache2.generate() is called.
           The resulting string is stored in the file:
             default_services/apache2.conf.

       This creates a flexible and simple method for including default
       rules for common services. Rules in default_services are given
       lowest priority so that they do not conflict with user defined
       rules. The default services' rules can copied to another folder
       and modified by hand, to tailor the rules to the user. It is not
       recommended to edit the rules in place, as they will be
       destroyed if generate_default_conf() is called again.
    """
    pass

