
from MalmoRun import MalmoRun
import MalmoPython
import os
import random
import sys
import time
import json
import errno

mr = MalmoRun()

def loadXMLFile(mission_file = './Mazes/Maze1.xml'):
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        mr.setXML(xml)

def main():
    agentTime = 0.0
    reward = 0.0
    mr.setAgentFun(agentFun)
    for i in range(1,16):
        loadXMLFile('./Mazes/EvalMaze'+str(i)+'.xml')
        mr.runAgent(True)
        currentReward = mr.getReward()
        currentTime = mr.agentTime
        printString = str(i) + "," + str(currentReward) + "," + str(currentTime) + "\n"
        print printString
        agentTime = agentTime + currentTime
        reward = reward + currentReward
        with open("HumanAgentData.txt", 'a') as f:
            f.write(printString)
    return reward

def agentFun():
    world_state = mr.agent_host.getWorldState()
    while world_state.is_mission_running:
        world_state = mr.agent_host.getWorldState()

def Evaluate():
    with open("HumanAgentData.txt", 'w') as f:
        f.write("Random Agent Data\n")
        f.write("Maze,Reward,Time\n")
    main()

Evaluate()
