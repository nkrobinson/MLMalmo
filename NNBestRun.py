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

mr = MalmoRun()
NN = NeuralNetwork()

def loadXMLFile(mission_file = './Mazes/Maze1.xml'):
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        mr.setXML(xml)

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
    mr.commandCount += 1
    return direction

def setNNBestFun():
    with open("NNMalmoBest.txt", 'r') as f:
        weights = f.read()
    print "Weights: ",
    print weights
    NN.setWeights(weights)
    MR.setAgentFun(agentFun)

def main():
    agentTime = 0.0
    reward = 0.0
    setNNBestFun()
    for i in range(1,6):
        loadXMLFile('./Mazes/EvalMaze'+str(i)+'.xml')
        mr.runAgent(True)
        currentReward = mr.getReward()
        currentTime = mr.agentTime
        printString = str(i) + "," + str(currentReward) + "," + str(currentTime) + "," + str(mr.commandCount) + "\n"
        print printString
        agentTime = agentTime + currentTime
        reward = reward + currentReward
        with open("BestNNAgentData.txt", 'a') as f:
            f.write(printString)
    return reward

def Evaluate():
    with open("BestNNAgentData.txt", 'w') as f:
        f.write("Random Agent Data\n")
        f.write("Maze,Reward,Time,Command Count\n")
    for i in range(3):
        main()

Evaluate()
