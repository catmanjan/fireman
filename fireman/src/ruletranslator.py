""" An interface for translating and executing rules using specific
    formats and firewall services
"""
from rte import iptables
from rte.iptables import Iptables
import xmltodict
import json
import objtodict


def add_rule(rule, service_name):
    """ Add the rules using the specified firewall
        (Rule, str) -> None
    """
    if service_name == "iptables":
        # create specific Iptables object
        rule = Iptables(rule)
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


def translate(rule, format):
    """ Translate the set of rules into a specified format
        (Rule, str) -> None
    """
    if format == "json":
        return json.dumps(objtodict.todict(rule))
    elif format == "xml":
        return xmltodict.unparse(objtodict.todict(rule))
    else:
        raise ValueError("Error: " + format + " is not yet supported")
