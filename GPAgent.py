
from MalmoRun import MalmoRun
from Commands import Commands

from functools import partial
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

GENERATIONS = 15
POPULATION = 50
TOURNAMENT_SIZE = 6
CROSSOVER_PROBABILITY = 0.75
MUTATION_PROBABILITY = 0.25

def ifThenElse(in1, out1, out2):
    if(in1):
        return out1
    else:
        return out2

def oneOver(x):
    if x != 0:
        return 1/x
    return x

MR = MalmoRun()

# pset = gp.PrimitiveSetTyped("MAIN", [float, float, float, float, float, float,
#                                      float, float, float, float, float,], float)
pset = gp.PrimitiveSetTyped("MAIN", [float,float,float,float,float,
                                     float,float,float,float,float,
                                     float,float,float,float,float,
                                     float,float,float,float,float], float)
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
pset.addTerminal(MR.b.blockId("air"), float)
pset.addTerminal(MR.b.blockId("stone"), float)
# pset.addTerminal(MR.b.blockId("dirt"), float)
# pset.addTerminal(MR.b.blockId("glowstone"), float)
# pset.addTerminal(MR.b.blockId("emerald_block"), float)
# pset.addTerminal(MR.b.blockId("beacon"), float)
pset.addTerminal(MR.b.blockId("redstone_block"), float)
# pset.addTerminal(MR.b.blockId("stained_hardened_clay"), float)
# pset.addTerminal(MR.b.blockId("sea_lantern"), float)
pset.addEphemeralConstant("rand100", lambda: random.random() * 1000, float)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=10)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

MR.gpFun = sum
def gpLoop():
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

    direction = math.floor(MR.gpFun(observations[0],observations[1],observations[2],
                                    observations[3],observations[4],observations[5],
                                    observations[6],observations[7],observations[8],
                                    observations[9],observations[10],observations[11],
                                    observations[12],observations[13],observations[14],
                                    observations[15],observations[16],observations[17],
                                    observations[18],observations[19]))


    direction = direction % 4

    # print "Direction: ",
    # print direction

    if direction < 1:
        MR.c.moveForward()
        MR.commandCount += 1
    elif direction < 2:
        MR.c.moveBackward()
        MR.commandCount += 1
    elif direction < 3:
        MR.c.turnLeft()
        MR.commandCount += 1
    elif direction < 4:
        MR.c.turnRight()
        MR.commandCount += 1
    return observations[:10]


def evalMalmoAgent(individual):
    agentTime = 0.0
    reward = 0.0
    commands = 0
    # Transform the tree expression to functional Python code
    routine = gp.compile(individual, pset)
    MR.gpFun = routine
    MR.setAgentFun(gpLoop)
    # print "Individual: ",
    # print individual

    # Run the generated routine
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
        commands = commands + MR.commandCount
    printString = str(reward) + "," + str(agentTime) + "," + str(commands) + "\n"
    print printString
    with open("FullGPAgentData.txt", 'a') as f:
        f.write(printString)
    return (reward,)

toolbox.register("evaluate", evalMalmoAgent)
toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def loadXMLFile(mission_file = './Mazes/Maze1.xml'):
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        MR.setXML(xml)

def runEvalMazes(individual):
    print "\nEvaluation Mazes"
    print "Maze,Reward,Time,Command Count"
    agentFun = gp.compile(individual, pset)
    MR.gpFun = agentFun
    MR.setAgentFun(gpLoop)
    with open("GPAgentData.txt", 'w') as f:
        f.write("GP Agent Data\n")
        f.write("Maze,Reward,Time,Command Count\n")

    for i in range(1,6):
        loadXMLFile('./Mazes/EvalMaze'+str(i)+'.xml')
        MR.runAgent(True)
        currentReward = MR.getReward()
        currentTime = MR.agentTime
        printString = str(i) + "," + str(currentReward) + "," + str(currentTime) + "," + str(MR.commandCount) + "\n"
        print printString
        with open("GPAgentData.txt", 'a') as f:
            f.write(printString)
    return


def main():
    with open("FullGPAgentData.txt", 'w') as f:
        f.write("GP Agent Data\n")
        f.write("Reward,Time,Command Count\n")
    pop = toolbox.population(n=POPULATION)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, CROSSOVER_PROBABILITY,
                        MUTATION_PROBABILITY, GENERATIONS, stats, halloffame=hof)

    # print "Hall Of Fame: ",
    # print str(hof[0])
    with open("GPMalmoBest.txt", 'w') as f:
        f.write(str(hof[0]))

    runEvalMazes(hof[0])

    return pop, hof, stats

if __name__ == "__main__":
    main()
