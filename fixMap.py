import numpy as np
import pandas as pd

matrix = (np.genfromtxt("maps/testSauble.csv", delimiter=" ")).astype(int)

rowNum = 0
for row in matrix:
	for i in range(0,len(row)):
		if row[i] == 255:
			offset = 1
			while row[i+offset] == 255:
				offset += 1
			row[i] = row[i+offset]
		elif row[i] > 2:
			row[i] = row[i] - 1

#print(matrix)
#np.savetxt("testSauble.csv", matrix, delimiter=",", format = '%d')

df = pd.DataFrame(matrix)
df.to_csv("testSauble.csv", header = None, index = False)