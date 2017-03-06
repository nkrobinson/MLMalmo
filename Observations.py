import MalmoPython
import re

class Observations(object):

	def __init__(self, agent_host):
		self.agent_host = agent_host

	def update(self, _observations=None):
		if _observations is None:
			world_state = self.agent_host.getWorldState()
			print "Obserations: World state observations: " + str(len(world_state.observations))
			self.observations = world_state.observations[0].text
		else:
			self.observations = _observations
		self.direction = re.split(',', self.observations)[14]
		self.grid = re.split(',', re.split('[\[\]]', self.observations)[1])

	def frontBlocked(self):
		self.update();
		if (self.direction <= 45 and self.direction > 315):
			return self.grid[17] != "air"
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[12] != "air"
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[10] != "air"
		else:
			return self.grid[14] != "air"

	def frontBlock(self):
		self.update();
		if (self.direction <= 45 and self.direction > 315):
			return self.grid[17]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[12]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[10]
		else:
			return self.grid[14]

	def backBlock(self):
		self.update();
		if (self.direction <= 45 and self.direction > 315):
			return self.grid[10]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[14]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[17]
		else:
			return self.grid[12]

	def leftBlock(self):
		self.update();
		if (self.direction <= 45 and self.direction > 315):
			return self.grid[14]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[17]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[12]
		else:
			return self.grid[10]

	def rightBlock(self):
		self.update();
		if (self.direction <= 45 and self.direction > 315):
			return self.grid[12]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[10]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[14]
		else:
			return self.grid[17]

	def getDirection(self):
		self.update()
		return self.direction
