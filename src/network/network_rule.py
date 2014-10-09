#!/usr/bin/env python

from twisted.spread import pb
import services_conf

class SenderRule(services_conf.Rule, pb.Copyable):
    """
        We need to make the object copyable which req
    """
    def getStateToCopy(self):
        """
            Here we send the object as a dictionary,
            and we have to set up action and condition to
            be sent in a particular way. This is due to it needing
            to serialise the objects even at lower level.
            This implementation will only work for PortEquals and while
            Rule only contains a Condition and Action object
        """
        d = self.__dict__.copy()
        # copy their dictionaries over
        d['action'] = self.action.__dict__.copy()
        d['condition'] = self.condition.__dict__.copy()
        # need to add type
        if isinstance(self.condition, services_conf.Portequals):
            d['condition']['type'] = unicode('portequals', 'utf8')
        return d

class ReceiverRule(pb.RemoteCopy):
    def setCopyableState(self, state):
        # add the action
        self.action = services_conf.Action(state['action']['action'])
        # add the condition
        self.condition = services_conf.Condition(state['condition'])

pb.setUnjellyableForClass(SenderRule, ReceiverRule)