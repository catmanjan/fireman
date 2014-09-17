""" An interface for translating and executing rules using specific
    formats and firewall services
"""
import iptables
from iptables import Iptables
import xmltodict
import json
from utils import objtodict
import logging

def start_service(service):
    """
    (Service) -> None
    """
    iptables.delete_chain(service.name)
    iptables.add_chain(service.name)
    # TODO: need to get chain into rule
    for rule in service.rules:
        add_rule(rule, "iptables",  service.name, service.transport)

def stop_service(service):
    """
    (Service) -> None
    """
    iptables.delete_chain(service.name)

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

