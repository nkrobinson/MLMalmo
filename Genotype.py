import random

class Genotype:
	def __init__(self, size):
		self.size = size

	def generate(self):
		chromosome = []
		for i in range(self.size):
			chromosome.append(random.uniform(-1, 1))
		return chromosome

	def setGenerateFunction(self, fun):
		self.generate = fun

	def mutate(self, chromosome):
		for num in range(random.randint(1,self.genotype.size)):
			index = random.randint(0,self.genotype.size-1)
			chromosome[index] = chromosome[index] + random.uniform(-0.5,0.5)
		return chromosome

	def setMutateFunction(self, fun):
		self.mutate = fun
