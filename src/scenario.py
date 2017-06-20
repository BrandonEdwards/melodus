from .agent import Agent
import numpy as np
import math

class Scenario(object):
	def __init__(self):
		self.scenarioMap = "maps/test.csv"
		self.mapWidth = 0
		self.initialAdults = math.ceil(np.random.normal(10,2,1))
		self.energyVector = [0.0,0.5,0.33,1.0,0,0]
		self.nestHabitatList = set()


	def readScenario(file):
		#readfile
		#get map
		#get map height
		#get inital adults
		#get energy vector
		#make new scenario
		#return scenario
		pass

	def getMap(self):
		return self.scenarioMap

	def setMapWidth(self):
		mapLocation = np.genfromtxt(self.scenarioMap, delimiter=",")

		for element in mapLocation[0]:
			self.mapWidth += 1

		return

	def hashNestingHabitat(self, agentDB):
		for agent in agentDB:
			#print("Testing if ", agent.getHabitatType(), " == 2", agent.getHabitatType() == 2)
			if agent.getHabitatType() == 2:
				self.nestHabitatList.add(agent.getAgentID())

	def updateNestingHabitat(self, ID):
		#See "General Map Matrix" page in your labbook for details on this weird thing
		#You probably want to make this into a more generic function for later use
		lower = -10
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