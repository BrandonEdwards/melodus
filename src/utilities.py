import math

def readScenario(file):
	#readfile
	#get map
	#get map height
	#get inital adults
	#get energy vector
	#make new scenario
	#return scenario
	pass

def timeToString(time):
	mins = time * 5;
	hours = math.floor(mins / 60)
	days = math.floor(hours / 24)

	string = "Day " + (days + 1) + " at time " + (hours - (days * 24)) + ":" + (mins - (hours * 60))

	return string

def createMapMatrix(ID, radius, mapWidth):
	mapMatrix = list()
	for x in range((radius * -1),radius):
		for b in range((radius * -1),radius):
			mapMatrix.append(ID + (x * mapWidth) + b)
	
	return mapMatrix

def mapIDToAgent(agentDB):
	IDToAgent = dict()

	agentNum = 0
	for agent in agentDB:
		IDToAgent[agent.getAgentID()] = agentNum
		agentNum += 1

	return IDToAgent