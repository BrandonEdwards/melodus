from .agent import Agent
import numpy as np
import math

class Scenario(object):
	def __init__(self):
		self.scenarioMap = "maps/test.csv"
		self.habitat = None
		self.mapWidth = 0
		self.initialAdults = 2#math.ceil(np.random.normal(10,2,1))
		self.energyVector = [0.0,0.5,0.33,1.0,0,0]
		self.nestHabitatList = set()

	def createAgentDB(self):
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
		return self.habitat

	def getMap(self):
		return self.scenarioMap

	def setMapWidth(self):
		mapLocation = np.genfromtxt(self.scenarioMap, delimiter=",")

		for element in mapLocation[0]:
			self.mapWidth += 1

		return

	def getMapWidth(self):
		return self.mapWidth

	def hashNestingHabitat(self, agentDB):
		for agent in agentDB:
			#print("Testing if ", agent.getHabitatType(), " == 2", agent.getHabitatType() == 2)
			if agent.getHabitatType() == 2:
				self.nestHabitatList.add(agent.getAgentID())

	def updateNestingHabitat(self, ID):
		#See "General Map Matrix" page in your labbook for details on this weird thing
		#You probably want to make this into a more generic function for later use
		lower = -100
		upper = lower * -1
		toRemove = set()
		for x in range(lower,upper):
			for b in range(lower,upper):
				toRemove.add(ID + (x * self.mapWidth) + b)

		self.nestHabitatList = self.nestHabitatList.difference(toRemove)

	def isNestHabitat(self, agent):
		#print("Agent ID = ", agent.getAgentID(), ", Habitat Type = ", agent.getHabitatType(), ", returns", agent.getAgentID() in self.nestHabitatList)
		return agent.getAgentID() in self.nestHabitatList

	def getInitialAdults(self):
		return self.initialAdults

	def getEnergyVector(self):
		return self.energyVector