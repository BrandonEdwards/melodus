#!/usr/bin/python3

import numpy as np
import sys
import src.utilities as util
import time as TIME
from src.agent import Agent
from src.scenario import Scenario
thread = 1#sys.argv[1]
print("Packges imported - thread ", thread)

#implement this later
#scenario = util.readScenario(str(sys.argv[1]))
scenario = Scenario(); print("Scenario created.")
scenario.setMapWidth(); print("Set map width at ", scenario.getMapWidth())

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

#Used so we don't have to iterate through entire environment every time
nextActiveAgents = list()

print("Beginning simulation.")
for time in range(0,35712):
    if time % 100 == 0:
        print("Current time is ", time)
        print(thread,"- It took ", elapsedTime, " seconds for the previous 100 time steps.")
        elapsedTime = 0.0

    start_time = TIME.time()

    print(len(nextActiveAgents))
    if len(nextActiveAgents) != 0:
       #  print("Here")
        activeAgent = list()
        activeAgents = nextActiveAgents
        nextActiveAgents = list()
    else:
        activeAgents = list()

    # Operations performed on all agents in Agent DB
    for agent in agentDB:
        # During nesting time, if the agent is proper nesting habitat, attempt a nest
        if availableNests > 0 and nestMakingTime == True:
            if scenario.isNestHabitat(agent):
                if agent.attemptNest(availableNests, time) == True:
                    availableNests -= 1
                    scenario.updateNestingHabitat(agent.getAgentID())
                    activeAgents.append(agent)

    for agent in activeAgents:
        if agent.isNest() == True and agent.isEmpty() == True:
            if breedingTime == True:
                agent.layEgg(time)
            # This will already be a part of the active agents if it hatches
            agent.checkHatchTime(time)
            nextActiveAgents.append(agent)
            continue

        if agent.isEmpty() == False:
            if agent.isHumanPresence():
                agent.flush();
                continue
            if foragingTime == True:
                agent.forage(scenario.getEnergyVector())
                nextActiveAgents.append(agent.move(agentDB, IDToAgent, scenario.getHabitatVector(), 
                    scenario.getEnergyVector(), scenario.getMapWidth()))
            else:
                if agent.chickAtNest() == True:
                    agent.rest()
                    nextActiveAgents.append(agent)
                else:
                    nextActiveAgents.append(agent.findNearestNest(agentDB, IDToAgent, scenario.getHabitatVector(), scenario.getMapWidth()))

    if nestMakingTime == True and time > 9000:
        nestMakingTime = False; print("Nest making time has ended.")
    if breedingTime == True and time > 20000:
        breedingTime = False; print("Breeding time has ended.")
    if (time - 12) % 144 == 0:
        foragingTime = not foragingTime
    elapsedTime += (TIME.time() - start_time)

#output data to files
