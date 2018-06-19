import numpy as np


class Genome():
	def __init__(self):
		self.w1 = np.random.randn(2,4)
		self.w2 = np.random.randn(4,1)
		self.fitness = 0

	def out(self, distance, speed):
		inp = np.array([distance, speed], dtype=float)
		res = np.dot(inp,self.w1)
		res = np.tanh(res)
		res = np.dot(res,self.w2)
		res = np.tanh(res)
		return res


