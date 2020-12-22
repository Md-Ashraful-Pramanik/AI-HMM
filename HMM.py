import numpy as np

from Constant import Constant
from Board import Board

const = Constant()


class HMM(Board):
    def __init__(self, config):
        super().__init__(config)

        self.probDistribution = np.zeros((self.dim, self.dim, self.dim, self.dim))
        self.populateProbDistribution()

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

        self.probDistribution = np.reshape(self.probDistribution, (self.dim * self.dim, self.dim * self.dim))
        self.probDistribution = self.probDistribution.transpose()
        # print(self.probDistribution2)

    def advanceTime(self):
        super().advanceTime()
        self.board = np.reshape(
            np.dot(self.probDistribution,
                   np.reshape(self.board, (self.dim * self.dim))),
            (self.dim, self.dim))
        # print(np.sum(sum(self.board)))

    def useEvidence(self, selectedPoint):
        super().useEvidence(selectedPoint)
        color = self.getColor(Board.manhattanDistancePoint(selectedPoint, self.ghostPosition))
        self.board = self.emissionDistribution[color][selectedPoint[0]][selectedPoint[1]] * self.board
        self.board /= sum(sum(self.board))
