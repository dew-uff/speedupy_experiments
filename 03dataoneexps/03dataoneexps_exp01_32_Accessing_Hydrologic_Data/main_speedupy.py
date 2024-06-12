from suds.client import Client
from pandas import Series
import matplotlib.pyplot as plt
from datetime import datetime

from speedupy.speedupy import initialize_speedupy, deterministic

def get_input():
	with open("input.bin", "rb") as f:
		import pickle
		dados = pickle.load(f)
		siteName = dados["siteName"]
		flow = dados["flow"]
		dates = dados["dates"]
	return siteName, flow, dates

@deterministic
def cell_1(flow, dates):
	ts = Series(flow, index=dates)
	return ts

@deterministic
def cell_2(ts):
	temp1 = ts.resample(rule='24h')
	mean_discharge = temp1.agg("mean")
	
	temp2 = ts.resample(rule='24h')
	max_discharge = temp2.agg("mean")
	
	temp3 = ts.resample(rule='24h')
	min_discharge = temp3.agg("mean")
	return mean_discharge, max_discharge, min_discharge

def cell_3(ts, mean_discharge, max_discharge, min_discharge, siteName):
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)  # arguments for add_subplot - add_subplot(nrows, ncols, plot_number)

	# Plotting series data
	ts.plot(color='powderblue', linestyle='solid', label='15-minute streamflow values')
	mean_discharge.plot(color='green', linestyle='solid', label='Average streamflow values')
	max_discharge.plot(color='red', linestyle='solid', label='Maximum streamflow values')
	min_discharge.plot(color='blue', linestyle='solid', label='Minimum streamflow values')

	# Formatting Axes
	ax.set_ylabel('Discharge, cubic feet per second')
	ax.set_xlabel('Date')
	ax.grid(True)
	ax.set_title(siteName)

	# Adding a legend
	legend = ax.legend(loc='upper left', shadow=True)
	frame = legend.get_frame()
	frame.set_facecolor('0.95')
	for label in legend.get_texts():
		label.set_fontsize('large')

	for label in legend.get_lines():
		label.set_linewidth(1.5)  # the legend line width

	# Displaying the plot
	plt.savefig("output.png")

@initialize_speedupy
def main():
	siteName, flow, dates = get_input()
	ts = cell_1(flow, dates)
	mean_discharge, max_discharge, min_discharge = cell_2(ts)
	cell_3(ts, mean_discharge, max_discharge, min_discharge, siteName)

main()