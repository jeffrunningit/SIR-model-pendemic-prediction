import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


print("Animation updating")
fig = plt.figure(figsize=(6, 6))


def animate(i):
	groups=data.groupby('state')
	
	plt.cla()
	if 2 in s:
		x2 = groups.get_group(2)['x']
		y2 = groups.get_group(2)['y']
		plt.scatter(x2,y2,c='grey',label='removed')
	if 1 in s:
		x1 = groups.get_group(1)['x']
		y1 = groups.get_group(1)['y']
		plt.scatter(x1,y1,c='red',label='infected')
	if 0 in s:
		x0 = groups.get_group(0)['x']
		y0 = groups.get_group(0)['y']
		plt.scatter(x0,y0,c='green',label='susceptible')
	plt.xlim(0, 30)
	plt.ylim(0, 30)
	ax = plt.gca()
	ax.axes.xaxis.set_ticks([])
	ax.axes.yaxis.set_ticks([])
		
ani = FuncAnimation(plt.gcf(), animate, interval=60)

plt.show()