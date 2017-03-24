
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
import numpy

def progn(*args):
	for arg in args:
		arg()

def prog2(out1, out2):
	return partial(progn,out1,out2)

def prog3(out1, out2, out3):
	return partial(progn,out1,out2,out3)

mr = MalmoRun()

pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(prog2, 2)
pset.addPrimitive(prog3, 3)

pset.addTerminal(mr.c.moveForward)
pset.addTerminal(mr.c.moveBackward)
#pset.addTerminal(mr.c.moveRight)
#pset.addTerminal(mr.c.moveLeft)
pset.addTerminal(mr.c.turnRight)
pset.addTerminal(mr.c.turnLeft)
#pset.addTerminal(mr.c.startJump)
#pset.addTerminal(mr.c.stopJump)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=2)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalMalmoAgent(individual):
	# Transform the tree expression to functionnal Python code
	routine = gp.compile(individual, pset)
	print "Individual: ",
	print individual
	# Run the generated routine
	mr.setAgentFun(routine)
	mr.runAgent()
	reward = mr.getReward()
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
		mr.setXML(xml)

	pop = toolbox.population(n=30)
	hof = tools.HallOfFame(1)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)

	algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 20, stats, halloffame=hof)

	print "Hall Of Fame: ",
	print hof

	return pop, hof, stats

if __name__ == "__main__":
	main()
