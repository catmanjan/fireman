#!/bin/python2.7
import logging

def generate():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Beginning httpd service generation.")
    port = ""
    ip = ""
    try:
        f = open("/etc/httpd/conf/httpd.conf","r")
        for line in f:
            # Remove newline character
            line = line[:-1]
            line = line.partition(" ")
            if line[0] == "Listen":
                line = line[2].partition(":")
                if line[2] != "":
                    port = line[2]
                    ip = line[0]
                else:
                    port = line[0]
                   
        if port == "":
            return ""
        logging.debug("httpd service generation found port: " + port)
        if ip != "":
            logging.debug("found ip: " + ip)
    except Exception as e:
        logging.debug("service generation failed: " + e.strerror)
        return ""

    # TODO
    # This is pretty crappy. We should have a way to marshal service objects.
    # Also match on ip address if it is present in httpd configuration
    return """{
    "COMMENT": "This is an automatically generated service file.",
    "systemd_service": "httpd.service",
    "port": """ + port + """,
    "transport": "tcp"
}
"""
