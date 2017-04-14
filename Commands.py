import MalmoPython
import time

class Commands(object):

    def __init__(self, malmo_run):
        self.mr = malmo_run
        self.agent_host = self.mr.agent_host

    def moveForward(self):
        self.agent_host.sendCommand( "move 1" )
        time.sleep(0.1)
        #time.sleep(0.5)
        #self.agent_host.sendCommand( "move 0" )
        self.mr.getWorldState()

    def moveBackward(self):
        self.agent_host.sendCommand( "move -1" )
        time.sleep(0.1)
        #time.sleep(0.5)
        #self.agent_host.sendCommand( "move 0" )
        self.mr.getWorldState()

    def moveRight(self):
        self.agent_host.sendCommand( "strafe 1" )
        time.sleep(0.5)
        self.agent_host.sendCommand( "strafe 0" )
        self.mr.getWorldState()

    def moveLeft(self):
        self.agent_host.sendCommand( "strafe -1" )
        time.sleep(0.5)
        self.agent_host.sendCommand( "strafe 0" )
        self.mr.getWorldState()

    def turnRight(self):
        self.agent_host.sendCommand( "turn 1" )
        time.sleep(0.1)
        #time.sleep(0.5)
        #self.agent_host.sendCommand( "turn 0" )
        self.mr.getWorldState()

    def turnLeft(self):
        self.agent_host.sendCommand( "turn -1" )
        time.sleep(0.1)
        #time.sleep(0.5)
        #self.agent_host.sendCommand( "turn 0" )
        self.mr.getWorldState()

    def startJump(self):
        self.agent_host.sendCommand( "jump 1" )
        self.mr.getWorldState()

    def stopJump(self):
        self.agent_host.sendCommand( "jump 0" )
        self.mr.getWorldState()
