class Agent(object):
    habitatType = 0
    humanPresence = False
    predatorPresence = False
    nestInfo = None
    chickWeight = list()
    closestNest = 0

    def __init__(self, habitatType):
        self.habitatType = habitatType

    def isHumanPresence(self):
        return humanPresence

    #def flush(self):
    #def forage(self, reduced):
    #def chickAtNest(self):
    #def rest(self):
    #def findNearestNest():
