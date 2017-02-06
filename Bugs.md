#Bugs
##Active
###GP does not execute every command
Agent tree doesn't execute commands if they cancel each other out instead of running all commands.

###Agent Running Loop Broken
Immediately ends run. Reward is calculated before agent is run.
While loop around runAgent function breaks program.

##Fixed
###GP is not sequential
Issue lied with agent running function. Agent was evaluated before running.
