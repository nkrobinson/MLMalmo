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
    MR.o.update()
    observations.append(MR.o.getDirection())
    """
    if MR.o.frontBlocked():
        print "FRONT"
        observations.append(1.0)
    else:
        observations.append(0.0)
    if MR.o.backBlocked():
        print "BACK"
        observations.append(1.0)
    else:
        observations.append(0.0)
    if MR.o.leftBlocked():
        print "LEFT"
        observations.append(1.0)
    else:
        observations.append(0.0)
    if MR.o.rightBlocked():
        print "RIGHT"
        observations.append(1.0)
    else:
        observations.append(0.0)
    """
    if MR.o.grid[10] != '"air"':
        observations.append(1.0)
    else:
        observations.append(0.0)
    if MR.o.grid[12] != '"air"':
        observations.append(1.0)
    else:
        observations.append(0.0)
    if MR.o.grid[14] != '"air"':
        observations.append(1.0)
    else:
        observations.append(0.0)
    if MR.o.grid[16] != '"air"':
        observations.append(1.0)
    else:
        observations.append(0.0)
    print "Observations: " + str(np.array(observations))

    direction = NN.run(np.array(observations))

    if direction[0] > -0.5 and direction[0] < 0.5:
        if direction[0] > 0:
            MR.c.moveForward()
        else:
            MR.c.moveBackward()
    if direction[1] > -0.5 and direction[1] < 0.5:
        if direction[1] > 0:
            MR.c.turnLeft()
        else:
            MR.c.turnRight()

def evalMalmoAgent(weights):
    print "Weights: " + str(weights)
    NN.setWeights(weights)
    # Run the generated routine
    MR.setAgentFun(agentFun)
    MR.runAgent()
    reward = MR.getReward()
    print "\tReward: ",
    print reward
    return (reward,)

def main():
    mission_file = './Maze.xml'
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        MR.setXML(xml)

if __name__ == "__main__":
    main()
    GA = GeneticAlgorithm(Genotype(NN.weightNum), evalMalmoAgent)
    weights = GA.Run()
    print "Final Weights: " + str(weights)
