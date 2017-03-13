
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
import operator

def progn(*args):
	for arg in args:
		arg()

def prog2(out1, out2):
	return partial(progn,out1,out2)

def prog3(out1, out2, out3):
	return partial(progn,out1,out2,out3)

def ifThenElse(in1, out1, out2):
	if(in1):
		return partial(progn,out1)
	else:
		return partial(progn,out2)

mr = MalmoRun()

pset = gp.PrimitiveSetTyped("MAIN", [], [])
#Function Primitives
pset.addPrimitive(prog2, [int, int], int)
#pset.addPrimitive(prog3, [None, None, None], None)
pset.addPrimitive(ifThenElse, [bool, int, int], int)

#Bool Operators
pset.addPrimitive(operator.and_, [bool, bool], bool)
pset.addPrimitive(operator.or_, [bool, bool], bool)
pset.addPrimitive(operator.not_, [bool], bool)

#Float Operators
pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
pset.addPrimitive(operator.div, [float,float], float)

pset.addPrimitive(operator.lt, [float, float], bool)
pset.addPrimitive(operator.le, [float, float], bool)
pset.addPrimitive(operator.eq, [float, float], bool)
pset.addPrimitive(operator.gt, [float, float], bool)
pset.addPrimitive(operator.ge, [float, float], bool)

#Function Terminals
pset.addTerminal(mr.c.moveForward, int)
pset.addTerminal(mr.c.moveBackward, int)
#pset.addTerminal(mr.c.moveRight, None)
#pset.addTerminal(mr.c.moveLeft, None)
pset.addTerminal(mr.c.turnRight, int)
pset.addTerminal(mr.c.turnLeft, int)
#pset.addTerminal(mr.c.startJump, None)
#pset.addTerminal(mr.c.stopJump, None)

#String Terminals
pset.addTerminal(mr.o.frontBlock, str)
pset.addTerminal(mr.o.backBlock, str)
pset.addTerminal(mr.o.leftBlock, str)
pset.addTerminal(mr.o.rightBlock, str)
pset.addTerminal(mr.b.getWall, str)
pset.addTerminal(mr.b.getFloor, str)
pset.addTerminal(mr.b.getPath, str)
pset.addTerminal(mr.b.getSubGoal, str)
pset.addTerminal(mr.b.getGoal, str)
pset.addTerminal(mr.b.getStart, str)

#Float Terminals
pset.addTerminal(mr.o.getDirection, float)
pset.addEphemeralConstant("rand100", lambda: random.random() * 100, float)

#Bool Terminals
pset.addTerminal(False, bool)
pset.addTerminal(True, bool)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=4)

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

	pop = toolbox.population(n=10)
	hof = tools.HallOfFame(1)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)

	algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 30, stats, halloffame=hof)

	print "Hall Of Fame: ",
	print hof

	return pop, hof, stats

if __name__ == "__main__":
	main()
