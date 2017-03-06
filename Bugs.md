#Bugs
##Active
###
Different number of observations in LeftAgent & Observations

##Fixed
###GP is not sequential
Issue lied with agent running function. Agent was evaluated before running.

###GP does not execute every command
Issue with Continuous Movement. 1 to move, 0 to stop.

###Agent Running Loop Broken
Continuous movement issue again.
While loop was not updating as world_state was not being called.
