#!/usr/bin/python3

import numpy as np
import sys
from src.agent import Agent

#nestMakingTime::Boolean
#availableNests::Int
#currentTime::Int
#breedingTime::Boolean
#foragingTime::Boolean

agents = Agent.createAgentDB(str(sys.argv[1]))

nestMakingTime = True
availableNests = 5
currentTime = 0
breedingTime = True
foragingTime = True
'''
for agent in agents:
    print(agent.habitatType)
'''
for i in range(1,100):
    for agent in agents:
        if nestMakingTime == True and availableNests > 0:
            availableNests = availableNests - agent.attemptNest()
        elif breedingTime == True:
            if agent.isNest():
                agent.layEgg()
        else:
            if agent.isHumanPresence():
                agent.flush();
                continue
            if foragingTime == True:
                if agent.humanInAlertDistance() == True:
                    agent.forage(True)
                else:
                    agent.forage(False)
            else:
                if agent.chickAtNest() == True:
                    agent.rest()
                else:
                    agent.findNearestNest()

    #Update time frames
