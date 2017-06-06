class Nest(object):
	def __init__(self, timeCreated):
		self.timeCreated = timeCreated
		self.eggLayingTimes = list()
		self.hatchTime = None
		self.totalEggs = 0

		for i in range(0,4):
			self.eggLayingTimes.append(timeCreated + ((i+1) * 576))

		self.hatchTime = self.eggLayingTimes[3] + (27 * 288)

	def layEgg(self, time):
		if time == self.eggLayingTimes[0]:
			self.totalEggs += 1
			del self.eggLayingTimes[0]
			print(self.eggLayingTimes)
			return 1
		else:
			return 0
