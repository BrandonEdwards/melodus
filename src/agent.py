"""
	Package: 		melodus
	File:			agent.py
	Author:			Brandon Edwards
	Created:		May 2017
	
	Class and associated methods for agents used by other functions.
"""

from .nest import Nest
import numpy as np
import random
import math
import src.utilities as util

class Agent(object):
	def __init__(self, ID, habitatType, anthro):
		"""Create a new Agent object.

		Keyword arguments:
		ID 				--	index of agent in its environment
		habitatType 	--	integer value of habitat type for the agent

		Assign the ID and habitat type to the agent and assign false, empty,
		or 0 values for the rest of the agent attributes (until I implement
		something to do with them at the beginning of the simulation).
		"""	
		self.agentID = ID
		self.habitatType = int(habitatType)
		self.humanPresence = bool(np.random.binomial(1,(anthro / 100),1))#False#int(random.choice([True,False]))
		self.predatorPresence = False
		self.nestInfo = None
		self.chickWeight = list()
		self.nestLocation = list()
		self.closestNest = 0

	def attemptNest(self, availableNests, time):
		"""Attempt a nest and return boolean value on success or failure.

		Keyword arguments:
		availableNests  --  The total number of potential nests still available based
							on number of adults in the simulation.
		time            --  Current time in the simulation. Future implementations may
							reduce nesting probability based on this time.

		Pull a number from random Bernoulli trial. If success, create a nest in the agent.
		Otherwise return.
		"""
		if self.nestInfo != None:
			return 0

		numNests = np.random.binomial(availableNests, 0.00001, 1)
		if numNests > 0:
			self.nestInfo = Nest(time)
			print("Nest successfully created in agent ", self.agentID, " at time ", time)
			return True
		else:
			return False

	def checkHatchTime(self, time):
		"""Check if eggs should hatch based on time in simulation.

		Keyword arguments:
		time 			--	Current time in simulation. Used to match up with egg hatching
							times of the nest.

		Call hatch() function from Nest() class. If it returns a list of hatch weights,
		then the nest has successfully hatched. Add this list of weights to the chick
		weight of the current agent.
		"""
		weights = self.nestInfo.hatch(time)
		if len(weights) > 0:
			self.chickWeight.append(weights)
			self.nestLocation.append(self.agentID)
			print("Chicks successfully hatched in agent ", self.agentID, " with weights: ", self.chickWeight)
			return True

		return False

	def chickAtNest(self):
		"""Check if there are chicks in an agent that is not a nest. Return boolean."""
		if self.nestInfo == None and len(self.chickWeight) > 0:
			return False
		else:
			return True

	def findNearestNest(self, agentDB, IDToAgent, habitatVector, mapWidth):
		"""Find location of nearest nest and move chicks to that agent.

		Keyword arguments:
		agentDB			--	List of all agents in the simulation
		IDToAgent		--	Dictionary mapping agent IDs to their index in agentDB
		habitatVector	--	1D list of all habitat types contained in environment (row major)
		mapWidth		--	Width of the total simulation environment

		Create a map matrix 200 cells wide. After ridding of non-environment cells,
		check for any cells containing a nest. If a nest exists, move chick vector
		to that agent.

		TO DO:
		If no nest exist, find agent that would bring the chicks closest to a nest
		to try again next time step. One way to implement this would be to store
		a "nearest nest" attribute in each given agent, calculated at the beginning
		of the simulation when nesting occurs, that assists in moving chicks in the
		direction of the nearest nest.
		"""
		newAgentLocationList = list()
		weightToDelete = list()
		nestLocationToDelete = list()
		for i in range(0, len(self.chickWeight)):
			newAgentID = self.nestLocation[i]

			agentDB[IDToAgent[newAgentID]].chickWeight.append(self.chickWeight[i])
			weightToDelete.append(self.chickWeight[i])

			agentDB[IDToAgent[newAgentID]].nestLocation.append(self.nestLocation[i])
			nestLocationToDelete.append(self.nestLocation[i])

			newAgentLocationList.append(agentDB[IDToAgent[newAgentID]])	

		for i in weightToDelete:
			self.chickWeight.remove(i)

		for i in nestLocationToDelete:
			self.nestLocation.remove(i)

		return newAgentLocationList		

	def flush(self, agentDB, IDToAgent, habitatVector, mapWidth):
		"""If humans are present in cell, move chicks away from humans."""
		moveChoices = util.createMapMatrix(self.agentID, 10, mapWidth)

		#Get rid of all move choices that are out of environment (if necessary)
		moveChoices = [i for i in moveChoices if habitatVector[i] > -1]

		# Create a matrix of 1s if humans are not in agent and 0s if humans are in agent
		moveChoicesHumans = [int(not agentDB[IDToAgent[i]].humanPresence) for i in moveChoices]

		#Normalize the movement choice energy vectors
		probabilities = [float(i)/sum(moveChoicesHumans) for i in moveChoicesHumans]

		newAgentLocationList = list()
		weightToDelete = list()
		nestLocationToDelete = list()
		for i in range(0, len(self.chickWeight)):
			#Pull from multinomial distribution and get index of the success (i.e. new agent).
			moveLocationArray = np.random.multinomial(1, probabilities, size = 1)
			moveLocationIndex = -1
			for j in range(0, len(moveLocationArray[0])):
				if moveLocationArray[0][j] == 1:
					moveLocationIndex = j
					break

			if moveLocationIndex == -1:
				newAgentLocationList.append(self)
				continue

			newAgentID = moveChoices[moveLocationIndex]

			if newAgentID == self.agentID:
				#print("No movement")
				newAgentLocationList.append(self)
				continue
			
			agentDB[IDToAgent[newAgentID]].chickWeight.append(self.chickWeight[i])
			weightToDelete.append(self.chickWeight[i])

			agentDB[IDToAgent[newAgentID]].nestLocation.append(self.nestLocation[i])
			nestLocationToDelete.append(self.nestLocation[i])

			newAgentLocationList.append(agentDB[IDToAgent[newAgentID]])

		for i in weightToDelete:
			self.chickWeight.remove(i)

		for i in nestLocationToDelete:
			self.nestLocation.remove(i)

		return newAgentLocationList

	def forage(self, energyVector, alert, time):
		"""Increase weight of chicks in given agent based on habitat type.

		Keyword arguments:
		energyVector 	--	Energy multiplier indexed by habitat type

		Check if there are humans in alert distance of the agent. If so, increase
		chick weight vector by a reduced rate (half), otherwise increase chick weight
		vector by full amount. Get habitat type energy multiplier by indexing energyVector
		with habitat type.
		"""

		day = time / 288
		base = 0.014 * (-1/3*math.cos((1/9.55)*day - (7*math.pi/5)) + 2/3)
		if len(self.chickWeight) > 0:
			if alert == False:
				#multiply all elements in chick energy by energy gain
				self.chickWeight = [i + (base * energyVector[self.habitatType]) for i in self.chickWeight]
			else:
				self.chickWeight = [i + ((base / 2) * energyVector[self.habitatType]) for i in self.chickWeight]

	def getAgentID(self):
		"""Return agent ID (integer) of the given agent."""
		return self.agentID

	def getChickWeights(self):
		"""Return the list of chicks weights contained in the agent."""
		return self.chickWeight

	def getHabitatType(self):
		"""Return habitat type (integer) of the given agent."""
		return self.habitatType

	def humanInAlertDistance(self, agentDB, IDToAgent, habitatVector, mapWidth):
		"""Check if there are humans within alert distance (50m), return boolean."""
		locations = util.createMapMatrix(self.agentID, 50, mapWidth)
		locations = [i for i in locations if habitatVector[i] > -1]
		locationsHumans = [agentDB[IDToAgent[i]].humanPresence for i in locations]

		p = locationsHumans.count(True) / len(locationsHumans)
		return bool(np.random.binomial(1,p,1))

	def isEmpty(self):
		"""Return a boolean value as to whether the agent is empty."""
		if len(self.chickWeight) == 0:
			return True
		else:
			return False

	def isHumanPresence(self):
		"""Check if humans are present in the agent, return boolean."""
		return self.humanPresence

	def isNest(self):
		"""Check if agent contains a nest and return boolean value."""
		if self.nestInfo == None:
			return False
		else:
			return True

	def layEgg(self, time):
		"""Attempt to lay an egg based on time in simulation.

		Keyword arguments:
		time 			--	Current time in simulation. Used to match up with egg laying
							times of the nest.
		"""
		if self.nestInfo.layEgg(time) == 1:
			print("Laid egg at nest in agent ", self.agentID)

	def move(self, agentDB, IDToAgent, habitatVector, energyVector, mapWidth):
		"""Attempt to move chicks to different agent to forage.

		Keyword arguments:
		agentDB			--	List of all agents in the simulation
		IDToAgent		--	Dictionary mapping agent IDs to their index in agentDB
		habitatVector	--	1D list of all habitat types contained in environment (row major)
		energyVector 	--	Energy multiplier indexed by habitat type
		mapWidth		--	Width of the total simulation environment

		Create a map matrix 25 cells wide for all possible move choices. After getting
		rid of all move choices that are outside of the given environment, convert the
		agentIDs to their respective energy levels (as given by energyVector, higher energy
		level indicated better foraging zone). Normalize these values and pull from
		multinomial distribution to find index of what agent the chicks will move to.
		Copy the chick weights to the new agent and assign an empty chick weight list
		to the current agent.
		"""
		moveChoices = util.createMapMatrix(self.agentID, 25, mapWidth)

		#Get rid of all move choices that are out of environment (if necessary)
		moveChoices = [i for i in moveChoices if habitatVector[i] > -1]

		#Convert all to agent IDs to their respective habitat type
		moveChoicesHabitat = [habitatVector[i] for i in moveChoices]

		#Convert all habitat types to energyVectors
		moveChoicesEnergy = [energyVector[i] for i in moveChoicesHabitat]

		moveChoicesHumans = [int(not agentDB[IDToAgent[i]].humanPresence) for i in moveChoices]

		#Get rid of move choices that have humans
		for i in range(0, len(moveChoicesEnergy)):
			moveChoicesEnergy[i] = moveChoicesEnergy[i] * moveChoicesHumans[i]

		#Normalize the movement choice energy vectors
		probabilities = [float(i)/sum(moveChoicesEnergy) for i in moveChoicesEnergy]

		newAgentLocationList = list()
		weightToDelete = list()
		nestLocationToDelete = list()
		for i in range(0, len(self.chickWeight)):
			#Pull from multinomial distribution and get index of the success (i.e. new agent).
			moveLocationArray = np.random.multinomial(1, probabilities, size = 1)
			moveLocationIndex = -1
			for j in range(0, len(moveLocationArray[0])):
				if moveLocationArray[0][j] == 1:
					moveLocationIndex = j
					break

			if moveLocationIndex == -1:
				newAgentLocationList.append(self)
				continue

			newAgentID = moveChoices[moveLocationIndex]

			if newAgentID == self.agentID:
				#print("No movement")
				newAgentLocationList.append(self)
				continue
			
			agentDB[IDToAgent[newAgentID]].chickWeight.append(self.chickWeight[i])
			weightToDelete.append(self.chickWeight[i])

			agentDB[IDToAgent[newAgentID]].nestLocation.append(self.nestLocation[i])
			nestLocationToDelete.append(self.nestLocation[i])
			
			newAgentLocationList.append(agentDB[IDToAgent[newAgentID]])

		for i in weightToDelete:
			self.chickWeight.remove(i)

		for i in nestLocationToDelete:
			self.nestLocation.remove(i)

		return newAgentLocationList

	def rest(self):
		"""Check for humans in a reduced alert distance"""
		pass
