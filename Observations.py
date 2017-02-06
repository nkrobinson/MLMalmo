import MalmoPython
import os
import sys
import time
import random

class Observations(object):

	def __init__(self, agent_host):
		self.agent_host = agent_host

	def update(self):
		world_state = self.agent_host.getWorldState()
		self.observations = world_state.observations
		self.ObsGrid = 0
		self.ObjDistance = 0
