"""Implements an API for the core. The core does NOT run as a daemon,
   so any state is stored in files.

   See fireman/doc/core_notes for some notes.

   STATE:2/10
   TODO:
     Design API for adding/removing rules/services 
     get_service_names
     start_service
     stop_service
     refresh
     generate_default_conf
     add a global start/stop mechanism - what will this mean?
   CONSIDERATIONS:fireman/doc/core_notes
"""
import sys
import os
import threading
if os.name == "posix":
    import fcntl
    import signal
    import errno

# God damn it. This is really bad TODO
sys.path.append(".")
sys.path.append("..")

import config_parser as options
from utils.misc import lmap
# NOTE: servicedaemon has superseded servicelistener
# start_daemon has been updated accordingly
from services import servicedaemon as daemon
import services_conf

__all__ = [
    "start_daemon",
    "stop_daemon",
    "get_lock",
    "release_lock",
    "force_lock",
    "get_service_names",
    "start_service",
    "stop_service",
    "get_service_emitter",
    "drop_service_emitter",
    "refresh",
    "generate_default_conf",
    "set_master_config"
]

# If we have the core lock, the file is stored here.
# Internal.
_lock_fd = None

# Whether or not we are forcing the program (ignoring locks).
# Internal.
_force = False

# Maps pipe file objects to their filenames.
# The file is a named pipe that is used to signal events (see
#     get_service_emitter)
# Really, this should only ever contain one object, but why force it.
_emitters = {}


# TODO comment
# Internal. Use start_daemon() and stop_daemon().
_daemon_thread = None


# Flag to check whether the service listener has been asked to stop
# listening phase. If set to True during the monitor phase, the listener
# will terminate.
# Internal. Use start_daemon() and stop_daemon().
_stop_daemon = True

_service_list = None 

class LockedError(Exception):
    """Thrown whenever a function that requires the core lock is called
       if the core lock is not held, and forcing has not been enabled.
    """
    pass

def locked(f):
    def wrapper(*args,**kargs):
        global _lock_fd
        global _force
        if (not _lock_fd) and (not _force):
            raise LockedError("Core is locked. Get the lock or force it.")
        return f(*args,**kargs)
    return wrapper

@locked
def start_daemon():
    """ Start service listener daemon in it's own thread.
    """
    global _stop_daemon
    if not _stop_daemon:
        # Leave printing to the user's (CLI's) discretion
        # print("Daemon has already started.")
        return False
    
    # JM: To be replaced with a list of service names we are listening for
    programs = [ "httpd" ]
    # programs = get_service_names()
    
    # This list seems to have to be the same length as programs
    pids = [ -1 ]

    _daemon_thread = threading.Thread( 
        target = daemon.runDaemon,
        args = ( programs, pids, ) )
    _daemon_thread.daemon = True
    _daemon_thread.start()
    _stop_daemon = False
    return True

@locked
def stop_daemon():
    """ Ask the daemon to stop responding to service triggers.
    """
    global _stop_daemon
    _stop_daemon = True
    
    # Leave printing to the user's (CLI's) discretion
    # print "Asking daemon to stop."


def get_lock():
    """Attempts to wait and hold the core lock file. This is probably
       /var/www/fireman/lock, but can be set in the master
       configuration file.
       Throws - not guaranteed to be exhaustive:
         EnvironmentError - not posix compatible environment
         KeyError - required options don't exist in config file
         Exception - must specify config file using set_master_config
         IOError - error opening lock file or making directory
         ValueError - config file entry for lock_timeout not a number
         LockTimeoutError - system call timed out
       Locking is enforced, but only superficially. The lock can be
       forced open if the application wishes. The point of enforcing
       the lock is to make sure API users only ignore the lock on
       purpose. 
    """
    global _lock_fd
    # Locking is only provided on posix environment.
    if os.name != 'posix':
        raise EnvironmentError("File locking requires a posix environment.")
    if not _options:
        raise Exception("Set config file before calling other API functions.")
    if _lock_fd:
        raise IOError("Already have file lock. Release it first.")
    # Directory to look for/make lock file (probably /var/fireman).
    lock_dir = _options.get("lock_dir")
    lock_name = _options.get("lock_name")
    # We can continue without a lock timeout, so catch exception.
    try:
        lock_timeout = _options.get("lock_timeout")
        lock_timeout = int(lock_timeout)
    except KeyError:
        lock_timeout = None
    except ValueError:
        raise ValueError("Non-integer lock_timeout in config file.")
    # Make the directory if it doesn't exist.
    if not os.path.exists(lock_dir):
        os.makedirs(lock_dir)
    # Open the lock file.
    _lock_fd = open(os.path.join(lock_dir,lock_name),"w+")
    # Set up timeout.
    if lock_timeout:
        old_handler = signal.signal(signal.SIGALRM,
                                    lambda x,y:None)
        signal.alarm(lock_timeout)
    class LockTimeoutError(Exception):
        pass
    try:
        fcntl.flock(_lock_fd,fcntl.LOCK_EX)
    except IOError as e:
        if errno.errorcode[e.errno] == "EINTR":
            raise LockTimeoutError("Get lock timed out.")
        else:
            raise e

def release_lock():
    """Releases hold on core lock file. Throws an exception if the lock
       isn't already held. The lock will be released afterwards
       regardless.
       Lock is held in global _lockfd.
       Throws - not guaranteed to be exhaustive:
           EnvironmentError - non posix
           Exception - didnt set config file
           IOError - don't have lock
    """
    global _lock_fd
    if not _lock_fd:
        raise LockedError("You must get the lock before you release it.")
    if os.name != 'posix':
        raise EnvironmentError("File locking requires a posix environment.")
    if not _options:
        raise Exception("Set config file before calling other API functions.")
    fcntl.flock(_lock_fd,fcntl.LOCK_UN)
    _lock_fd.close()
    _lock_fd = None

def force_lock(force):
    """Notifies the API that you wish to ignore the lock.
       This is generally not recommended. If the lock is troubling you
       then try to resolve it.
       force
         True - enable lock forcing
         False - disable lock forcing 
    """
    global _force
    _force = force

@locked 
def get_services():
    """Returns a list of all services. Services class is defined in services_conf.py. Should I rearrange this? 
       Parses services on first time.
    """
    global _service_list
    if not _service_list:
        global _options
        default = _options.get("default_services")
        custom = _options.get("custom_services")
        _service_list = services_conf.getServices([custom,default])
    return _service_list

def get_service_names():
    """Returns a list containing pairs of the form (name,service),
       where name is the name of the service (to be passed to start_service
       and service is the systemd service it is bound to (such as httpd.service).
    """
    return lmap(lambda s: (s.name,s.systemd_service),get_services())
    #return lmap(lambda s: (s.name,s.systemd_service),get_services())

@locked
def start_service(service):
    """Adds all the rules associated with string:service using the
       underlying firewall software.
       TODO
       Throws:
    """
    # get all the rules associated with service from config file
    # remove them if they exist already, or check state of service
    # add rules to firewall
    pass

@locked
def stop_service(service):
    """Removes  all the rules associated with string:service using the
       underlying firewall software.
       TODO
       Throws:
    """
    # get all the rules associated with service from config file
    # removes rules from firewall
    # print "Removing rules associated with {0}.".format(service)
    pass

@locked
def get_service_emitter():
    """Returns a file. A byte of data will be written to
       this file whenever a new service is defined, or a service
       is undefined. This allows a service listener to adjust the
       events it listens for appropriately.
       
       The service listener is expected to grab the core lock, read out
       any data present on this file, grab the list of
       current services, then release the core lock.

       This function could have easily returned the name of the
       underlying pipe, instead of opening it for the user. However,
       opening it has some complications that should be hidden.

       A file object is returned NOT a file descriptor.
    """
    global _emitters
    # We will be using a named pipe. Deny non-posix environments.
    if os.name != 'posix':
        raise EnvironmentError("File locking requires a posix environment.")
    # Get the directory our emitters (named pipes) are to be stored.
    emitter_dir = _options.get("emitter_dir")
    # os.tempnam can be vulnerable to symlink attack.
    # It is okay to use with named pipes though.
    # Also, emitter_dir should be owned by room.
    pipe_name = os.tempnam(emitter_dir)
    # Make pipe. Only we (root) can read and write to it.
    os.mkfifo(pipe_name,0o600)
    # We don't want the open call to block (see fifo(7))
    try:
        fd = os.open(pipe_name,os.O_NONBLOCK|os.O_RDONLY)
    except:
        # Clean up, but reraise.
        os.unlink(pipe_name)
        raise
    # We want to return a file object, not a file descriptor.
    try:
        f = os.fdopen(fd)
    except:
        # Clean up, but reraise.
        os.close(fd)
        os.unlink(pipe_name)
        raise
    # When the user is done, we have to be able to clean up.
    # We need to be able to associate the file with its file name.
    # Because we used os.fdopen, f.name is not set correctly.
    # So, just store it in a dictionary.
    if f in _emitters:
        # Not sure how this would occur, but it shouldn't.
        raise Exception("File already associated with a name.")
    _emitters[f] = pipe_name 
    return pipe_name

@locked
def drop_service_emitter(fileobject):
    """fileobject must be a file returned by get_service_emitter.
       Closes fileobject, and cleans up (unlinks the FIFO)
    """
    pipe_name = _emitters[fileobject]
    del _emitters[fileobject]
    try:
        fileobject.close()
    except:
        # We really want to try to unlink the file.
        os.unlink(pipe_name)
        raise
    os.unlink(pipe_name)
    
@locked
def refresh():
    """Clears all rules from firewall. Reparses configuration file to
       and reincludes all the rules.
    """
    global _lock_fd
    global _force
    if (not _lock_fd) and (not _force):
        raise LockedError("Core is locked. Get the lock or force it.")
    pass

@locked
def generate_default_conf():
    """Imports all the scripts in default_conf_scripts directory
       (defined in master configuration file). Runs each import's
       generate function. This function returns a string containing
       the generated config file for the service with the same name
       as the script's file name. This config file is added to the
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
       rules. The default services' rules can be copied to another
       directory and modified by hand, to tailor the rules to the user.
       It is not recommended to edit the rules in place, as they will b
       destroyed if generate_default_conf() is called again.
    """
    pass

def set_master_config(filename):
    """Sets the core to use filename as its master configuration file.
       This file is parsed and the options will be used by other core
       functions. The options object is stored in the global _options.
       Throws - not guaranteed to be exhaustive:
           IOError - error opening file
           SyntaxError - config file syntax wrong
       This function does NOT require the core lock. All it does is
       parse a file. Also, the config defines the location of the lock
       file.
       Should this be exported?
    """
    global _options
    _options = options.Options(filename)

# Do some testing?
if __name__ == "__main__":
    print("We test core API.")
    config_filename = "../config/master.conf"
    try:
        set_master_config(config_filename)
    except IOError:
        print("Couldn't open \""+config_filename+"\". Are you root? Does"+
              " this file exist?")
    print("Here is the config file:")
    print(str(_options))

    # To see if lock works, run this script twice with "lock" as the arg
    if sys.argv[1] == "lock":
        print("Getting lock.")
        get_lock()
        print("Got lock.")
        while True:
            pass

    if sys.argv[1] == "unlock":
        print("Getting lock.")
        get_lock()
        print("Got lock. Releasing lock.")
        release_lock()
        while True:
            pass

    if sys.argv[1] == "lockpoll":
        while True:
            print("Getting lock.")
            get_lock()
            print("Got lock. Releasing lock.")
            release_lock()


    if sys.argv[1] == "services":
        get_lock()
        for s in get_services():
            print(s)
        print(get_service_names())
        release_lock()
