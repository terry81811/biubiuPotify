import sys
import collections
import numpy as np
from collections import Counter

import matplotlib.pyplot as plt

userLabelsFileName = "aggr_output/users_labels.tsv"

f = open(userLabelsFileName, 'r')
userLabels = [line.rstrip('\n\r') for line in f]
userLabelsFields = userLabels[0]
userLabels = userLabels[1:]

spammerList = []

for userLabel in userLabels:
	parts = userLabel.split("\t")
	if float(parts[3]) > 0.5 and (float(parts[1]) + float(parts[2]) > 2):
		spammerList.append(float(parts[1]) + float(parts[2]))

print spammerList[0]
print len(spammerList)

print Counter(spammerList)

plt.hist(np.array(spammerList))
# fig = plt.gcf()
plt.show()