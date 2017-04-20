
from MalmoRun import MalmoRun
from Commands import Commands

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import MalmoPython
import os
import random
import sys
import time
import json
import errno
import numpy as np
import operator
import math

mr = MalmoRun()

def ifThenElse(in1, out1, out2):
    if(in1):
        return out1
    else:
        return out2

def oneOver(x):
    if x != 0:
        return 1/x
    return x

def loadXMLFile(mission_file = './Mazes/Maze1.xml'):
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        mr.setXML(xml)

def gpLoop():
    time.sleep(0.1)
    observations = []
    if not mr.o.update():
        return -1.0
    observations.append(float(mr.o.getDirection()))
    for i in range(len(mr.o.gridFloat)):
        observations.append(float(mr.o.gridFloat[i]))
    observations.append(float(mr.lastVal))
    # print "Observations: ",
    # print observations
    direction = math.floor(mr.gpFun(observations[0],observations[1],observations[2],
                                    observations[3],observations[4],observations[5],
                                    observations[6],observations[7],observations[8],
                                    observations[9],observations[10]))
    direction = direction % 4
    # print "Direction: ",
    # print direction
    if direction < 1:
        mr.c.moveForward()
    elif direction < 2:
        mr.c.moveBackward()
    elif direction < 3:
        mr.c.turnLeft()
    elif direction < 4:
        mr.c.turnRight()
    mr.commandCount += 1
    return direction

def setGPBestFun():
    pset = gp.PrimitiveSetTyped("MAIN", [float, float, float, float, float, float,
                                         float, float, float, float, float,], float)
    pset.addPrimitive(ifThenElse, [bool, float, float], float)

    pset.addPrimitive(operator.add, [float,float], float)
    pset.addPrimitive(operator.sub, [float,float], float)
    pset.addPrimitive(operator.mul, [float,float], float)
    pset.addPrimitive(oneOver, [float], float)
    pset.addPrimitive(operator.neg, [float], float)

    pset.addPrimitive(operator.lt, [float, float], bool)
    # pset.addPrimitive(operator.le, [float, float], bool)
    pset.addPrimitive(operator.eq, [float, float], bool)
    pset.addPrimitive(operator.gt, [float, float], bool)
    # pset.addPrimitive(operator.ge, [float, float], bool)
    pset.addPrimitive(operator.not_, [bool], bool)
    pset.addPrimitive(operator.and_, [bool, bool], bool)
    pset.addPrimitive(operator.or_, [bool, bool], bool)

    pset.addTerminal(True, bool)
    pset.addTerminal(mr.b.blockId("air"), float)
    pset.addTerminal(mr.b.blockId("stone"), float)
    # pset.addTerminal(mr.b.blockId("dirt"), float)
    # pset.addTerminal(mr.b.blockId("glowstone"), float)
    # pset.addTerminal(mr.b.blockId("emerald_block"), float)
    # pset.addTerminal(mr.b.blockId("beacon"), float)
    pset.addTerminal(mr.b.blockId("redstone_block"), float)
    # pset.addTerminal(mr.b.blockId("stained_hardened_clay"), float)
    # pset.addTerminal(mr.b.blockId("sea_lantern"), float)
    pset.addEphemeralConstant("rand100", lambda: random.random() * 1000, float)

    with open("GPMalmoBest.txt", 'r') as f:
        individual = f.read()
    print "Individual: ",
    print individual
    mr.gpFun = gp.compile(individual, pset)
    mr.setAgentFun(gpLoop)

def main():
    agentTime = 0.0
    reward = 0.0
    setGPBestFun()
    for i in range(1,6):
        loadXMLFile('./Mazes/EvalMaze'+str(i)+'.xml')
        mr.runAgent(True)
        currentReward = mr.getReward()
        currentTime = mr.agentTime
        printString = str(i) + "," + str(currentReward) + "," + str(currentTime) + "," + str(mr.commandCount) + "\n"
        print printString
        agentTime = agentTime + currentTime
        reward = reward + currentReward
        with open("BestGPAgentData.txt", 'a') as f:
            f.write(printString)
    return reward

def Evaluate():
    with open("BestGPAgentData.txt", 'w') as f:
        f.write("Random Agent Data\n")
        f.write("Maze,Reward,Time,Command Count\n")
    for i in range(3):
        main()

Evaluate()
