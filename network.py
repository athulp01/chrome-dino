import numpy as np


class Genome():
    def __init__(self):
        self.w1 = np.random.randn(3,6)
        self.w2 = np.random.randn(6,3)
        self.fitness = 0

    def out(self, distance, ypos, speed):
        inp = np.array([distance, ypos, speed], dtype=float)
        res = np.dot(inp,self.w1)
        res = np.tanh(res)
        res = np.dot(res,self.w2)
        res = self.softmax(res)
        return res

    def softmax(self,x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)


