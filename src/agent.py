from .nest import Nest
from scipy.stats import truncnorm
import numpy as np

class Agent(object):
    agentID = 0
    habitatType = 0
    humanPresence = False
    predatorPresence = False
    nestInfo = None
    chickWeight = list()
    closestNest = 0

    def __init__(self, ID, habitatType):
        self.agentID = ID
        self.habitatType = habitatType

    def createAgentDB(mapName):
        map = np.genfromtxt(mapName, delimiter=",")
        agents = list()
        ID = 0

        for row in map:
            for habitatType in row:
                agents.append(Agent(ID, habitatType))
                ID += 1

        return agents

    def getAgentID(self):
        return self.agentID

    def getHabitatType(self):
        return self.habitatType

    def isEmpty(self):
        if self.nestInfo == None and len(self.chickWeight) == 0:
            return True
        else:
            return False

    def attemptNest(self, availableNests, time):
        if self.nestInfo != None:
            return 0

        numNests = np.random.binomial(availableNests, 0.00001, 1)
        if numNests > 0:
          #  print(numNests)
           # print(time)
            self.nestInfo = Nest(time)
            print("Nest successfully created in agent ", self.agentID, " at time ", time)
            return 1
        else:
        #If probability pulled from a distribution is above a certain threshold,
        #create a new nest

        #Return 1 on success, 0 on failure
            return 0

    def isNest(self):
        if self.nestInfo == None:
            return False
        else:
            return True

    def layEgg(self, time):
        if self.nestInfo.layEgg(time) == 1:
            print("Laid egg at nest in agent ", self.agentID)

    def isHumanPresence(self):
        return self.humanPresence

    def flush(self):
        pass

    def forage(self, reduced):
        pass

    def humanInAlertDistance(self):
        pass

    def chickAtNest(self):
        if self.nestInfo == None and len(self.chickWeight) > 0:
            return False
        else:
            return True

    def rest(self):
        pass

    def findNearestNest(self):
        pass
