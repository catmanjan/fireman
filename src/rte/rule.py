""" A generic rule model that can translate to iptables rules and also can work
    with most other firewall services as well
"""


class Rule(object):
    """ A rule model that contains
         - an id field, which is a string.
         - an action, which can be: ACCEPT/DROP, or maybe more.
         - a list of conditions. The semantics are that if a packet matches all
           of these conditions, then the Rule's action will be taken, otherwise
           the rule will be skipped.
         - an optional rule number to choose where to insert the rule
    """

    def __init__(self, id, chain="INPUT", action, conditions=[]):
        """ Make a new Rule object
            (Rule, str, str, Action, [Condition]) -> None
        """
        self.id = id
        self.chain = chain
        self.action = action
        self.conditions = conditions
        self.rule_number = None

    def add_condition(new_condition):
        """ Adds new condition that needs to be matched for the Rule object
            (Rule, Condition) -> None
        """
        self.conditions.append(new_condition)
