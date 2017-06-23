import numpy as np

class Nest(object):
	def __init__(self, timeCreated):
		"""Create a new Nest obect.

		Keyword arguments:
		timeCreated 		--	Time step in simulation that nest was created

		Assign time created to its corresponding attribute. Create a list of
		egg laying times which will correspond to the current time +
		(egg number * 576 time steps). These will be the time steps that
		a given egg is laid. Hatch time is 27 days after the last egg is laid.
		"""
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
		"""Attempt to lay an egg in the nest based on time in simulation.

		Keyword arguments:
		time 		--	Current time step in the simulation.

		If the current time in the simulation is the same as the first time in
		the eggLayingTimes list, add an egg to the nest and pop the first entry
		from eggLayingTimes list.
		"""
		if len(self.eggLayingTimes) > 0:
			if time == self.eggLayingTimes[0]:
				self.totalEggs += 1
				del self.eggLayingTimes[0]
				return 1
			else:
				return 0

	def hatch(self, time):
		"""Attempt to hatch chicks in the nest based on time in simulation.

		Keyword arguments:
		time 		--	Current time step in the simulation.

		If the current time in the simulation is the same as the expected hatch
		time, hatch the eggs. Create a list of 4 weights normally distributed
		about 10 with standard deviation of 2. If it is not time to hatch, return
		None.
		"""
		if time == self.hatchTime:
			return np.random.normal(10,2,self.totalEggs)
		else:
			return None