#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
import sys
import time

class GeneticAlgorithm:
    # Config Options
    def __init__(self,
                genotype,
                function,
                generations=25,
                population_size=50,
                mutate_chance=0.25,
                tournamentSize=6,
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
        return initGen

    def Fitness(self, chromosome):
        fitnessVal = self.function(chromosome)
        self.curTime = fitnessVal[1]
        return fitnessVal[0]

    def PopFitness(self, pop):
        fitnesspop = []
        popNum = 0
        self.bestTime = np.inf
        for chromosome in pop:
            popNum += 1
            print "Pop: ",
            print popNum
            fitnesspop.append(self.Fitness(chromosome))
            if self.curTime < self.bestTime:
                self.bestTime = self.curTime
        return fitnesspop

    def Mutate(self, chromosome):
        return self.genotype.mutate(chromosome)

    def Crossover(self, chromosome1, chromosome2):
        if self.genotype.size == 1:
            return chromosome1
        index = random.randint(1, self.genotype.size -1)
        index2 = random.randint(index, self.genotype.size)
        result = []
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
        popValues = self.PopFitness(pop)
        bestIndex = np.argsort(popValues, axis=0)[::-1]
        self.popBestVal = popValues[bestIndex[0]]
        self.popBest = pop[bestIndex[0]]
        if self.elitism:
            newpop.append(self.popBest)
        while len(newpop) != len(pop):
            newpop.append(self.TournamentSelection(pop, bestIndex.tolist()))
        return newpop

    def NewGeneration(self, pop):
        #fbest = np.inf
        genNum = 0
        with open("GAValues.csv", 'w') as f:
            f.write("New Run\n")
            f.write("Generation,Best Reward,Best Time\n")
        for gen in range(self.generations):
            print "Generation: ",
            print genNum
            pop = self.Evolve(pop)
            with open("GAValues.csv", 'a') as f:
                f.write(str(genNum) + "," + str(self.popBestVal) + "," + str(self.bestTime) + "\n")
            with open("NNMalmoBest.txt", 'w') as f:
                f.write(str(self.popBest))
            genNum += 1
        fvalues = self.PopFitness(pop)
        idx = np.argsort(fvalues, axis=0)[::-1]
        self.popBest = pop[idx[0]]
        self.popBestVal = fvalues[idx[0]]
        with open("GAValues.csv", 'a') as f:
            f.write(str(genNum) + "," + str(self.popBestVal) + "," + str(self.bestTime) + "\n")
        return self.popBest

    def Run(self):
        pop = self.InitialGeneration()
        return self.NewGeneration(pop)
