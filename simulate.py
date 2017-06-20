#!/usr/bin/python3

import numpy as np
import sys
import src.utilities as u
import time as TIME
from src.agent import Agent
from src.scenario import Scenario
print("Packges imported.")

#implement this later
#scenario = Scenario.readScenario(str(sys.argv[1]))
scenario = Scenario(); print("Scenario created.")
scenario.setMapWidth();

agentDB = scenario.createAgentDB(); print("Agent database created.")

scenario.hashNestingHabitat(agentDB); print("Nesting habitat hash created.")

totalAdults = scenario.getInitialAdults(); print("Initial adults = ", totalAdults)

#Change these later
nestMakingTime = True
#assume 50/50 split of males and females
availableNests = int(totalAdults / 2)
currentTime = 1
breedingTime = True
foragingTime = True

print("Beginning simulation.")
for time in range(1,35712):
    if time % 100 == 0:
        print("Current time is ", time)

    start_time = TIME.time()
    for agent in agentDB:
        if availableNests > 0 and nestMakingTime == True:
            if scenario.isNestHabitat(agent):
                if agent.attemptNest(availableNests, time) == True:
                    availableNests -= 1
                    scenario.updateNestingHabitat(agent.getAgentID())

        if agent.isEmpty() == False:
            if breedingTime == True:
                if agent.isNest():
                    agent.layEgg(time)
                agent.checkHatchTime(time)

            if agent.isHumanPresence():
                agent.flush();
                continue
            if foragingTime == True:
                agent.forage(scenario.getEnergyVector())
                #agent.move()
            else:
                if agent.chickAtNest() == True:
                    agent.rest()
                else:
                    agent.findNearestNest()

    if nestMakingTime == True and time > 9000:
        nestMakingTime = False; print("Nest making time has ended.")
    if breedingTime == True and time > 20000:
        breedingTime = False; print("Breeding time has ended.")
   # print(TIME.time() - start_time)

#output data to files
