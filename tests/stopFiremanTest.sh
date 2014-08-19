#!/bin/bash

#Using the CLI to determine if running, should use ps aswell?
state="$(python src/fireman.py start)"
if [ '$state' = 'Fireman is currently active.' ];
then 
echo "Running"
python src/fireman.py stop
echo "return for CLI was: " $PIPESTATUS
#TODO make a nice grep with more meaningful result
ps -aux | grep '??'
#TODO check for logging -wait till logging is done first
else
echo "Fireman wasn't running; A start was attempted, try again."
fi


