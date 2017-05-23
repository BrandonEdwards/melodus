#!/usr/bin/python3

import numpy as np
import sys
from src.agent import Agent

agents = Agent.createAgentDB(str(sys.argv[1]))

#Agent natural mortality by habitat type and stage

#Change these later
nestMakingTime = True
availableNests = 5
currentTime = 0
breedingTime = True
foragingTime = True

for time in range(1,100):
    for agent in agents:
        if nestMakingTime == True and availableNests > 0:
            availableNests = availableNests - agent.attemptNest(time)
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
