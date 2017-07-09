"""
	Package: 		melodus
	File:			fileio.py
	Author:			Brandon Edwards
	Created:		July 2017
	
	Class and associated methods for outputting results from model.
"""

import numpy as np
import pandas as pd
import os
import time

class IO(object):
	def __init__(self):
		self.chickWeightData = pd.DataFrame(np.zeros(0, dtype=[('Day', int), ('Num.Chicks', int),
								('Weight', str), ('Mean.Weight', float)]))

	def createOutputDir(self):
		self.ensureResultsDir()
		dateDir = self.ensureDateDir()

		runNum = str(len(os.listdir(dateDir)))
		outputDir = dateDir + "/run" + runNum + "/"

		os.makedirs(outputDir)

		return outputDir		
	def ensureDateDir(self):
		directory = "results/" + time.strftime("%d-%m-%Y")

		if not os.path.exists(directory):
			os.makedirs(directory)

		return directory

	def ensureResultsDir(self):
		if not os.path.exists("results/"):
			os.makedirs("results/")

	def outputResults(self):
		directory = self.createOutputDir()

		self.chickWeightData.to_csv(directory + "chickWeights.csv", index = False)

	def updateChickWeight(self, day, totalChickWeights):
		weightString = ",".join(str(i) for i in totalChickWeights)

		meanWeight = 0
		if len(totalChickWeights) > 0:
			meanWeight = sum(totalChickWeights)/len(totalChickWeights)
			# Append information to chickWeight Data frame (hopefully)
			self.chickWeightData = self.chickWeightData.append({'Day':day, 'Num.Chicks':len(totalChickWeights),
				'Weight':weightString,
				'Mean.Weight':meanWeight}, 
				ignore_index=True)
