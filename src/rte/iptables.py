""" Interfaces with iptables to add, delete and search for rules using
    the Rule model and unique identifiers stored in comments
"""
import subprocess
from ..utils import objtodict
from action import Action
from chain import Chain
from collections import OrderedDict


class Iptables(object):
    """ An Iptables which holds iptables' rule model
        and deals with the interface between fireman and iptables
    """

    def __init__(self, rule):
        """ Make a new Iptables from a Rule object.
            (Iptables, Rule) -> None
        """
        # converts generic rule model conditions into commands for
        # iptables. This is ordered because certain arguments need to
        # be before others. Order the keys in the order the arguments
        # need to be added.
        self.condition_conversions = OrderedDict([('protocol', '-p'),
                                                ('source_port', '--sport'),
                                                ('destination_port',
                                                    '--dport'),
                                                ('input_interface', '-i'),
                                                ('output_interface', '-o'),
                                                ('source_address', '-s'),
                                                ('destination_address', '-d')])

        # the chain the rule is appended to (INPUT or OUTPUT)
        # set as INPUT on default
        self.chain = "INPUT"
        if rule.chain == Chain.INPUT:
            self.chain = "INPUT"
        elif rule.chain == Chain.OUTPUT:
            self.chain = "OUTPUT"

        # the action of the rule ie. what to do if the packet matches
        self.action = None
        if rule.action == Action.ACCEPT:
            self.action = "ACCEPT"
        elif rule.action == Action.DROP:
            self.action = "DROP"

        # matching criteria
        self.conditions = []
        for condition in rule.conditions:
            # creates a dict of each condition
            self.conditions.append(objtodict.todict(condition))
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
            args.extend(["-A", self.chain])
        else:
            # insert rule
            args.extend(["-I", self.chain, str(self.rule_number)])
        if self.action is not None:
            # if action is specified add this
            args.extend(["-j", self.action])

        # convert each condition to an iptables argument
        for condition in self.conditions:
            # run through each key of conversions, this is to retain
            # ordering
            for key in self.condition_conversions:
                if key in condition:
                    args.extend([
                                self.condition_conversions[key],
                                str(condition[key])])

        # add rule id as comment
        args.extend(["-m", "comment", "--comment", self.rule_id])

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
    if rules is None:
        return
    # the first column stores the rule number - filter by this
    # we will only delete the first rule, since the index will change
    # after that, and we do not expect there to be multiple rules
    # with the same id
    index = filter(rules, 1)[0]
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
        # grep returns failure if it can't find anything
        return None
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
