import numpy as np

from Constant import Constant
from random import random

const = Constant()


class Board:
    def __init__(self, config):
        self.config = config
        self.dim = config.dim
        self.ghostPosition = (0, 0)
        self.board = np.ones((self.dim, self.dim)) * (1 / (self.dim * self.dim))

        self.probDistribution = np.zeros((self.dim, self.dim, self.dim, self.dim))
        self.emissionDistribution = np.zeros((self.config.noOfColor, self.dim, self.dim, self.dim, self.dim))

        self.probDistribution2 = 0
        self.populateProbDistribution()
        self.populateEmissionDistribution()
        self.turn = const.TIME

    def populateProbDistribution(self):

        for i in range(self.dim):
            for j in range(self.dim):
                if (i + 1) < self.dim:
                    self.probDistribution[i][j][i + 1][j] = self.config.neighbourProb
                if (j + 1) < self.dim:
                    self.probDistribution[i][j][i][j + 1] = self.config.neighbourProb
                if (i - 1) >= 0:
                    self.probDistribution[i][j][i - 1][j] = self.config.neighbourProb
                if (j - 1) >= 0:
                    self.probDistribution[i][j][i][j - 1] = self.config.neighbourProb
                if (i + 1) < self.dim and (j + 1) < self.dim:
                    self.probDistribution[i][j][i + 1][j + 1] = self.config.otherProb
                if (i - 1) >= 0 and (j + 1) < self.dim:
                    self.probDistribution[i][j][i - 1][j + 1] = self.config.otherProb
                if (i + 1) < self.dim and (j - 1) >= 0:
                    self.probDistribution[i][j][i + 1][j - 1] = self.config.otherProb
                if (i - 1) >= 0 and (j - 1) >= 0:
                    self.probDistribution[i][j][i - 1][j - 1] = self.config.otherProb
                self.probDistribution[i][j][i][j] = self.config.otherProb

        # print(np.reshape(self.probDistribution, (self.dim * self.dim, self.dim * self.dim)))
        for i in range(self.dim):
            for j in range(self.dim):
                self.probDistribution[i][j] /= sum(sum(self.probDistribution[i][j]))

        self.probDistribution2 = np.reshape(self.probDistribution, (self.dim * self.dim, self.dim * self.dim))
        self.probDistribution2 = self.probDistribution2.transpose()
        print(self.probDistribution2)
        # print(self.probDistribution)
        # print(np.reshape(self.probDistribution, (self.dim * self.dim, self.dim * self.dim)))
        # p = self.probDistribution
        # for i in range(self.dim):
        #     for j in range(self.dim):
        #         for k in range(self.dim):
        #             for l in range(self.dim):
        #                 self.probDistribution[i][j][k][l] = p[k][l][i][j]
        # print(self.probDistribution)
        # print(self.probDistribution)
        #         # self.probDistribution[i][j]=p[:][:][i][j]
        # print(self.probDistribution[0][0])
        # print(self.probDistribution[:][:][0][0])
        # #print(sum(sum(self.probDistribution[0][0])))
        #
        # exit(0)

    def populateEmissionDistribution(self):

        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    for l in range(self.dim):
                        color = self.getColor(Board.manhattanDistance(i, j, k, l))

                        if color == const.RED:
                            self.emissionDistribution[const.RED][i][j][k][l] = 0.75
                            self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.15
                            self.emissionDistribution[const.GREEN][i][j][k][l] = 0.10

                        elif color == const.ORANGE:
                            self.emissionDistribution[const.RED][i][j][k][l] = 0.12
                            self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.76
                            self.emissionDistribution[const.GREEN][i][j][k][l] = 0.12

                        elif color == const.GREEN:
                            self.emissionDistribution[const.RED][i][j][k][l] = 0.10
                            self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.15
                            self.emissionDistribution[const.GREEN][i][j][k][l] = 0.75

                # if sum(sum(sum(self.emissionDistribution[:][i][j])) == [0, 0, 0]):
                #     # print("False")
                #     # print(self.emissionDistribution[:][i][j])
                #     for k in range(self.dim):
                #         for l in range(self.dim):
                #             color = self.getColor(Board.manhattanDistance(i, j, k, l))
                #
                #             if color == const.RED:
                #                 self.emissionDistribution[const.RED][i][j][k][l] = 0.75
                #                 self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.15
                #                 self.emissionDistribution[const.GREEN][i][j][k][l] = 0.10
                #
                #             elif color == const.ORANGE:
                #                 self.emissionDistribution[const.RED][i][j][k][l] = 0.12
                #                 self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.76
                #                 self.emissionDistribution[const.GREEN][i][j][k][l] = 0.12
                #
                #             elif color == const.GREEN:
                #                 self.emissionDistribution[const.RED][i][j][k][l] = 0.10
                #                 self.emissionDistribution[const.ORANGE][i][j][k][l] = 0.15
                #                 self.emissionDistribution[const.GREEN][i][j][k][l] = 0.75
                #             print(self.emissionDistribution[const.RED][i][j][k][l])
                #     if sum(sum(sum(self.emissionDistribution[:][i][j])) == [0, 0, 0]):
                #         print("False")
                #         print(self.emissionDistribution[:][i][j])
                #         exit(0)
                # self.emissionDistribution[:][i][j] /= sum(sum(self.emissionDistribution[:][i][j]))
        for i in range(self.dim):
            for j in range(self.dim):
                self.emissionDistribution[:][i][j] /= sum(sum(self.emissionDistribution[:][i][j]))

        # print(self.emissionDistribution)

    def getColor(self, distance):
        if distance <= (self.config.maxDistance / self.config.noOfColor):
            return const.RED

        elif distance <= ((self.config.maxDistance / self.config.noOfColor) * 2):
            return const.ORANGE

        else:
            return const.GREEN

    def advanceTime(self):
        # print(sum(sum(self.board)))
        # self.board = np.dot(self.probDistribution, self.board)
        # print(self.board[0][0])
        # print(self.probDistribution[0][0])
        # print(sum(sum(self.probDistribution[:][:][0][0])))

        # print(sum(sum(self.board)))
        # b2 = sum(sum(self.probDistribution * self.board))
        # print(np.reshape(self.probDistribution, (self.dim * self.dim, self.dim * self.dim)))
        # print(np.reshape(self.board, (self.dim * self.dim)))
        # b = np.zeros((self.dim, self.dim))
        # for i in range(self.dim):
        #     for j in range(self.dim):
        #         t = 0
        #         for k in range(self.dim):
        #             for l in range(self.dim):
        #                 t += self.probDistribution[i][j][k][l] * self.board[k][l]
        #         b[i][j] = t
        #
        # print(np.reshape(b, (self.dim * self.dim)))
        # print("DOT")

        # 00 12 => 12 theqe 00 => kl theqe ij te jasse
        # 3*3*3*3
        # if sum(sum(b)) != 1:
        #     print("Wrong")
        #     print(sum(sum(b)))
        #     print(self.probDistribution)
        #     print(self.board)
        #     print(b)
        # exit(0)
        # self.board = b
        # print(b == b2)
        # print(b)
        # print(b2)
        # self.board = sum(sum(self.probDistribution * self.board))
        # print(sum(sum(self.board)))

        b = self.board
        b = np.dot(self.probDistribution2, np.reshape(b, (self.dim * self.dim)))
        print(b)
        self.board = np.reshape(b, (self.dim, self.dim))
        print(np.sum(b))

        # self.board /= sum(sum(self.board))
        self.updateGhostPosition()
        self.alterTurn()

    def useEvidence(self, selectedPoint):
        color = self.getColor(Board.manhattanDistancePoint(selectedPoint, self.ghostPosition))
        self.board = self.emissionDistribution[color][selectedPoint[0]][selectedPoint[1]] * self.board
        self.board /= sum(sum(self.board))
        self.alterTurn()

    def alterTurn(self):
        # self.turn = (self.turn + 1) % 2
        self.turn = const.TIME

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
        else:
            self.ghostPosition = ((self.ghostPosition[0] + int(random() * 100)) % self.dim,
                                  (self.ghostPosition[1] + int(random() * 100) % self.dim))
        print(self.ghostPosition)

    @staticmethod
    def manhattanDistancePoint(p1, p2):
        return Board.manhattanDistance(p1[0], p1[1], p2[0], p2[1])

    @staticmethod
    def manhattanDistance(x1, y1, x2, y2):
        return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))

# print(board)
# print(probDistribution)

# board2 = np.zeros((self.dim, self.dim))
# for i in range(self.dim):
#     for j in range(self.dim):
#         board2[i][j] = sum(sum(probDistribution[i][j] * board))
# print(board2)

# board2 = sum(sum(probDistribution * board))
# board3 = self.emissionDistribution[const.ORANGE][0][0] * board2
# print(board3 / sum(sum(board3)))
#
# print()
# print(board3)

# print(board2==board3)

# print(board)
#
# selected_position = (1, 1)
#
# print(manhattan_distance_point(ghostPosition, selected_position))
# print(get_color(manhattan_distance_point(ghostPosition, selected_position)))
