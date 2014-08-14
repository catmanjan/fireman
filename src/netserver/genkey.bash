#!/bin/bash

# Make a private key
openssl genrsa -out priv.key

# Make a certificate signing request (that we will sign)
openssl req -new -key priv.key -out server.csr

# Produce a self signed certificate
openssl x509 -req -in server.csr -signkey priv.key -out cert.crt


