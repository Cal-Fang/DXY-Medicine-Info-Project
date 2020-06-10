# -*- coding: utf-8 -*- #

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create DataFrame
data4 = open("data4.txt", "r")
list = [line.split('\t') for line in data4.readlines()]
nameinfo = pd.DataFrame([infoline[0:2] for infoline in list])
nameinfo.columns = ['name', 'tradeName']

# Reorganize
tradeNamecount = nameinfo.groupby('name').size().reset_index(name='counts')
final = tradeNamecount.groupby('counts').size().reset_index()
final.columns = ['sameNamecount', 'counts']

# Graph
ax = sns.barplot(x = 'sameNamecount', y = 'counts', data = final)
ax.set_title("How many trade names does one medicine have?")
plt.savefig('eg1.png')
plt.show()
plt.close()

# So through this graph we could find, most of the medicine will share the same trade name.
# We could try to further get some sales number and do a regress to check whether a trade
# name different from other same medicine will be correlated with higher profit or revenue.
