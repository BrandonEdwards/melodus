from .agent import Agent
import numpy as np
import math

class Scenario(object):
	def __init__(self):
		self.scenarioMap = "maps/test.csv"
		self.initialAdults = math.ceil(np.random.normal(10,2,1))
		self.energyVector = [0.0,0.5,0.33,1.0,0,0]
		self.nestHabitatHash = dict()


	def readScenario(file):
		#readfile
		#get map
		#get inital adults
		#get energy vector
		#make new scenario
		#return scenario
		pass

	def getMap(self):
		return self.scenarioMap

	def hashNestingHabitat(self, agentDB):
		i = 0
		for agent in agentDB:
			if agent.getHabitatType() == 2:
				self.nestHabitatHash[i] = agent.getAgentID()
				i += 1

	def isNestHabitat(self, agent):
		return agent in self.nestHabitatHash

	def getInitialAdults(self):
		return self.initialAdults

	def getEnergyVector(self):
		return self.energyVector