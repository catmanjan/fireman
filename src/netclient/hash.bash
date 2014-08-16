#!/bin/bash

# Returns a hash of a certificate file. <hash>.n should be symbolic
#   linked to the certificate file. This is how openssl quickly finds
#   trusted certificates to verify against.
openssl x509 -hash -in $1 -noout
