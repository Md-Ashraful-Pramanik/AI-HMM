import numpy as np

from Constant import Constant
from random import random
from Board import Board

const = Constant()


class PF(Board):
    def __init__(self, config):
        super().__init__(config)

        self.particleCount = self.dim * self.dim * 5
        self.particles = []
        self.populateParticles()

    def populateParticles(self):
        for i in range(self.particleCount):
            self.particles.append((int(random() * self.dim), int(random() * self.dim)))
        self.updateBoard()

    def advanceTime(self):
        super().advanceTime()

        for i in range(self.particleCount):
            self.reSample(i)

        self.updateBoard()

    def useEvidence(self, selectedPoint):
        super().useEvidence(selectedPoint)

        color = self.getColor(Board.manhattanDistancePoint(selectedPoint, self.ghostPosition))
        weight = np.zeros(self.particleCount)
        for i in range(self.particleCount):
            weight[i] = self.emissionDistribution[color][selectedPoint[0]][selectedPoint[1]][
                         self.particles[i][0]][self.particles[i][1]] * 100
        maxWeight = np.max(weight, keepdims=False)
        # print(maxWeight)
        for i in range(self.particleCount):
            if weight[i] < (maxWeight-2):
                self.reSample(i)

        self.updateBoard()

    def reSample(self, i):
        r = random()
        if (r < self.config.neighbourProb) and self.particles[i][0] < (self.dim - 1):
            self.particles[i] = (self.particles[i][0] + 1, self.particles[i][1])
        elif (r < self.config.neighbourProb * 2) and self.particles[i][1] < (self.dim - 1):
            self.particles[i] = (self.particles[i][0], self.particles[i][1] + 1)
        elif (r < self.config.neighbourProb * 3) and self.particles[i][0] > 0:
            self.particles[i] = (self.particles[i][0] - 1, self.particles[i][1])
        elif (r < self.config.neighbourProb * 4) and self.particles[i][1] > 0:
            self.particles[i] = (self.particles[i][0], self.particles[i][1] - 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb) \
                and self.particles[i][0] > 0 and self.particles[i][1] > 0:
            self.particles[i] = (self.particles[i][0] - 1, self.particles[i][1] - 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb * 2) \
                and self.particles[i][0] < (self.dim - 1) and self.particles[i][1] > 0:
            self.particles[i] = (self.particles[i][0] + 1, self.particles[i][1] - 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb * 3) \
                and self.particles[i][0] > 0 and self.particles[i][1] < (self.dim - 1):
            self.particles[i] = (self.particles[i][0] - 1, self.particles[i][1] + 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb * 4) \
                and self.particles[i][0] < (self.dim - 1) and self.particles[i][1] < (self.dim - 1):
            self.particles[i] = (self.particles[i][0] + 1, self.particles[i][1] + 1)

    def updateBoard(self):
        self.board = np.zeros((self.dim, self.dim))

        for particle in self.particles:
            self.board[particle[0]][particle[1]] += 1

        self.board /= sum(sum(self.board))
