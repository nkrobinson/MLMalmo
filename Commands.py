import MalmoPython
import time

class Commands(object):

	def __init__(self, agent_host):
		self.agent_host = agent_host

	def moveForward(self):
		print "moveForward"
		self.agent_host.sendCommand( "move 1" )
		time.sleep(0.1)
		#time.sleep(0.5)
		#self.agent_host.sendCommand( "move 0" )

	def moveBackward(self):
		print "moveBackward"
		self.agent_host.sendCommand( "move -1" )
		time.sleep(0.1)
		#time.sleep(0.5)
		#self.agent_host.sendCommand( "move 0" )

	def moveRight(self):
		self.agent_host.sendCommand( "strafe 1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "strafe 0" )

	def moveLeft(self):
		self.agent_host.sendCommand( "strafe -1" )
		time.sleep(0.5)
		self.agent_host.sendCommand( "strafe 0" )

	def moveNorth(self):
		self.agent_host.sendCommand( "movenorth 1" )
		time.sleep(0.1)

	def moveSouth(self):
		self.agent_host.sendCommand( "movesouth 1" )
		time.sleep(0.1)

	def moveEast(self):
		self.agent_host.sendCommand( "moveeast 1" )
		time.sleep(0.1)

	def moveWest(self):
		self.agent_host.sendCommand( "movewest 1" )
		time.sleep(0.1)

	def turnRight(self):
		print "turnRight"
		self.agent_host.sendCommand( "turn 1" )
		time.sleep(0.1)
		#time.sleep(0.5)
		#self.agent_host.sendCommand( "turn 0" )

	def turnLeft(self):
		print "turnLeft"
		self.agent_host.sendCommand( "turn -1" )
		time.sleep(0.1)
		#time.sleep(0.5)
		#self.agent_host.sendCommand( "turn 0" )

	def startJump(self):
		self.agent_host.sendCommand( "jump 1" )

	def stopJump(self):
		self.agent_host.sendCommand( "jump 0" )
