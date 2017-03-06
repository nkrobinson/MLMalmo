
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
	wall = mr.b.getWall()
	world_state = mr.agent_host.getWorldState()
	while world_state.is_mission_running:
		observationsNum = world_state.number_of_observations_since_last_state
		if observationsNum > 0:
			print "Got " + str(observationsNum) + " observations since last state."
			print "World state observations: " + str(len(world_state.observations))
			mr.o.update()
			if(mr.o.leftBlock() == wall):
				if(mr.o.frontBlock() != wall):
					mr.c.moveForward()
				else:
					mr.c.turnRight()
			else:
				mr.c.turnRight()
				mr.c.moveForward()
		world_state = mr.agent_host.getWorldState()

mr = MalmoRun()
main()
