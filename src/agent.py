from .nest import Nest
import numpy as np

class Agent(object):
    habitatType = 0
    humanPresence = False
    predatorPresence = False
    nestInfo = None
    chickWeight = list()
    closestNest = 0

    def __init__(self, habitatType):
        self.habitatType = habitatType

    def createAgentDB(mapName):
        map = np.genfromtxt(mapName, delimiter=",")
        agents = list()

        for i in map:
            for j in i:
                agents.append(Agent(j))

        return agents

    def attemptNest(self):
        #If probability pulled from a distribution is above a certain threshold,
        #create a new nest

        #Return 1 on success, 0 on failure
        return 1

    def isNest(self):
        if self.nestInfo == None:
            return False
        else:
            return true

    def layEgg(self):
        pass

    def isHumanPresence(self):
        return humanPresence

    def flush(self):
        pass

    def forage(self, reduced):
        pass

    def humanInAlertDistance(self):
        pass

    def chickAtNest(self):
        if nestInfo == None and len(chickWeight) > 0:
            return False
        else:
            return True

    def rest(self):
        pass

    def findNearestNest(self):
        pass
