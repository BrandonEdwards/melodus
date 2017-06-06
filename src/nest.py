class Nest(object):
    timeCreated = 0
    totalEggs = 0
    hatchTime = 0
    eggLayingTimes = [None] * 4

    def __init__(self, timeCreated):
        self.timeCreated = timeCreated

        for i in range(0,4):
        	self.eggLayingTimes[i] = (timeCreated + ((i+1) * 576))

        self.hatchTime = self.eggLayingTimes[3] + (27 * 288)

        print(self.eggLayingTimes)
        print(self.hatchTime)
        

    def layEgg(self, time):
    	if time == self.eggLayingTimes[0]:
    		self.totalEggs += 1
    		del self.eggLayingTimes[0]
    		print(self.eggLayingTimes)
    		return 1
    	else:
    		return 0
