from time import localtime
from calendar import month_name
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


print('Generating Visualization...')

current_mon = localtime().tm_mon

read_rows = current_mon - 2
data = pd.read_csv('GoodDay.csv', nrows=read_rows, na_values='x')

Z = data.iloc[:, 2:]
x = np.arange(1, 32)
y = np.arange(current_mon, 2, -1)

fig, ax = plt.subplots(figsize=(16, 4))
ax.pcolormesh(x, y, Z, edgecolors='black')
ax.set_ylabel('Year 2023')
ax.set_xlabel('Days')
ax.set_yticks(y[::-1])
ax.set_yticklabels(month_name[current_mon:2:-1])
ax.set_xticks(x)

fig.savefig('progress.png', pad_inches=0.2)
print('Visualization saved at ./progress.png')