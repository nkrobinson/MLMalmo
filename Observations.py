import MalmoPython
import re

class Observations(object):

	def __init__(self, malmo_run):
		self.mr = malmo_run
		self.agent_host = self.mr.agent_host

	def update(self):
		world_state = self.mr.checkWorldState()
		if len(world_state.observations) == 0:
			return
		#print "Observations: World state observations: " + str(world_state.observations)
		#print "Length: " + str(len(world_state.observations))
		self.observations = world_state.observations[0].text
		self.direction = float(re.split(',', self.observations)[14][6:])
		self.grid = re.split(',', re.split('[\[\]]', self.observations)[1])

	def frontBlocked(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[16] != '"air"'
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[12] != '"air"'
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[10] != '"air"'
		else:
			return self.grid[14] != '"air"'

	def backBlocked(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[10] != '"air"'
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[14] != '"air"'
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[16] != '"air"'
		else:
			return self.grid[12] != '"air"'

#FRONT?
	def leftBlocked(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[14] != '"air"'
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[16] != '"air"'
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[12] != '"air"'
		else:
			return self.grid[10] != '"air"'

	def rightBlocked(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[12] != '"air"'
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[10] != '"air"'
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[14] != '"air"'
		else:
			return self.grid[16] != '"air"'

	def frontBlock(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[16]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[12]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[10]
		else:
			return self.grid[14]

	def backBlock(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[10]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[14]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[16]
		else:
			return self.grid[12]

	def leftBlock(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[14]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[16]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[12]
		else:
			return self.grid[10]

	def rightBlock(self):
		#self.update();
		if (self.direction <= 45 or self.direction > 315):
			return self.grid[12]
		elif (self.direction <= 135 and self.direction > 45):
			return self.grid[10]
		elif (self.direction <= 225 and self.direction > 135):
			return self.grid[14]
		else:
			return self.grid[16]

	def getDirection(self):
		#self.update()
		return self.direction
