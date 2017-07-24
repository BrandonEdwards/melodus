#!/usr/bin/python3

"""
    Package:        melodus
    File:           simulate.py
    Author:         Brandon Edwards
    Created:        May 2017
    
    Script to drive a given simulation.
"""
import numpy as np
import pandas as pd
import sys
import csv
import src.utilities as util
import time as TIME
from src.agent import Agent
from src.scenario import Scenario
from src.fileio import IO

thread = sys.argv[1]
scenarioFile = sys.argv[2]
print("Packges imported - thread ", thread)

io = IO()

scenario = util.readScenario(Scenario, scenarioFile); print("Scenario created.")

agentDB = util.createAgentDB(Agent, scenario); print("Agent database created.")
IDToAgent = util.mapIDToAgent(agentDB)

scenario.hashNestingHabitat(agentDB); print("Nesting habitat hash created.")

totalAdults = scenario.getInitialAdults(); print("Initial adults = ", totalAdults)

#Create empty dataframe to store chick weight data. Probably will move this to different file
chickWeightData = pd.DataFrame(np.zeros(0, dtype=[('Day', int), ('Num.Chicks', int),
    ('Weight', str), ('Mean.Weight', float)]))

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
for time in range(0,9000):#35712):
    if time % 288 == 0:
        totalChickWeights = list()
        output = list()

        day = (time / 288)
        # Delete these later
        print("Current day is ", day)
        print(thread,"- It took ", elapsedTime, " seconds for the previous day.")

        for agent in nextActiveAgents:
            print(agent.getChickWeights())
            for i in agent.getChickWeights():
                totalChickWeights.extend(i)

        print()
        elapsedTime = 0.0
        if (time > 0):
            io.updateChickWeight(day, totalChickWeights, scenario.getAnthroLevel())

    start_time = TIME.time()

    if len(nextActiveAgents) != 0:
        activeAgent = list()
        activeAgents = nextActiveAgents
        nextActiveAgents = list()
    else:
        activeAgents = list()
    
    if availableNests > 0 and nestMakingTime == True:
        # Operations performed on all agents in Agent DB
        for agent in agentDB:
            # During nesting time, if the agent is proper nesting habitat, attempt a nest
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
                nextActiveAgents.extend(agent.flush(agentDB, IDToAgent, scenario.getHabitatVector(), 
                    scenario.getMapWidth()));
                continue
            if foragingTime == True:
                alert = agent.humanInAlertDistance(agentDB, IDToAgent, scenario.getHabitatVector(),
                        scenario.getMapWidth())

                agent.forage(scenario.getEnergyVector(), alert, time)

                nextActiveAgents.extend(agent.move(agentDB, IDToAgent, scenario.getHabitatVector(), 
                    scenario.getEnergyVector(), scenario.getMapWidth()))
            else:
                if agent.chickAtNest() == True:
                    agent.rest()
                    nextActiveAgents.append(agent)
                else:
                    nextActiveAgents.extend(agent.findNearestNest(agentDB, IDToAgent, scenario.getHabitatVector(), scenario.getMapWidth()))

    if nestMakingTime == True and time > 9000:
        nestMakingTime = False; print("Nest making time has ended.")
    if breedingTime == True and time > 20000:
        breedingTime = False; print("Breeding time has ended.")
    if (time - 12) % 144 == 0:
        foragingTime = not foragingTime
    elapsedTime += (TIME.time() - start_time)

io.outputResults()
