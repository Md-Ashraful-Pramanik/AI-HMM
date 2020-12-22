import numpy as np

from HMM import HMM
from PF import PF
from Constant import Constant

const = Constant()


class Config:
    def __init__(self, dim=5, neighbourProb=.24):
        self.dim = dim
        self.maxDistance = np.sqrt(self.dim * self.dim * 2)
        self.neighbourProb = neighbourProb
        self.otherProb = (1 - self.neighbourProb * 4) / 5
        self.noOfColor = 3
        self.diagonalProb = 0

    @staticmethod
    def getBoard(choice, config):
        if str.lower(choice) == str.lower(const.HMM):
            return HMM(config)
        elif str.lower(choice) == str.lower(const.PF):
            return PF(config)
