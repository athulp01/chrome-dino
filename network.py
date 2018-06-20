import numpy as np


class Genome():
	def __init__(self):
		self.w1 = np.random.randn(3,5)
		self.w2 = np.random.randn(5,3)
		self.fitness = 0

	def out(self, distance, ypos, speed):
		inp = np.array([distance, ypos, speed], dtype=float)
		res = np.dot(inp,self.w1)
		res = np.tanh(res)
		res = np.dot(res,self.w2)
		res = np.tanh(res)
		return res


