"""
	Package: 		melodus
	File:			scenario.py
	Author:			Brandon Edwards
	Created:		May 2017
	
	Class and associated methods for dealing with what scenario
	the model will be simulating.
"""

from .agent import Agent
import numpy as np
import src.utilities as util
import math

class Scenario(object):
	def __init__(self, scenarioMap, anthro, habitat, mapWidth, 
		initialAdults, energyVector, humanExclosureRadius):
		"""Create a new Scenario object from parameters read from file."""
		self.scenarioMap = scenarioMap
		self.anthro = anthro
		self.habitat = habitat
		self.mapWidth = mapWidth
		self.initialAdults = initialAdults
		self.energyVector = energyVector
		self.humanExclosureRadius = humanExclosureRadius
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
		agents = list()
		ID = 0

		for ID in range(0,len(self.habitat)):
			if self.habitat[ID] >= 0:
				agents.append(Agent(ID, self.habitat[ID], self.anthro))

		return agents

	def getAnthroLevel(self):
		"""Return the level of anthropogenic presence for the simulation."""
		return self.anthro

	def getEnergyVector(self):
		"""Return the habitat-indexed energy vector for the simulation."""
		return self.energyVector

	def getHabitatVector(self):
		"""Return list of habitat types for each environment cell (agent)."""
		return self.habitat

	def getHumanExclosureRadius(self):
		"""Return the radius of the desired human exclosures around a nest."""
		return self.humanExclosureRadius

	def getInitialAdults(self):
		"""Return total number of adults that start the simulation."""
		return self.initialAdults

	def getMap(self):
		"""Return the path to the map used for a particular simulation."""
		return self.scenarioMap

	def getMapWidth(self):
		"""Return width of the environment."""
		return self.mapWidth

	def hashNestingHabitat(self, agentDB):
		"""Return a list of all agents that are suitable for nesting.

		Keyword arguments:
		agentDB 		--	List of all agents in the simulation.

		Iterate through all agents in the agentDB and add the agent ID of
		those who are appropriate nesting habitat (open beach --> habitat 4).
		"""
		for agent in agentDB:
			if agent.getHabitatType() == 4:
				self.nestHabitatList.add(agent.getAgentID())

	def isNestHabitat(self, agent):
		"""Check if agent is contained in the suitable nesting habitat list, return boolean"""
		return agent.getAgentID() in self.nestHabitatList

	def setMapWidth(self):
		"""Set the map width attribute based on the width of the environment."""
		mapLocation = np.genfromtxt(self.scenarioMap, delimiter=",")

		for element in mapLocation[0]:
			self.mapWidth += 1

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
