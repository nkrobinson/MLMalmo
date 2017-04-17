# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class NeuralNetwork(object):
    def __init__(self):
        # self.inputLayerSize = 29
        self.inputLayerSize = 12
        self.outputLayerSize = 1
        self.hiddenLayerSize = 8
        # self.hiddenLayerSize = 20

        self.W1 = np.random.randn(self.inputLayerSize,self.hiddenLayerSize)
        self.W2 = np.random.randn(self.hiddenLayerSize,self.hiddenLayerSize)
        self.W3 = np.random.randn(self.hiddenLayerSize,self.outputLayerSize)

        self.weightNum = self.W1.size + self.W2.size + self.W2.size

    def run(self, x):
        if len(x) != self.inputLayerSize -1:
            raise ValueError('Incorrect input array size')
        x.append(1.0)
        z = np.dot(x, self.W1)
        a = self.sigmoid(z)
        z2 = np.dot(a, self.W2)
        a2 = self.sigmoid(z2)
        z3 = np.dot(a2, self.W3)
        y = self.sigmoid(z3)
        return y

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def tanH(self, z):
        return (2/(1 + np.exp(-2 * z))) - 1

    def setWeights(self, weights):
        index = 0

        d1 = len(self.W1)
        d2 = len(self.W1[0])
        arrayList = []
        for i in range(d1):
            arrayList.append(np.array(weights[index:index+d2]))
        self.W1 = np.array(arrayList[0])
        for i in range(1,len(arrayList)):
            if i == 1:
                self.W1 = np.append([self.W1], [arrayList[i]], axis = 0)
            else:
                self.W1 = np.append(self.W1, [arrayList[i]], axis = 0)

        d1 = len(self.W2)
        d2 = len(self.W2[0])
        arrayList = []
        for i in range(d1):
            arrayList.append(np.array(weights[index:index+d2]))
        self.W2 = np.array(arrayList[0])
        for i in range(1,len(arrayList)):
            if i == 1:
                self.W2 = np.append([self.W2], [arrayList[i]], axis = 0)
            else:
                self.W2 = np.append(self.W2, [arrayList[i]], axis = 0)

        d1 = len(self.W3)
        d2 = len(self.W3[0])
        arrayList = []
        for i in range(d1):
            arrayList.append(np.array(weights[index:index+d2]))
        self.W3 = np.array(arrayList[0])
        for i in range(1,len(arrayList)):
            if i == 1:
                self.W3 = np.append([self.W3], [arrayList[i]], axis = 0)
            else:
                self.W3 = np.append(self.W3, [arrayList[i]], axis = 0)
