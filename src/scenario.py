from .agent import Agent
import numpy as np
import src.utilities as util
import math

class Scenario(object):
	def __init__(self):
		self.scenarioMap = "maps/test.csv"
		self.habitat = None
		self.mapWidth = 0
		self.initialAdults = 2#math.ceil(np.random.normal(10,2,1))
		self.energyVector = [0.1,0.5,0.33,1.0,0.1,0.1]
		self.nestHabitatList = set()

	def createAgentDB(self):
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
		self.habitat = (np.genfromtxt(self.scenarioMap, delimiter=",")).astype(int)

		#Pad habitat to avoid out of bounds errors for map matrices
		self.habitat = np.pad(self.habitat, 200, mode = 'constant', constant_values = -1)

		#Flatten habitat to iterate through
		self.habitat = self.habitat.flatten()
		agents = list()
		ID = 0

		for ID in range(0,len(self.habitat)):
			if self.habitat[ID] >= 0:
				agents.append(Agent(ID, self.habitat[ID]))

		return agents

	def getHabitatVector(self):
		"""Return list of habitat types for each environment cell (agent)."""
		return self.habitat

	def getMap(self):
		"""Return the path to the map used for a particular simulation."""
		return self.scenarioMap

	def setMapWidth(self):
		"""Set the map width attribute based on the width of the environment."""
		mapLocation = np.genfromtxt(self.scenarioMap, delimiter=",")

		for element in mapLocation[0]:
			self.mapWidth += 1

	def getMapWidth(self):
		"""Return width of the environment."""
		return self.mapWidth

	def hashNestingHabitat(self, agentDB):
		"""Return a list of all agents that are suitable for nesting.

		Keyword arguments:
		agentDB 		--	List of all agents in the simulation.

		Iterate through all agents in the agentDB and add the agent ID of
		those who are appropriate nesting habitat. For now, it is habitat 2.
		"""
		for agent in agentDB:
			if agent.getHabitatType() == 2:
				self.nestHabitatList.add(agent.getAgentID())

	def updateNestingHabitat(self, ID):
		"""Remove nest location and surround agents from possible nesting habitats.

		Keyword arguments:
		ID 				--	ID of agent with newly created nest.

		Create a map matrix of width 100 around the new nest agent. Remove any agents
		in the current nesting habitat list that appear in the map matrix, representing
		a zone around the new nest that no new nests can be created.
		"""
		toRemove = set(util.createMapMatrix(ID, 100, self.mapWidth))
		self.nestHabitatList = self.nestHabitatList.difference(toRemove)

	def isNestHabitat(self, agent):
		"""Check if agent is contained in the suitable nesting habitat list, return boolean"""
		return agent.getAgentID() in self.nestHabitatList

	def getInitialAdults(self):
		"""Return total number of adults that start the simulation."""
		return self.initialAdults

	def getEnergyVector(self):
		"""Return the habitat-indexed energy vector for the simulation."""
		return self.energyVector