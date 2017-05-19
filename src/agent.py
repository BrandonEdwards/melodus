from .nest import Nest

class Agent(object):
    habitatType = 0
    humanPresence = False
    predatorPresence = False
    nestInfo = None
    chickWeight = list()
    closestNest = 0

    def __init__(self, habitatType):
        self.habitatType = habitatType
        self.nestInfo = Nest(4)

    def isHumanPresence(self):
        return humanPresence

    #def attemptNest(self):
        #If probability pulled from a distribution is above a certain threshold,
        #create a new nest

    #def flush(self):
    #def forage(self, reduced):
    #def humanInAlertDistance(self)
    #def chickAtNest(self):
    #def rest(self):
    #def findNearestNest(self):
