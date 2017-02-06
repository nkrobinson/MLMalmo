import MalmoPython
import os
import sys
import time
import random

class Commands(object):

	def __init__(self, agent_host):
		self.agent_host = agent_host

	def moveForward(self):
		self.agent_host.sendCommand( "move 1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "move 0" )

	def moveBackward(self):
		self.agent_host.sendCommand( "move -1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "move 0" )

	def moveRight(self):
		self.agent_host.sendCommand( "strafe 1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "strafe 0" )

	def moveLeft(self):
		self.agent_host.sendCommand( "strafe -1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "strafe 0" )

	def turnRight(self):
		self.agent_host.sendCommand( "turn 1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "turn 0" )

	def turnLeft(self):
		self.agent_host.sendCommand( "turn -1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "turn 0" )

	def startJump(self):
		self.agent_host.sendCommand( "jump 1" )
		
	def stopJump(self):
		self.agent_host.sendCommand( "jump 0" )
