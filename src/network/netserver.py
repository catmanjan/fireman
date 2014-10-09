#!/usr/bin/env python

# run with: twistd -ny netserver.py
# or without -n to make it run in the background

# I couldn't get relative imports working, so i just
# copied the files from core into here. I assume these
# files will end up elsewhere anyway

from twisted.application import service, internet
from twisted.internet import reactor
from twisted.spread import pb
import network_rule # needed to get ReceiverRule registered with Jelly
import core_api

class Receiver(pb.Root):
    """
        Receives rules and adds them to the firewall
    """
    def remote_receiveRule(self, rule):
        # this currently doesn't work because we aren't applying
        # rules one at a time. Matt may need to implement apply_rule
        core_api.apply_rule(rule)
    def remote_shutdown(self):
        reactor.stop()

application = service.Application("client")
factory = pb.PBServerFactory(Receiver())
internet.TCPServer(8800, factory).setServiceParent(
    service.IServiceCollection(application))