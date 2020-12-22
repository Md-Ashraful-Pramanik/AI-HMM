import numpy as np

from Constant import Constant
from random import random

const = Constant()


class Board:
    def __init__(self, config):
        self.config = config
        self.dim = config.dim
        self.ghostPosition = (int(random()*self.dim), int(random()*self.dim))
        self.board = np.ones((self.dim, self.dim)) * (1 / (self.dim * self.dim))

        self.emissionDistribution = np.zeros((self.config.noOfColor, self.dim, self.dim, self.dim, self.dim))
        self.populateEmissionDistribution()

        self.turn = const.TIME

    def populateProbDistribution(self):
        pass

    def populateEmissionDistribution(self):

        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    for l in range(self.dim):
                        color = self.getColor(Board.manhattanDistance(i, j, k, l))

                        if color == const.RED:
                            self.emissionDistribution[const.RED][i][j][k][l] = 0.80
                            self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.15
                            self.emissionDistribution[const.GREEN][i][j][k][l] = 0.05

                        elif color == const.ORANGE:
                            self.emissionDistribution[const.RED][i][j][k][l] = 0.12
                            self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.76
                            self.emissionDistribution[const.GREEN][i][j][k][l] = 0.12

                        elif color == const.GREEN:
                            self.emissionDistribution[const.RED][i][j][k][l] = 0.05
                            self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.15
                            self.emissionDistribution[const.GREEN][i][j][k][l] = 0.80

        for i in range(self.dim):
            for j in range(self.dim):
                self.emissionDistribution[const.RED][i][j] /= sum(sum(self.emissionDistribution[const.RED][i][j]))
                self.emissionDistribution[const.ORANGE][i][j] /= sum(sum(self.emissionDistribution[const.ORANGE][i][j]))
                self.emissionDistribution[const.GREEN][i][j] /= sum(sum(self.emissionDistribution[const.GREEN][i][j]))

        # print(self.emissionDistribution)

    def advanceTime(self):
        self.alterTurn()
        self.updateGhostPosition()

    def useEvidence(self, selectedPoint):
        self.alterTurn()

    def alterTurn(self):
        self.turn = (self.turn + 1) % 2
        # self.turn = const.TIME

    def updateGhostPosition(self):
        r = random()

        if (r < self.config.neighbourProb) and self.ghostPosition[0] < (self.dim - 1):
            self.ghostPosition = (self.ghostPosition[0] + 1, self.ghostPosition[1])
        elif (r < self.config.neighbourProb * 2) and self.ghostPosition[1] < (self.dim - 1):
            self.ghostPosition = (self.ghostPosition[0], self.ghostPosition[1] + 1)
        elif (r < self.config.neighbourProb * 3) and self.ghostPosition[0] > 0:
            self.ghostPosition = (self.ghostPosition[0] - 1, self.ghostPosition[1])
        elif (r < self.config.neighbourProb * 4) and self.ghostPosition[1] > 0:
            self.ghostPosition = (self.ghostPosition[0], self.ghostPosition[1] - 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb) \
                and self.ghostPosition[0] > 0 and self.ghostPosition[1] > 0:
            self.ghostPosition = (self.ghostPosition[0] - 1, self.ghostPosition[1] - 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb * 2) \
                and self.ghostPosition[0] < (self.dim - 1) and self.ghostPosition[1] > 0:
            self.ghostPosition = (self.ghostPosition[0] + 1, self.ghostPosition[1] - 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb * 3) \
                and self.ghostPosition[0] > 0 and self.ghostPosition[1] < (self.dim - 1):
            self.ghostPosition = (self.ghostPosition[0] - 1, self.ghostPosition[1] + 1)

        elif (r < self.config.neighbourProb * 4 + self.config.otherProb * 4) \
                and self.ghostPosition[0] < (self.dim - 1) and self.ghostPosition[1] < (self.dim - 1):
            self.ghostPosition = (self.ghostPosition[0] + 1, self.ghostPosition[1] + 1)

        print(self.ghostPosition)

    def getColor(self, distance):
        if distance <= (self.config.maxDistance / (self.config.noOfColor * 2)):
            return const.RED

        elif distance <= (self.config.maxDistance / self.config.noOfColor):
            return const.ORANGE

        else:
            return const.GREEN

    @staticmethod
    def manhattanDistancePoint(p1, p2):
        return Board.manhattanDistance(p1[0], p1[1], p2[0], p2[1])

    @staticmethod
    def manhattanDistance(x1, y1, x2, y2):
        return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))
