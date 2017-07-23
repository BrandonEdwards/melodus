"""
	Package: 		melodus
	File:			utilities.py
	Author:			Brandon Edwards
	Created:		June 2017
	
	Utility/helper functions for the agent database.
"""

import math
import numpy as np
#from src.scenario import Scenario

def createAgentDB(Agent, scenario):
	"""Return a list of enviro-agents based off of a scenario map environment.

	Read in habitat types from a csv file representing the environment. Each
	entry in the file is an agent. Pad the habitat to avoid out of bounds errors.
	200 dummy cells will pad the environment as 200 is the largest "map matrix"
	area created in the simulation. Create agents based off of each habitat type,
	assigning an ID (index in the habitat) and the habitat type number.

	TO DO:
	Separate the reading in of the habitat and the creation of the agentDB list
	into two separate functions. Something like initEnvironment() and createAgentDB()
	should do fine.
	"""
	agents = list()
	habitat = scenario.getHabitatVector()
	anthro = scenario.getAnthroLevel()
	ID = 0

	for ID in range(0,len(habitat)):
		if habitat[ID] >= 0:
			agents.append(Agent(ID, habitat[ID], anthro))

	return agents

def createHabitat(scenarioMap):
	habitat = (np.genfromtxt(scenarioMap, delimiter=",")).astype(int)

	#Pad habitat to avoid out of bounds errors for map matrices
	habitat = np.pad(habitat, 200, mode = 'constant', constant_values = -1)

	#Flatten habitat to iterate through
	habitat = habitat.flatten()

	return habitat

def createMapMatrix(ID, radius, mapWidth):
	"""Return a matrix of surrounding agent IDs about a given agent.

	Keyword arguments:
	ID 				-- ID of the central agent for which to create a matrix around
	radius			-- How wide the map matrix should be about the central agent
	mapWidth		-- How wide the environment is

	Create a pseudo-2D matrix of agents given a central agent, radius, and mapWidth.
	Add to list the agent whose agentID = ID + xw + b, where ID is the central agent's
	ID, x and b are the desired radius from [-radius, radius], and w is the width 
	of the map.
	"""
	mapMatrix = list()
	for x in range((radius * -1),radius):
		for b in range((radius * -1),radius):
			mapMatrix.append(ID + (x * mapWidth) + b)
	
	return mapMatrix

def mapIDToAgent(agentDB):
	"""Return dictionary of agent numbers hashed by agent ID.

	Keyword arguments:
	agentDB			--	List of all agents in a given simulation.

	An entry in the IDToAgent dictionary maps ID --> Agent Index in agentDB.
	Iterate through all agents in agent DB and assign the "agent number" (index)
	to its agent ID.
	"""
	IDToAgent = dict()

	agentNum = 0
	for agent in agentDB:
		IDToAgent[agent.getAgentID()] = agentNum
		agentNum += 1

	return IDToAgent
	
def readScenario(Scenario, file):
	"""Read scenario file and create scenario based on information in file.

	Keyword arguments:
	file 			--	Path to scenario file.

	Not yet implemented. Will serve to parse a scenario file and pull out information
	regarding the scenario, including habitat type, energetics, size of environment, etc.
	"""
	lines = list()

	with open(file) as f:
		for line in f:
			lines.append(line)

	scenarioMap = lines[0].split()[1]
	habitat = createHabitat(scenarioMap)
	mapWidth = setMapWidth(scenarioMap); print(mapWidth)
	initialAdults = math.ceil(np.random.normal(int(lines[1].split()[1]),int(lines[2].split()[1]),1))
	energyVector = eval(lines[3].split()[1])
	anthro = int(lines[4].split()[1])

	return Scenario(scenarioMap, anthro, habitat, mapWidth, initialAdults, energyVector)

def setMapWidth(scenarioMap):
	"""Set the map width attribute based on the width of the environment."""
	mapWidth = 0
	mapLocation = np.genfromtxt(scenarioMap, delimiter=",")

	for element in mapLocation[0]:
		mapWidth += 1

	return mapWidth

def timeToString(time):
	"""Return formatted time string based on time step in simulation.

	Keyword arguments:
	time 			--	Current time step in simulation.

	The simulations temporal resolution gives time steps of 5 minutes. This converts
	the current time step into total minutes to calculate the current day, hour, and minute
	of the simulation.
	"""
	mins = time * 5;
	hours = math.floor(mins / 60)
	days = math.floor(hours / 24)

	string = "Day " + (days + 1) + " at time " + (hours - (days * 24)) + ":" + (mins - (hours * 60))

	return string
