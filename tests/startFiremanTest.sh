#!/bin/bash

python src/fireman.py start 2> /dev/null
echo "The return from cli was: " $PIPESTATUS
#TODO make a nice grep with more meaningful result
ps -aux | grep '??'
#TODO check for logging -wait till logging is done first

