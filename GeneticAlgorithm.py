#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
import sys

class GeneticAlgorithm:
    # Config Options
    def __init__(self,
                genotype,
                function,
                generations=30,
                population_size=50,
                mutate_chance=0.25,
                tournamentSize=4,
                elitism=True):
        self.elitism = elitism
        self.generations = generations
        self.population_size = population_size
        self.mutate_chance = mutate_chance
        self.tournamentSize = tournamentSize
        self.genotype = genotype
        self.function = function

    def InitialGeneration(self):
        initGen = []
        for i in range(self.population_size):
            initGen.append(self.genotype.generate())
        print "initGen"
        print initGen
        return initGen

    def Fitness(self, chromosome):
        return self.function(chromosome)

    def PopFitness(self, pop):
        fitnesspop = []
        popNum = 0
        for chromosome in pop:
            popNum += 1
            print "Pop: ",
            print popNum
            fitnesspop.append(self.Fitness(chromosome))
        return fitnesspop

    def Mutate(self, chromosome):
        return self.genotype.mutate(chromosome)

    def Crossover(self, chromosome1, chromosome2):
        if self.genotype.size == 1:
            return chromosome1
        index = random.randint(1, self.genotype.size -1)
        index2 = random.randint(index, self.genotype.size)
        result = []
        # result = np.array(chromosome1[:index])
        # result = np.append(result, chromosome2[index:index2])
        # result = np.append(result, chromosome1[index2:])
        result.extend(chromosome1[:index])
        result.extend(chromosome2[index:index2])
        result.extend(chromosome1[index2:])
        return result

    def TournamentSelection(self, pop, bestIndex):
        parentList = []
        parents = np.random.choice(self.population_size, self.tournamentSize)
        for i in range(self.tournamentSize):
            parentList.append(bestIndex.index(parents[i]))
        parentList = np.argsort(np.array(parentList))
        parent1 = pop[parents[parentList[0]]]
        parent2 = pop[parents[parentList[1]]]

        child = self.Crossover(parent1,parent2)
        if random.random() > self.mutate_chance:
            child = self.Mutate(child)
        return child

    def Evolve(self, pop):
        newpop = []
        bestIndex = np.argsort(self.PopFitness(pop), axis=0)[::-1]
        popbest = pop[bestIndex[0]]
        print "Pop: "
        print pop
        print "Best pop: "
        print popbest
        if self.elitism:
            newpop.append(popbest)
        while len(newpop) != len(pop):
            newpop.append(self.TournamentSelection(pop, bestIndex.tolist()))
        print len(newpop)
        print newpop
        return newpop

    def NewGeneration(self, pop):
        #fbest = np.inf
        genNum = 0
        for gen in range(self.generations):
            genNum += 1
            print "Generation: ",
            print genNum
            pop = self.Evolve(pop)
        fvalues = self.PopFitness(pop)
        idx = np.argsort(fvalues, axis=0)[::-1]
        return pop[idx[0]]

    def Run(self):
        pop = self.InitialGeneration()
        # print "Initial Generation Pop:"
        # print pop
        return self.NewGeneration(pop)
