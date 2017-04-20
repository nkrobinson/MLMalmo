
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
        loadXMLFile('./Mazes/EvalMaze'+str(i)+'NoLimit.xml')
        mr.runAgent(True)
        currentReward = mr.getReward()
        currentTime = mr.agentTime
        printString = str(i) + "," + str(currentReward) + "," + str(currentTime) + "," + str(mr.commandCount) + "\n"
        print printString
        agentTime = agentTime + currentTime
        reward = reward + currentReward
        with open("LeftAgentData.txt", 'a') as f:
            f.write(printString)

    # printString = "Total" + "," + str(reward) + "," + str(agentTime) + "\n"
    # print printString
    # with open("LeftAgentData.txt", 'a') as f:
    #     f.write(printString)
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
    time.sleep(0.1)
    if not mr.o.update():
        return -1.0
    if(leftBlock() == "stone"):
        if(frontBlock() != "stone"):
            mr.c.moveForward()
            mr.commandCount += 1
        else:
            mr.c.turnRight()
            mr.commandCount += 1
    else:
        mr.c.turnLeft()
        mr.c.moveForward()
        mr.commandCount += 2

def Evaluate():
    with open("LeftAgentData.txt", 'w') as f:
        f.write("Left Agent Data\n")
        f.write("Maze,Reward,Time,Command Count\n")
    main()
    main()
    main()

Evaluate()
