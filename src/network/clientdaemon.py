# THIS FILE IS JUST FOR THINKING
# REMOVE LATER

# ServiceDaemon.py

# hardcode ip:port for now
# 127.0.0.1:9001

# 1. HOW DO WE AUTHENTICATE

# now we've authenticated and the server has accepted our 
# connection

# if start with --client flag use SSLTranslationEngine
0. SSL connect (inside SSLTranslationEngine) happens here

# SSLTranslationEngine.py
# extension of the original RTE
# match function names = inheritance/polymorphism

1. service daemon detects service event
2. notifies core
3. core calls add_rule(rule)
###
4. SSLTranslationEngine sends model over network
5. for now don't expect response (TODO?)