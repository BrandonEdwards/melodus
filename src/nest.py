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
        

    def layEgg(self):
    	self.totalEggs += 1
