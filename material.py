import random as rd
import numpy as np


class Material:
    def __init__(self, id, xs_s, xs_a, xs_f):
        self.id = id
        self.xs_s = xs_s
        self.xs_a = xs_a
        self.xs_f = xs_f
        self.miu = 2

    def fly(self):
        rd1 = rd.random()
        rd2 = rd.random()
        dist = -np.log(rd1) / (self.xs_s + self.xs_a)
        rd2 = rd2 * (self.xs_s + self.xs_a)
        if rd2 < self.xs_f / self.miu:
            return [1, dist]
        elif rd2 < self.xs_a:
            return [2, dist]
        else:
            return [3, dist]
