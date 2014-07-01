"""
Handles the interface to the service configuration files.
This interface needs defining - so does the service configuration file
format.

This module will be used to query and update services and their rules.
It is intended to abstract away how these are stored on the filesystem.

STATE:nearly complete
TODO:write subclasses for each condition type
     test
CONSIDERATIONS:
  how should it look?
"""

# import master_conf - find the service config files from the master_conf
import json
import os
import sys
# Why do I have to do crap like this? This is broken.
sys.path.append("..")
# In case we are in another directory wtf
sys.path.append(".")
from utils.misc import lmap, foldl, fil, find

# Throws an exception...
def jsonError(s = None):
    if s:
        raise Exception("Invalid json for services: %s" % s)
    else:
        raise Exception("Invalid json for services.")

class Condition:
    def __init__(self,cond):
        """
    Rather than being called by the subclass, we call the subclasses
    __init__ in this method using reflective abilities of Python.
        
    This allows us to take a json object that could represent ANY condition,
    turn it in to a condition, and then specialise it at run time.
        """
        # Verify
        if not 'type' in cond:
            jsonError()
        condType = cond["type"]
        if not issubclass(type(condType),basestring) or len(condType) == 0:
            jsonError()
        # We gonna reflect a bit.    
        # Get token (e.g PortCondition)    
        name = condType.capitalize()
        # Search global vars for it...
        if not name in globals():
            jsonError()
        condClass = globals()[name]
        # Gotta be a Condition.
        if not issubclass(condClass,Condition):
            jsonError()
        # Specialise dis guy.
        self.__class__ = condClass
        # It's like subclassing with reversed roles, man.
        condClass.__init__(self,cond)

# This class name can't be camel cased. Oops!
class Portequals(Condition):
    """A specialised condition that compares port numbers."""
    def __init__(self,cond):
        # Set our parameter
        if not "value" in cond:
            jsonError()
        value=cond["value"]
        if not type(value) is int:
            jsonError()
        self.value=value
        
    def __str__(self):
        return ("Port equality on port: " + str(self.value))

class Action:
    validActions = [
        'ACCEPT',
        'DROP',
        'REJECT'
    ]

    def __init__(self,act):
        # Not necessary..?
        if not issubclass(type(act),basestring) and not type(act) is unicode:
            jsonError("action is of type %s" % type(act))
        # Verify
        if not act in Action.validActions:
            jsonError()
        self.action=act    

    def __str__(self): return self.action
    
class Rule:
    def __init__(self,dic):
        """Turns part of a parsed json string in to a Rule"""
        # Verify
        if not type(dic) is dict:
            jsonError()
        if not 'action' in dic:
            jsonError()
        if not 'condition' in dic:
            jsonError()
        # Build
        self.action = Action(dic['action'])
        self.condition = Condition(dic['condition'])

    def __str__(self):
        return """
    Hi am Rule and this is me:
        Action: %s
        Condition: %s""" % (self.action, self.condition)

class Service:
    """Represents a service..."""
    def __init__(self,name,jsons):
        """Turns a json string in to a Service instance"""
        # Parse json
        dic = json.loads(jsons)
        # Verify json
        if not 'rules' in dic:
            jsonError()
        # Verify more
        if not type(dic['rules']) is list:
            jsonError()
        # Make rule list
        self.rules = lmap(Rule,dic['rules'])
        self.name = name 

        # Systemd service name this is associated with
        if 'systemd_service' in dic:
            self.systemd_service= dic['systemd_service']
        else:
            self.systemd_service = ""

    def __str__(self):
        # Man I just don't know how I should tab out stuff like this.
        if self.systemd_service:
            s = (" and I represent the systemd service: " + 
                self.systemd_service)
        return (("Hi I'm Service called %s%s and this are my Rules:" % 
            (self.name,s)) + 
                foldl(lambda acc,r: acc + str(r),
                      "",
                      self.rules))

def getDirServices(d):
    names = fil(lambda name: name.endswith(".service"),os.listdir(d))
    return lmap(lambda name: Service(name,open(os.path.join(d,name),'r').read()), names)

def getServices(serviceDirs):
    """
        serviceDirs is a list of directories
        This function parses all *.service files in these directories
        It creates a list of the service objects contained in each file
        Duplicate services are filtered out:
            services with the same name or same non-"" systemd_service are considered duplicates
            services earlier in serviceDirs are given priority: e.g. if service foo appears in serviceDirs[0] and in serviceDirs[1], then the instance in serviceDirs[0] will be used
    """
    # Get all services and concatenate the lists
    services = foldl(lambda acc,l: acc+l,
             [],
             lmap(getDirServices,serviceDirs))
    return foldl(lambda acc,s:
            # LOL what retard made this if syntax holy shit this language sucks hahaha
            acc 
            if find(lambda service: service.name == s.name or
                        service.systemd_service == s.systemd_service,
                    acc) 
            else acc+[s],
        [],
        services)

if __name__ == "__main__":
    # Test some stuff?
    a_service = """
{
  "systemd_service": "httpd.service",
  "rules": [
    { 
      "action":"ACCEPT",
      "condition": {
        "type": "portequals",
        "value": 80
      }
    },
    { 
      "action":"DROP",
      "condition": {
        "type": "portequals",
        "value": 81
      }
    }
  ]
}
"""
    print(Service("httpd",a_service))
