from .nest import Nest
from scipy.stats import truncnorm
import numpy as np

class Agent(object):
    def __init__(self, ID, habitatType):
        self.agentID = ID
        self.habitatType = int(habitatType)
        self.humanPresence = False
        self.predatorPresence = False
        self.nestInfo = None
        self.chickWeight = list()
        self.closestNest = 0

    def createAgentDB(mapName):
        mapLocation = np.genfromtxt(mapName, delimiter=",")
        agents = list()
        ID = 0

        for row in mapLocation:
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
            self.nestInfo = Nest(time)
            print("Nest successfully created in agent ", self.agentID, " at time ", time)
            return 1
        else:
            return 0

    def isNest(self):
        if self.nestInfo == None:
            return False
        else:
            return True

    def layEgg(self, time):
        if self.nestInfo.layEgg(time) == 1:
            print("Laid egg at nest in agent ", self.agentID)

    def checkHatchTime(self, time):
        weights = self.nestInfo.hatch(time)
        if weights != None:
            for weight in weights:
                self.chickWeight.append(weight)
                
            print("Chicks successfully hatched in agent ", self.agentID, " with weights: ", self.chickWeight)

    def isHumanPresence(self):
        return self.humanPresence

    def flush(self):
        pass

    def forage(self, energyVector):
        if len(self.chickWeight) > 0:
            if self.humanInAlertDistance() == False:
                #multiply all elements in chick energy by energy gain
                self.chickWeight[:] = [i + (0.007 * energyVector[self.habitatType]) for i in self.chickWeight]
            else:
                self.chickWeight[:] = [i + (0.0035 * energyVector[self.habitatType]) for i in self.chickWeight]

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
