'''
MalmoRun Class
by Nicholas Robinson

Used as a class to run the Malmo system with given parameters. To be used for machine learning.
'''

from Commands import Commands
from Observations import Observations
from Blocks import Blocks

import MalmoPython
import os
import sys
import time
import random

class MalmoRun(object):

    def __init__(self):
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

        self.agent_host = MalmoPython.AgentHost()
        self.mission_xml = None
        self.agentFun = None
        self.c = Commands(self)
        self.o = Observations(self)
        self.b = Blocks()
        self.reward = 0

    def setXML(self, xml):
        self.mission_xml = xml

    def setAgentFun(self, fun):
        self.agentFun = fun

    def checkWorldState(self):
        world_state = self.agent_host.peekWorldState()
        for reward in world_state.rewards:
            self.reward += reward.getValue()
        return world_state

    def getWorldState(self):
        #check for update
        world_state = self.agent_host.getWorldState()
        for reward in world_state.rewards:
            self.reward += reward.getValue()
        return world_state

    def wrapperFun(self):
        world_state = self.agent_host.getWorldState()
        self.reward = 0
        while world_state.is_mission_running:
            self.agentFun()
            world_state = self.agent_host.getWorldState()


    def getReward(self):
        return self.reward

    def runAgent(self):
        #Check for agent and server information
        if self.mission_xml is None:
            print "Mission XML Missing"
            return
        if self.agentFun is None:
            print "Agent Run Function Missing"
            return

        # Create default Malmo objects:
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print 'ERROR:',e
            print self.agent_host.getUsage()
            exit(1)
        if self.agent_host.receivedArgument("help"):
            print self.agent_host.getUsage()
            exit(0)

        my_mission = MalmoPython.MissionSpec(self.mission_xml, True)
        my_mission_record = MalmoPython.MissionRecordSpec("chat_reward.tgz")

        # Attempt to start a mission:
        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agent_host.startMission( my_mission, my_mission_record )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print "Error starting mission:",e
                    exit(1)
                else:
                    time.sleep(2)

        # Loop until mission starts:
        print "Waiting for the mission to start ",
        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            sys.stdout.write(".")
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print "Error:",error.text

        print
        print "Mission running ",

        self.wrapperFun()

        print
        print "Mission ended"
        # Mission has ended.
