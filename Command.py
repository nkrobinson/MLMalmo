import MalmoPython
import os
import sys
import time
import random

class Command(object):

	def __init__(self, agent_host):
		self.agent_host = agent_host

	def moveForward(self):
		self.agent_host.sendCommand( "move 1" )

	def moveBackward(self):
		self.agent_host.sendCommand( "move -1" )

	def turnLeft(self):
		self.agent_host.sendCommand( "turn 1" )

	def turnRight(self):
		self.agent_host.sendCommand( "turn -1" )
