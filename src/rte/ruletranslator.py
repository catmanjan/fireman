""" An interface for translating and executing rules using specific
    formats and firewall services
"""
import iptables
from iptables import Iptables
import xmltodict
import json
from utils import objtodict
import logging
from core import services_conf

def start_service(service):
    """
    (Service) -> None
    """
    chain=u"fm_"+service.name
    iptables.delete_chain(chain)
    iptables.add_chain(chain)
    jump_rule = services_conf.Rule()
    jump_rule.action=chain
    my_cond = {}
    my_cond["type"]=u"Portequals"
    my_cond["value"]=service.port
    jump_rule.condition=services_conf.Condition(my_cond)
    # TODO: if service is called init or final, add at start or end
    add_rule(jump_rule, "iptables", "INPUT", service.transport)

    # A service doesn't really need rules.
    if hasattr(service,'rules'):    
        for rule in service.rules:
            add_rule(rule, "iptables", chain, service.transport)

def stop_service(service):
    """
    (Service) -> None
    """
    chain="fm_"+service.name
    jump_rule = services_conf.Rule()
    jump_rule.action=chain
    my_cond = {}
    my_cond["type"]=u"Portequals"
    my_cond["value"]=service.port
    jump_rule.condition=services_conf.Condition(my_cond)
    delete_rule(jump_rule,"iptables")
    iptables.delete_chain(chain)

def add_rule(rule, service_name, chain="INPUT", protocol="tcp"):
    """ Add the rules using the specified firewall
        (Rule, str) -> None
    """
    if service_name == "iptables":
        # create specific Iptables object
        rule = Iptables(rule, chain, protocol)
        # add rule to iptables
        rule.add_rule()
    else:
        raise ValueError("Error: " + service_name +
                         " is not yet supported")


def delete_rule_using_id(rule_id, service_name):
    """ Delete the rule from the specified firewall, using the
        rule_id saved in the comments of the firewall rule
        (str, str) -> None
    """
    if service_name == "iptables":
        iptables.delete_rule(rule_id)
    else:
        raise ValueError("Error: " + service_name +
                         " is not yet supported")


def delete_rule(rule, service_name):
    """ Delete the specified Rule object from the specified firewall
        service
        (Rule, str) -> None
    """
    if service_name == "iptables":
        # create specific Iptables object
        rule = Iptables(rule)
        # add rule to iptables
        rule.delete_rule()
    else:
        raise ValueError("Error: " + service_name +
                         " is not yet supported")


def translate(rule, format_name):
    """ Translate the set of rules into a specified format
        (Rule, str) -> str

        Currently supports format_name "json" or "xml"
    """
    if format_name == "json":
        return json.dumps(objtodict.todict(rule))
    elif format_name == "xml":
        return xmltodict.unparse(objtodict.todict(rule))
    else:
        raise ValueError("Error: " + format_name + " is not yet supported")

