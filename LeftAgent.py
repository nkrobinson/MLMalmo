
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

def frontBlock(grid, direction):
	if (direction <= 45 or direction > 315):
		return grid[17]
	elif (direction <= 135 and direction > 45):
		return grid[12]
	elif (direction <= 225 and direction > 135):
		return grid[10]
	else:
		return grid[14]

def leftBlock(grid, direction):
	if (direction <= 45 or direction > 315):
		return grid[14]
	elif (direction <= 135 and direction > 45):
		return grid[17]
	elif (direction <= 225 and direction > 135):
		return grid[12]
	else:
		return grid[10]

def agentFun():
	wall = mr.b.getWall()
	world_state = mr.agent_host.getWorldState()
	while world_state.is_mission_running:
		observationsNum = world_state.number_of_observations_since_last_state
		if observationsNum > 0:
			#print "Got " + str(observationsNum) + " observations since last state."
			#print "LeftAgent: World state observations: " + str(len(world_state.observations))

			observations = world_state.observations[0].text
			#print observations
			#direction = re.split(',', observations)[14]
			direction = re.split(':', re.split('[\[\]]', observations)[2])[1]
			direction = direction[:-1]
			grid = re.split(',', re.split('[\[\]]', observations)[1])

			print "Left block: " + leftBlock(grid, direction)
			print "Front block: " + frontBlock(grid, direction)
			#print "Wall block: " + wall
			print "Grid: " + str(grid)
			#print "Direction: " + direction
			if(leftBlock(grid, direction) == wall):
				print "Left wall detected"
				if(frontBlock(grid, direction) != wall):
					print "Front wall not detected"
					print "Moving Forward"
					mr.c.moveForward()
				else:
					print "Front wall detected"
					print "Turning Right"
					#mr.c.turnRight()
			else:
				print "Left wall not detected"
				print "Turning Left"
				print "Moving Forward"
				#mr.c.turnLeft()
				#mr.c.moveForward()
			mr.c.moveForward()
		world_state = mr.agent_host.getWorldState()
		time.sleep(1)

mr = MalmoRun()
main()
