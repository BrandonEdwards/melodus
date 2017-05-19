#!/usr/bin/python3

import numpy as np

'''
Read in maps
input = np.loadtxt(open("maps/test.csv", "rb"), delimiter = ",")

'''

'''
from src.agent import Agent

nestMakingTime::Boolean
availableNests::Int
currentTime::Int
breedingTime::Boolean
foragingTime::Boolean

Initiate enviroAgents

for i in timeFrames:
    for j in enviroAgents
        if nestMakingTime == true && availableNests > 0
            agent.attemptNest()
        elif breedTime == true
            if agent.isNest()
                agent.layEgg()
        else
            if agent.isHumanPresence()
                agent.flush(); nextAgentCell
            if foragingTime == true
                if agent.humanInAlertDistance() == true
                    agent.forage(true)
                else
                    agent.forage(false)
            else
                if agent.chickAtNest() == true
                    agent.rest()
                else
                    agent.findNearestNest()


Output results

'''
