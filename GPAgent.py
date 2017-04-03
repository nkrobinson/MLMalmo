
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

"""
def progn(*args):
    for arg in args:
        arg()

def prog2(out1, out2):
    return partial(progn,out1,out2)

def prog3(out1, out2, out3):
    return partial(progn,out1,out2,out3)
"""
def ifThenElse(in1, out1, out2):
    if(in1):
        return out1
    else:
        return out2

MR = MalmoRun()

pset = gp.PrimitiveSetTyped("MAIN", [float, float, float, float, float], float)
pset.addPrimitive(ifThenElse, [bool, float, float], float)

pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
#pset.addPrimitive(operator.div, [float,float], float)
pset.addPrimitive(operator.neg, [float], float)
pset.addPrimitive(operator.lt, [float, float], bool)
pset.addPrimitive(operator.le, [float, float], bool)
pset.addPrimitive(operator.eq, [float, float], bool)
pset.addPrimitive(operator.gt, [float, float], bool)
pset.addPrimitive(operator.ge, [float, float], bool)
pset.addPrimitive(operator.not_, [bool], bool)

pset.addTerminal(True, bool)
pset.addTerminal(MR.o.getDirection, float)
pset.addEphemeralConstant("rand100", lambda: random.random() * 100, float)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=4)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

MR.gpFun = sum
def gpLoop(direction):
    time.sleep(0.1)
    observations = []
    MR.o.update()
    observations.append(MR.o.getDirection())
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
    observations.append(float(direction))
    print "Observations: " + str(np.array(observations))

    direction = math.floor(MR.gpFun(observations[0],observations[1],observations[2],
                                    observations[3],observations[4]))

    if direction != 0:
        if direction < -0.5:
            MR.c.moveBackward()
        else:
            if direction > 0.5:
                MR.c.moveForward()
        if direction >= -0.5 and direction <= 0.5:
            if direction > 0:
                MR.c.turnLeft()
            else:
                MR.c.turnRight()

    return direction


def evalMalmoAgent(individual):
    # Transform the tree expression to functional Python code
    routine = gp.compile(individual, pset)
    MR.gpFun = routine
    print "Individual: ",
    print individual
    # Run the generated routine
    MR.setAgentFun(gpLoop)
    MR.runAgent()
    reward = MR.getReward()
    print "\tReward: ",
    print reward
    return (reward,)

toolbox.register("evaluate", evalMalmoAgent)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    mission_file = './Maze.xml'
    with open(mission_file, 'r') as f:
        print "Loading mission from %s" % mission_file
        xml = f.read()
        MR.setXML(xml)

    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 20, stats, halloffame=hof)

    print "Hall Of Fame: ",
    print hof

    return pop, hof, stats

if __name__ == "__main__":
    main()
