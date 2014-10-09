#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb, jelly
from twisted.python import log
from twisted.internet import reactor
from network_rule import SenderRule

class Sender:
    """
        Sends a rule over the network
    """
    def __init__(self, rule):
        self.rule = rule

    def send_rule(self, obj):
        # sends rule over the network using a remote call
        # to remote_receiveRule which is in netserver.py
        d = obj.callRemote("receiveRule", self.rule)
        # add callback to check result
        d.addCallback(self.sent).addErrback(self.failed)

    def sent(self, response):
        print "rule arrived", response
        reactor.stop()

    def failed(self, failure):
        print "error during receiveRule:"
        if failure.type == jelly.InsecureJelly:
            print " InsecureJelly"
        else:
            print failure
        reactor.stop()
        return None

def main():
    dic2 = {'type': unicode('Portequals', 'utf8'), 'value': 80}
    dic = {'action':unicode('ACCEPT', 'utf8'), 'condition': dic2}
    rule = SenderRule(dic)

    sender = Sender(rule)
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    deferred = factory.getRootObject()
    deferred.addCallback(sender.send_rule)
    reactor.run()

if __name__ == '__main__':
    main()