
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
    for i in range(1,6):
        loadXMLFile('./Mazes/EvalMaze'+str(i)+'.xml')
        mr.runAgent(True)
        currentReward = mr.getReward()
        currentTime = mr.agentTime
        printString = str(i) + "," + str(currentReward) + "," + str(currentTime) + "\n"
        print printString
        agentTime = agentTime + currentTime
        reward = reward + currentReward
        with open("RandomAgentData.txt", 'a') as f:
            f.write(printString)

    printString = "Total" + "," + str(reward) + "," + str(agentTime) + "\n"
    print printString
    with open("RandomAgentData.txt", 'a') as f:
        f.write(printString)
    return reward

def frontBlock():
    if (mr.o.direction == 0.0):
        return mr.o.grid[7]
    elif (mr.o.direction == 90):
        return mr.o.grid[3]
    elif (mr.o.direction == 180.0):
        return mr.o.grid[1]
    else:
        return mr.o.grid[5]

def leftBlock():
    if (mr.o.direction == 0.0):
        return mr.o.grid[5]
    elif (mr.o.direction == 90):
        return mr.o.grid[7]
    elif (mr.o.direction == 180.0):
        return mr.o.grid[3]
    else:
        return mr.o.grid[1]

def agentFun():
    world_state = mr.agent_host.getWorldState()
    while world_state.is_mission_running:
        observations = []
        if not mr.o.update():
            return 0
        if(frontBlock() == "air"):
            mr.c.moveForward()
        else:
            if random.random() >= 0.5:
                mr.c.turnRight()
            else:
                mr.c.turnLeft()
        time.sleep(0.1)
        world_state = mr.getWorldState()

def Evaluate():
    with open("RandomAgentData.txt", 'w') as f:
        f.write("Random Agent Data\n")
        f.write("Maze,Reward,Time\n")
    main()
    main()
    main()

Evaluate()
