import subprocess
import objtodict
from collections import OrderedDict

class Iptables:
    """ An Iptables which holds iptables' rule model
        and deals with the interface between fireman and iptables
    """
    
    def __init__(self, rule):
        """ Make a new Iptables from a Rule object.
            (Iptables, Rule) -> None
        """
        # add fields for the Iptables class using passed rule

    def add_rule(self):
        """ Add Iptables rule to iptables
            (Iptables) -> None
        """
        # not implemented yet
        raise NotImplementedError, "Adding rules is not yet available"
        return

        # will call iptables to add rules
        try:
            iptables_list = subprocess.check_call(["iptables", "-A", "INPUT"])
        except subprocess.CalledProcessError:
            print "error"

    def delete_rule(self):
        """ Delete the current rule
            (Iptables) -> None
        """
        # delete rule using id
        delete_rule(self.rule_id)

def delete_rule(rule_id):
    """ Delete an iptables rule using the rule_id stored in the comments of the rule
        (str) -> None
    """
    # search for the rule using id
    rules = find(rule_id)
    # the first column stores the rule number - filter by this
    indexes = filter(rules, 1)
    # for each rule with that id
    for index in indexes:
        try:
            # delete that rule
            iptables_list = subprocess.check_call(["iptables", "-D", "INPUT", index])
        except subprocess.CalledProcessError:
            print "Error when deleting rule: " + iptables_list

def find(rule_id):
    """ Find an iptables rule using the rule_id stored in the comments of the rule
        (str) -> str
    """
    rules = ""
    # list the rules
    iptables_list = subprocess.Popen(["iptables", "-L", "--line-numbers"], stdout=subprocess.PIPE)
    try:
        # grep to find the rule, which is stored in the comments
        rules = subprocess.check_output(["grep", "\/\* " + rule_id + " \*\/"], stdin=iptables_list.stdout, stderr=subprocess.STDOUT)
        iptables_list.wait()
    except subprocess.CalledProcessError:
        print "Error when finding rule: " + rules
    # split the output into a list
    return rules.splitlines()

def filter(rules, column_index):
    """ Filter rules by specified column index
        ([str], int) -> [str]
    """
    fields = []
    # filter the list of rules
    for rule in rules:
        rules_echo = subprocess.Popen(["echo", rule], stdout=subprocess.PIPE)
        try:
            # get the specified column using awk
            field = subprocess.check_output(["awk", "{print $" + str(column_index) + "}"], stdin=rules_echo.stdout, stderr=subprocess.STDOUT)
            rules_echo.wait()
            # remove unnecessary whitespace
            fields.append(field.strip())
        except subprocess.CalledProcessError:
            print "Error when filtering rules: " + field
    return fields