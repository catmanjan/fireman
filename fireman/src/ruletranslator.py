from rte import iptables
from rte.iptables import Iptables
import xmltodict, json
import objtodict

def add_rule(rule, firewall_type):
    """ Add the rules using the specified firewall
        (Rule, str) -> None
    """
    if firewall_type == "iptables":
        # create specific Iptables object
        rule = Iptables(rule)
        # add rule to iptables
        rule.add_rule()
    else:
        raise ValueError("Error: " + firewall_type + " is not yet supported")

def delete_rule(rule_id, program):
    """ Delete the rule from the specified firewall, using the rule_id saved
        in the comments of the firewall rule
        (Rule, str) -> None
    """
    if firewall_type == "iptables":
        iptables.delete_rule(rule_id)
    else:
        raise ValueError("Error: " + firewall_type + " is not yet supported")

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