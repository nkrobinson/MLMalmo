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

    observations.append(MR.o.getDirection())
    for i in range(len(MR.o.gridFloat)):
        observations.append(MR.o.gridFloat[i])
    observations.append(MR.lastVal)

    # print "Observations: ",
    # print observations

    direction = NN.run(observations)[0]
    direction = (direction * 4)

    print "Direction:",
    print direction

    if direction <= 1:
        MR.c.moveForward()
    elif direction <= 2:
        MR.c.moveBackward()
    elif direction <= 3:
        MR.c.turnLeft()
    elif direction <= 4:
        MR.c.turnRight()
    return direction

def evalMalmoAgent(weights):
    agentTime = 0.0
    reward = 0.0
    NN.setWeights(weights)
    # print "Weights: ",
    # print np.array(weights)
    MR.setAgentFun(agentFun)

    # for i in range(1,16):
    for i in [1]:
        loadXMLFile('./Mazes/Maze'+str(i)+'.xml')
        MR.runAgent()
        currentReward = MR.getReward()
        currentTime = MR.agentTime
        print "Reward: ",
        print currentReward,
        print "  Time: ",
        print currentTime
        agentTime = agentTime + currentTime
        reward = reward + currentReward

    print "\tReward: ",
    print reward,
    print "  Time: ",
    print agentTime
    # return (reward,)
    return [reward,agentTime]

def loadXMLFile(mission_file = './Mazes/Maze.xml'):
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        MR.setXML(xml)

if __name__ == "__main__":
    GA = GeneticAlgorithm(Genotype(NN.weightNum), evalMalmoAgent)
    weights = GA.Run()
    f = open('NNMalmoBest.txt', 'w')
    print "Final Weights: " + str(weights)
    f.write(str(weights))
    f.close()
