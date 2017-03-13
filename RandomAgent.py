
from MalmoRun import MalmoRun
import MalmoPython
import os
import random
import sys
import time
import json
import errno
import re

def main():
	mission_file = './Maze.xml'
	with open(mission_file, 'r') as f:
		print "Loading mission from %s" % mission_file
		xml = f.read()
		mr.setXML(xml)

	mr.setAgentFun(agentFun)
	mr.runAgent()

def agentFun():
	world_state = mr.agent_host.getWorldState()
	while world_state.is_mission_running:
		command = random.randint(0,3)
		if (command == 0):
			mr.c.moveNorth()
		elif (command == 1):
			mr.c.moveSouth()
		elif (command == 2):
			mr.c.moveEast()
		elif (command == 3):
			mr.c.moveWest()
		world_state = mr.agent_host.getWorldState()

mr = MalmoRun()
main()
