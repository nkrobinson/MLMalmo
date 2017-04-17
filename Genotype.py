import random
import numpy as np

class Genotype:
    def __init__(self, size):
        self.size = size

    def generate(self):
        chromosome = []
        for i in range(self.size):
            chromosome.append(20 * random.random() - 10)
        return chromosome

    def setGenerateFunction(self, fun):
        self.generate = fun

    def mutate(self, chromosome):
        for num in range(random.randint(1,self.size)):
            index = random.randint(0,self.size-1)
            chromosome[index] = chromosome[index] + 10 * random.random() - 5
            # chromosome[index] = 20 * random.random() - 10
        return chromosome

    def setMutateFunction(self, fun):
        self.mutate = fun
