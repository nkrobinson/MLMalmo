from MalmoRun import MalmoRun
from Commands import Commands
from Observations import Observations
from GeneticAlgorithm import GeneticAlgorithm
from Genotype import Genotype
from NeuralNetwork import NeuralNetwork

import MalmoPython
import os
import random
import sys
import time
import json
import errno
import numpy as np

MR = MalmoRun()
NN = NeuralNetwork()

def agentFun():
    time.sleep(0.1)
    observations = []
    if not MR.o.update():
        return -1.0
    try:
        if len(MR.lastVal) > 1:
            pass
        else:
            raise Exception
    except:
        MR.lastVal = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        pass

    observations.append(MR.o.getDirection())
    for i in MR.o.gridFloat:
        observations.append(i)
    for i in MR.lastVal:
        observations.append(i)

    # print "Observations: ",
    # print observations

    direction = NN.run(observations)

    # print "Direction:",
    # print direction
    if direction[0] == 1:
        MR.c.moveForward()
        MR.commandCount += 1
    if direction[1] == 1:
        MR.c.moveBackward()
        MR.commandCount += 1
    if direction[2] == 1:
        MR.c.turnLeft()
        MR.commandCount += 1
    if direction[3] == 1:
        MR.c.turnRight()
        MR.commandCount += 1
    return observations[:10]

def evalMalmoAgent(weights):
    agentTime = 0.0
    reward = 0.0
    NN.setWeights(weights)
    # print "Weights: ",
    # print np.array(weights)
    MR.setAgentFun(agentFun)

    for i in range(1,16):
        loadXMLFile('./Mazes/Maze'+str(i)+'.xml')
        MR.runAgent()
        currentReward = MR.getReward()
        currentTime = MR.agentTime
        # print i,
        # print ",",
        # print currentReward,
        # print ",",
        # print currentTime
        agentTime = agentTime + currentTime
        reward = reward + currentReward
    print "\tReward: ",
    print reward,
    print "  Time: ",
    print agentTime
    return [reward,agentTime]

def loadXMLFile(mission_file = './Mazes/Maze.xml'):
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        MR.setXML(xml)

if __name__ == "__main__":
    GA = GeneticAlgorithm(Genotype(NN.weightNum), evalMalmoAgent)
    weights = GA.Run()
    with open("NNMalmoBest.txt", 'w') as f:
        print "Final Weights: " + str(weights)
        f.write(str(weights))
