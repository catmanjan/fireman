""" Abstract Condition class, must be overridden to make conditions to match
    for the rule model
"""


class Condition(object):
    """ Generic class for Condition """

    def __init__(self):
        """ These conditions must be matched to trigger the action
            All values are optional, not all of these can be used
            together
        """
        # the -p option in iptables, tcp or udp
        self.protocol = None
        # the --sport option in iptables
        self.source_port = None
        # the --dport option in iptables
        self.destination_port = None
        # the -i option in iptables
        self.input_interface = None
        # the -o option in iptables
        self.output_interface = None
        # the -s option in iptables
        self.source_address = None
        # the -d option in iptables
        self.destination_address = None
