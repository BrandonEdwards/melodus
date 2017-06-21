import numpy as np

class Nest(object):
	def __init__(self, timeCreated):
		self.timeCreated = timeCreated
		self.eggLayingTimes = list()
		self.hatchTime = 0
		self.totalEggs = 0

		for i in range(0,4):
			#self.eggLayingTimes.append(timeCreated + ((i+1) * 576))
			#use the following line only for quick testing purposes
			self.eggLayingTimes.append(timeCreated + ((i+1) * 10))

		#self.hatchTime = self.eggLayingTimes[3] + (27 * 288)
		#use the following line only for quick testing purposes
		self.hatchTime = self.eggLayingTimes[3] + (1*10)

	def layEgg(self, time):
		if len(self.eggLayingTimes) > 0:
			if time == self.eggLayingTimes[0]:
				self.totalEggs += 1
				del self.eggLayingTimes[0]
				return 1
			else:
				return 0

	def hatch(self, time):
		if time == self.hatchTime:
			return np.random.normal(10,2,4)
		else:
			return None