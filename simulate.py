#!/usr/bin/python3

import numpy as np
import sys
from src.agent import Agent

agents = Agent.createAgentDB(str(sys.argv[1]))
totalAdults = int(sys.argv[2])

#Agent natural mortality by habitat type and stage

#Change these later
nestMakingTime = True
#assume 50/50 split of males and females
availableNests = int(totalAdults / 2)
currentTime = 1
breedingTime = True
foragingTime = True

for time in range(1,35712):
    for agent in agents:
        if nestMakingTime == True and availableNests > 0:
            print("Here\n")
            availableNests = availableNests - agent.attemptNest(currentTime)
        elif breedingTime == True:
            if agent.isNest():
                agent.layEgg()
        else:
            if agent.isHumanPresence():
                agent.flush();
                continue
            if foragingTime == True:
                if agent.humanInAlertDistance() == True:
                    agent.forage(True) #Reduced foraging = True
                else:
                    agent.forage(False) #Reduced foraging = False
            else:
                if agent.chickAtNest() == True:
                    agent.rest()
                else:
                    agent.findNearestNest()

    #Update time frames
    if currentTime > 8928:
        nestMakingTime = False


#output data to files