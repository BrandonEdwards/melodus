import math

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
	
def readScenario(file):
	"""Read scenario file and create scenario based on information in file.

	Keyword arguments:
	file 			--	Path to scenario file.

	Not yet implemented. Will serve to parse a scenario file and pull out information
	regarding the scenario, including habitat type, energetics, size of environment, etc.
	"""
	#readfile
	#get map
	#get map height
	#get inital adults
	#get energy vector
	#make new scenario
	#return scenario
	pass

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
