#!/usr/bin/python3

import numpy as np
import sys
from src.agent import Agent
from src.scenario import Scenario
print("Packges imported.")

#implement this later
#scenario = Scenario.readScenario(str(sys.argv[1]))
scenario = Scenario(); print("Scenario created.")

mapLocation = scenario.getMap()
agentDB = Agent.createAgentDB(mapLocation); print("Agent database created.")

totalAdults = scenario.getInitialAdults();

#Change these later
nestMakingTime = True
#assume 50/50 split of males and females
availableNests = int(totalAdults / 2)
currentTime = 1
breedingTime = True
foragingTime = True

print("Beginning simulation.")
for time in range(1,35712):
    for agent in agentDB:
        if agent.isEmpty() == False:
            print("Agent not empty apparently")
            if availableNests > 0 and nestMakingTime == True:
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