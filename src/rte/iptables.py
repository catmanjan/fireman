""" Interfaces with iptables to add, delete and search for rules using
    the Rule model and unique identifiers stored in comments
"""
import subprocess
from ..utils import objtodict


class Iptables(object):
    """ An Iptables which holds iptables' rule model
        and deals with the interface between fireman and iptables
    """

    def __init__(self, rule):
        """ Make a new Iptables from a Rule object.
            (Iptables, Rule) -> None
        """
        # the target of the rule ie. what to do if the packet matches
        self.target = None
        if rule.target == 0:
            self.target = "ACCEPT"
        elif rule.target == 1:
            self.target = "DROP"

        # matching criteria
        self.conditions = rule.conditions
        # where to add this rule in iptables - ignored if None
        self.rule_number = rule.rule_number
        # unique identifier
        self.rule_id = rule.id

    def add_rule(self):
        """ Add Iptables rule to iptables
            (Iptables) -> None
        """
        # args will store arguments for iptables
        args = ["iptables"]
        if self.rule_number is None:
            # append rule
            args.extend(["-A", "INPUT"])
        else:
            # insert rule
            args.extend(["-I", "INPUT", str(self.rule_number)])
        if self.target is not None:
            # if target is specified add this
            args.extend(["-j", self.target])

        # add rule id as comment
        args.extend(["-m", "comment", "--comment", self.rule_id])
        #TODO: add conditions

        # will call iptables to add rules
        try:
            iptables_list = subprocess.check_call(args)
        except subprocess.CalledProcessError:
            print "error"

    def delete_rule(self):
        """ Delete the current rule
            (Iptables) -> None
        """
        # delete rule using id
        delete_rule(self.rule_id)


def delete_rule(rule_id):
    """ Delete an iptables rule using the rule_id stored in the
        comments of the rule
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
            iptables_list = subprocess.check_call(["iptables", "-D",
                                                   "INPUT", index])
        except subprocess.CalledProcessError:
            print "Error when deleting rule: " + iptables_list


def find(rule_id):
    """ Find an iptables rule using the rule_id stored in the comments
        of the rule
        (str) -> str
    """
    rules = ""
    # list the rules
    iptables_list = subprocess.Popen(["iptables", "-L",
                                      "--line-numbers"],
                                     stdout=subprocess.PIPE)
    try:
        # grep to find the rule, which is stored in the comments
        rules = subprocess.check_output(
            ["grep", "\/\* " + rule_id + " \*\/"],
            stdin=iptables_list.stdout,
            stderr=subprocess.STDOUT)
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
        rules_echo = subprocess.Popen(["echo", rule],
                                      stdout=subprocess.PIPE)
        try:
            # get the specified column using awk
            field = subprocess.check_output(["awk", "{print $" +
                                            str(column_index) + "}"],
                                            stdin=rules_echo.stdout,
                                            stderr=subprocess.STDOUT)
            rules_echo.wait()
            # remove unnecessary whitespace
            fields.append(field.strip())
        except subprocess.CalledProcessError:
            print "Error when filtering rules: " + field
    return fields
