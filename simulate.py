#!/usr/bin/python3

import numpy as np
import sys
import src.utilities as util
import time as TIME
from src.agent import Agent
from src.scenario import Scenario
print("Packges imported.")

#implement this later
#scenario = util.readScenario(str(sys.argv[1]))
scenario = Scenario(); print("Scenario created.")
scenario.setMapWidth();

agentDB = scenario.createAgentDB(); print("Agent database created.")
IDToAgent = util.mapIDToAgent(agentDB)

scenario.hashNestingHabitat(agentDB); print("Nesting habitat hash created.")

totalAdults = scenario.getInitialAdults(); print("Initial adults = ", totalAdults)

#Change these later
elapsedTime = 0.0
nestMakingTime = True
#assume 50/50 split of males and females
availableNests = int(totalAdults / 2)
currentTime = 1
breedingTime = True
foragingTime = False

print("Beginning simulation.")
for time in range(0,35712):
    if time % 100 == 0:
        print("Current time is ", time)
        print("It took ", elapsedTime, " seconds for the previous 100 time steps.")
        elapsedTime = 0.0

    start_time = TIME.time()
    for agent in agentDB:
        if availableNests > 0 and nestMakingTime == True:
            if scenario.isNestHabitat(agent):
                if agent.attemptNest(availableNests, time) == True:
                    availableNests -= 1
                    scenario.updateNestingHabitat(agent.getAgentID())

        if agent.isNest() == True:
            if breedingTime == True:
                agent.layEgg(time)
            agent.checkHatchTime(time)

        if agent.isEmpty() == False:
            if agent.isHumanPresence():
                agent.flush();
                continue
            if foragingTime == True:
                agent.forage(scenario.getEnergyVector())
                agentDB = agent.move(agentDB, IDToAgent, scenario.getHabitatVector(), 
                    scenario.getEnergyVector(), scenario.getMapWidth())
            else:
                if agent.chickAtNest() == True:
                    agent.rest()
                else:
                    agent.findNearestNest()

    if nestMakingTime == True and time > 9000:
        nestMakingTime = False; print("Nest making time has ended.")
    if breedingTime == True and time > 20000:
        breedingTime = False; print("Breeding time has ended.")
    if (time - 12) % 144 == 0:
        foragingTime = not foragingTime
    elapsedTime += (TIME.time() - start_time)

#output data to files
