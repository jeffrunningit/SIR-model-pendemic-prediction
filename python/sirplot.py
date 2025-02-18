import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

filename = 'sir.csv'
titlename = 'title.txt'
with open(titlename, 'r') as f:
	title = f.read()
graphpath = 'graphs/' + title + '.png'
data = pd.read_csv(filename, engine='python')
x = data.Time.tolist()
s = data.Susceptible.tolist()
i = data.Infected.tolist()
r = data.Removed.tolist()
fig = plt.figure(figsize=(6, 6))
labels = ["Infected", "Susceptible", "Removed"]
plt.stackplot(x,i,s,r,colors=['red','green','grey'],labels=labels)
plt.suptitle(title)
plt.legend(loc='upper center')
plt.savefig(graphpath); print('Saved figure: '+title)