import math
import numpy as np
import scipy.constants as c
import matplotlib.pyplot as plt

# Part 1 Helper Functions
def opencsv(name, verbose=False):
	"""
	Takes filename and returns a dictionary of each column with keys as the column headers. 
	"""

	csv_array = np.genfromtxt(name, delimiter=",", dtype="U25")
	csv_array_num = np.genfromtxt(name, delimiter=",")

	headers = csv_array[0,:]

	ret_dict = {}

	for header_ind in range(len(headers)):

		header = headers[header_ind]

		if (not header):
			continue

		if(verbose): print(header)
		data = csv_array_num[:, header_ind]
		ret_dict[header] = data[~np.isnan(data)]

	if(verbose): print(ret_dict)
	return ret_dict


def get_transconductance(current, voltage, verbose=False):
	"""
	Takes derivative of current wrt voltage (numerically using numpy gradient)

	Returns di_dv values, Peak gm, Voltage at Peak, and Vt = Voltage at Peak - 3kt/q
	"""

	di_dv = np.gradient(current, voltage)

	# Peak GM, Voltage at Peak, and Vthreshold
	peak_gm = np.max(di_dv)
	peak_vgs = voltage[np.argmax(di_dv)]
	if(peak_vgs > 0):
		v_threshold = peak_vgs - (3*c.k*300/c.e)
	else:
		v_threshold = peak_vgs + (3*c.k*300/c.e)

	if(verbose):
		print("Peak GM: {}\tVgs at Peak: {}\tV_threshold: {}".format(peak_gm, peak_vgs, v_threshold))
		plt.plot(voltage, current)
		plt.show()
		plt.plot(voltage, di_dv)
		plt.show()

	return di_dv, peak_gm, peak_vgs, v_threshold

def subthreshold_slope(current, voltage, vt):
	"""
	Calculate Subthreshold Slope. Units are in S. Swing is inverse of this slope
	"""

	# Find the indexes right before vt
	before = 0
	for i in range(len(voltage)):

		# Closest Vgs value to Vt is when Vgs[i] < Vt < Vgs[i+1]
		if(abs(voltage[i]) <= abs(vt) and abs(voltage[i+1]) >= abs(vt)):
			before = i
			break

	# Return slope. Remember to Log Current to get linear slope in exponential subthreshold region.
	slope = (math.log(abs(current[i]), 10) - math.log(abs(current[0]), 10)) / (abs(voltage[i]) - abs(voltage[0]))
	return slope


def plot_gm_ids_vgs(current, voltage, gm, vt, title):
	"""
	Make a nice plot for Q1a
	"""
	fig, ax1 = plt.subplots()

	color = 'tab:blue'
	ax1.set_xlabel('Vgs [V]')
	ax1.set_ylabel('Ids (Vds = 0.05V) [A]', color=color)
	ax1.plot(voltage, current, color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

	color = 'tab:orange'
	ax2.set_ylabel('gm [S]', color=color)  # we already handled the x-label with ax1
	ax2.plot(voltage, gm, color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	plt.axvline(x = vt, color = 'r', linestyle="dotted", label = r'$V_t$')

	ax1.set_title(title)

	plt.show()



# Part 2 Helper Function
def plot_ids_vds(voltage, current1, current2, current3, device):
	"""
	Helper Function for Part 2

	This function plots ids and vds of various Vgs and also returns channel length modulation at each Vgs
	Each input is a tuple of (label, numpy array)

	When plotted Ids and Vgs, saturation can be eye-balled from the end of Ids-Vds curve
	"""

	# Unpackage tuples
	vol_label, voltage = voltage[0], voltage[1]
	label1, current1 = current1[0], current1[1]
	label2, current2 = current2[0], current2[1]
	label3, current3 = current3[0], current3[1]

	# Get slope from that point to the end of graph
	slope1 = (current1[-2] - current1[-1]) / (voltage[-2] - voltage[-1])
	slope2 = (current2[-2] - current2[-1]) / (voltage[-2] - voltage[-1])
	slope3 = (current3[-2] - current3[-1]) / (voltage[-2] - voltage[-1])

	# Find X-Intercept
	Va1 = voltage[-1] - current1[-1]/slope1
	Va2 = voltage[-1] - current2[-1]/slope2
	Va3 = voltage[-1] - current3[-1]/slope3

	f, ax = plt.subplots()

	# Plot Ids Vds
	ax.plot(voltage, current1, color='b', label=label1)
	ax.plot(voltage, current2, color='g', label=label2)
	ax.plot(voltage, current3, color='c', label=label3)

	# Plot Line
	ax.plot([Va1, voltage[-1]], [0, current1[-1]], linestyle='dotted', color='r')
	ax.plot([Va2, voltage[-1]], [0, current2[-1]], linestyle='dotted', color='r')
	ax.plot([Va3, voltage[-1]], [0, current3[-1]], linestyle='dotted', color='r')

	# Visibility of Axis
	plt.axvline(x = 0, color = 'black')
	plt.axhline(y = 0, color = 'black') 

	ax.set_xlabel("Vds [V]")
	ax.set_ylabel("Ids [A]")
	ax.set_title("Ids of {} as function of Vds at Different Vgs".format(device))
	ax.legend()

	plt.show()

	return Va1, Va2, Va3


# Part 3 Helper Function
def plot_cvar_vg(vg, cvar, device):
	"""
	This function plots Cvar vs Vg

	Also extracts Vt using method referenced from: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6190623
	"""

	# Calculation of Cvth
	cvth = 0.3 * (np.max(cvar)-np.min(cvar)) + np.min(cvar)

	# Find Vth related to Cvth in data:
	# Find the indexes right before Cvth
	before = 0
	for i in range(len(cvar)):

		if(i == len(cvar) - 1): 
			print("Error Cvth does not intersect with graph, no Vt found")
			break

		# Closest Vgs value to Vt is when Vgs[i] < Vt < Vgs[i+1]
		if(abs(cvar[i]) <= abs(cvth) and abs(cvar[i+1]) >= abs(cvth)):
			before = i
			break

	# Interporlate Vthreshold Value
	vth = ((cvth - cvar[before]) / (cvar[before+1] - cvar[before])) * (vg[before+1] - vg[before]) + vg[before]

	f, ax = plt.subplots()
	ax.plot(vg, cvar)
	ax.set_xlabel("Vg [V]")
	ax.set_ylabel("Cvar [F]")
	ax.set_title("CV Characteristics of {}".format(device))

	# Plotting Cvth and Vt Extraction
	plt.axvline(x=vth, color='r', linestyle='--', ymin=0, ymax=(cvth-np.min(cvar))/(np.max(cvar)-np.min(cvar)) )
	plt.axhline(y=cvth, color='r', linestyle='--', xmin=0, xmax=(vth-np.min(vg))/(np.max(vg)-np.min(vg)) )

	plt.show()

	return vth


def plot_generic(x, y, xlabel, ylabel, title, device=None, legends=None, vline=None, hline=None):
	"""
	Make sure that each x y is labeled with a legends if it's provided.

	Only compatible types of x, y plotted together
	"""
	# up to 4 concurrent plots
	colors = ['r', 'b', 'g', 'c']

	f, ax = plt.subplots()
	if(legends):
		for i in range(len(legends)):

			ax.plot(x[i], y[i], label=legends[i], color=colors[i])
	else:
		ax.plot(x,y)

	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if(device):
		ax.set_title("{} of {}".format(title, device))

	if(vline):
		for x in vline:
			plt.axvline(x=x, color='r', linestyle='--')
	if(hline):
		for y in hline:
			plt.axhline(y=y, color='r', linestyle='--')

	if(legends):
		ax.legend()
	plt.show()
