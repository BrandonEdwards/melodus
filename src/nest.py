class Nest(object):
    timeCreated = 0
    totalEggs = 0

    def __init__(self, timeCreated):
        self.timeCreated = timeCreated

    def layEgg(self):
    	self.totalEggs += 1
