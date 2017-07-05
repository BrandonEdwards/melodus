import numpy as np
import pandas as pd

class IO(object):
	def __init__(self):
		self.chickWeightData = pd.DataFrame(np.zeros(0, dtype=[('Day', int), ('Num.Chicks', int),
    							('Weight', str), ('Mean.Weight', float)]))

	def updateChickWeight(self, day, totalChickWeights):
		weightString = ",".join(str(i) for i in totalChickWeights)

        # Append information to chickWeight Data frame (hopefully)
        chickWeightData = chickWeightData.append({'Day':day, 'Num.Chicks':len(totalChickWeights),
            'Weight':weightString,
            'Mean.Weight':(sum(totalChickWeights)/len(totalChickWeights))}, 
            ignore_index=True)