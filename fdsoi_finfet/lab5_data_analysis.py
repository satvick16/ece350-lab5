import math

import numpy as np
import scipy.constants as c

import lab5_helper as h

def part1():
	"""
	Does Part 1 Vt extraction and Graphing
	"""

	csv_files = ["nfdsoi_lp02_wp43_n40_transfer.csv", "nfinfet_3nm_nf02_n256_transfer.csv", "pfdsoi_lp02_wp43_n40_transfer.csv", "pfinfet_3nm_nf02_n256_transfer.csv"]

	for csv_file in csv_files:

		device = csv_file.split("_")[0]
		print("\n\nProcessing Data for Device {}\n".format(device))
		data = h.opencsv(csv_file)
		current_high_ds = data[list(data.keys())[2]]
		current = data[list(data.keys())[1]]
		voltage = data[list(data.keys())[0]]

		# Part 1A)
		gm, peak_gm, peak_vgs, v_t = h.get_transconductance(current=current,voltage=voltage)
		print("{} Vt: {}V\n".format(device, str(v_t.item())))
		h.plot_gm_ids_vgs(current, voltage, gm, v_t, device+ " " + r"$I_{DS}$, $g_m$ against $V_{GS}$")

		# Part 1B)
		print("\n1b) Peak Gm and Ion at High Vds")
		high_vds_gm, high_vds_peak_gm, _, v_t_high_ds = h.get_transconductance(current=current_high_ds, voltage=voltage)
		I_on = current_high_ds[np.argmax(abs(voltage))]
		print("{} Peak Gm at High Vds: {}S\n".format(device, str(high_vds_peak_gm.item())))
		print("{} Ion at High Vds: {}A\n".format(device, str(I_on.item())))

		# Part 1C)
		print("\n1c) Subthreshold Slope")
		slope = h.subthreshold_slope(current=current_high_ds, voltage=voltage, vt=v_t_high_ds)
		print("{} Subthreshold Slope: {}dec/V\n".format(device, str(slope.item())))

		# Part 1D)
		print("\n1d) DIBL")
		finfet_vds_diff = 0.7
		fdsoi_vds_diff = 0.75
		if(device == "nfdsoi" or device == "pfdsoi"):
			dibl = (v_t_high_ds - v_t) / fdsoi_vds_diff
			print("{} DIBL: {}\n".format(device, str(dibl)))
		else:
			dibl = (v_t_high_ds - v_t) / finfet_vds_diff
			print("{} DIBL: {}\n".format(device, str(dibl)))


def part2():

	csv_files = ["nfdsoi_lp02_wp43_n40_output.csv", "nfinfet_3nm_nf02_n256_output.csv", "pfdsoi_lp02_wp43_n40_output.csv", "pfinfet_3nm_nf02_n256_output.csv"]

	for csv_file in csv_files:
		device = csv_file.split("_")[0]
		print("\n\nProcessing Data for Device {}\n".format(device))
		data = h.opencsv(csv_file)
		current3 = (list(data.keys())[3], data[list(data.keys())[3]])
		current2 = (list(data.keys())[2], data[list(data.keys())[2]])
		current1 = (list(data.keys())[1], data[list(data.keys())[1]])
		voltage = (list(data.keys())[0], data[list(data.keys())[0]])
		Va1, Va2, Va3 = h.plot_ids_vds(voltage, current1, current2, current3, device)
		print("{} Early Voltage Extracted:\n{}: {}V\n{}: {}V\n{}: {}V\n".format(device, current1[0], str(abs(Va1)), current2[0], str(abs(Va2)), current3[0], str(abs(Va3))))
		print("{} Channel Length Modulation Parameters:\n{}: {}\n{}: {}\n{}: {}\n".format(device, current1[0], str(1/abs(Va1)), current2[0], str(1/abs(Va2)), current3[0], str(1/abs(Va3))))


def part3():
	"""
	C-V Characteristics Analysis
	"""

	csv_files = ["CV_characteristics/ece350_FDSOI_MOSCAP_CV_Characteristics.csv", "CV_characteristics/ece350_FinFET_MOSCAP_CV_Characteristics.csv"]

	# PROCESSING FOR FDSOI
	device = "FDSOI"
	print("\n\nProcessing Data for Device {}\n".format(device))
	data = h.opencsv(csv_files[0])

	vg = data['Vg [V]']
	cvar = data['Cvar [F]']

	# V Threshold From CV Char
	vth = h.plot_cvar_vg(vg=vg, cvar=cvar, device=device)
	print("{} V_threshold: {} V\n".format(device, str(vth.item())))

	# Max Min
	cmax, cmin = np.max(cvar), np.min(cvar)
	print("{} Cmax: {} F\tCmin: {} F\n".format(device, str(cmax.item()), str(cmin.item())))

	# Cvar is measured from 40 MOSFET in parallel, so divide value by 40
	# Also, we have Cox measured for a certain area, not Cox per area. Divide by area.
	# Then Cox/A = e_o e_ox/tox. Take Cmax as Cox
	A = 20*(10**(-9)) * 430*(10**(-9))			# Area = 20nm * 430nm
	tox = c.epsilon_0 * 4 / (cmax / (40*A))
	print("{} Oxide Thickness: {} m\n".format(device, str(tox.item())))


	# REPEAT FOR FINFET
	device = "FinFET"
	print("\n\nProcessing Data for Device {}\n".format(device))
	data = h.opencsv(csv_files[1])

	vg = data['Vg [V]']
	cvar = data['Cvar [F]']

	vth = h.plot_cvar_vg(vg=vg, cvar=cvar, device=device)
	print("{} V_threshold: {} V\n".format(device, str(vth.item())))

	# Max Min
	cmax, cmin = np.max(cvar), np.min(cvar)
	print("{} Cmax: {} F\tCmin: {} F\n".format(device, str(cmax.item()), str(cmin.item())))

	# Cvar is measured from 512 Fins in parallel, so divide value by 512
	# Also, we have Cox measured for a certain area, not Cox per area. Divide by area.
	# Then Cox = e_o e_ox/tox. Take Cmax as Cox
	A = 11*(10**(-9)) * 95*(10**(-9))			# Area = 11nm * 95nm
	tox = c.epsilon_0 * 4 / (cmax / (512*A))	# Perhaps we are not using effective width, but result should be the same
	print("{} Oxide Thickness: {} m\n".format(device, str(tox.item())))


def postlabq3():

	csv_files = ["nfdsoi_lp02_wp43_n40_transfer.csv", "nfinfet_3nm_nf02_n256_transfer.csv", "nfdsoi_lp02_wp43_n40_output.csv", "nfinfet_3nm_nf02_n256_output.csv"]

	# For FDSOI
	device = "FDSOI"

	fdsoi_ids_vgs = h.opencsv(csv_files[0])
	fdsoi_ids_vds = h.opencsv(csv_files[2])

	# I_ds vs Vgs at Vds = 0.8V
	ids_high_vds = fdsoi_ids_vgs[list(fdsoi_ids_vgs.keys())[2]]
	vgs = 		   fdsoi_ids_vgs[list(fdsoi_ids_vgs.keys())[0]]

	# I_ds vs Vds at Vgs = 0.4V
	ids_vgs_04 = fdsoi_ids_vds[list(fdsoi_ids_vds.keys())[1]]
	vds = 		 fdsoi_ids_vds[list(fdsoi_ids_vds.keys())[0]]

	gm, _, _, _ = h.get_transconductance(current=ids_high_vds, voltage=vgs)
	gds, _, _, _ = h.get_transconductance(current=ids_vgs_04, voltage=vds)

	intrinsic_gain = gm[np.where(vgs == 0.4)] / gds[np.where(vds == 0.8)]

	print("{} Intrinsic Gain: {}\n".format(device, str(intrinsic_gain.item())))



	# For FinFETs
	device = "FinFET"

	finfet_ids_vgs = h.opencsv(csv_files[1])
	finfet_ids_vds = h.opencsv(csv_files[3])

	# I_ds vs Vgs at Vds = 0.75V
	ids_high_vds = finfet_ids_vgs[list(finfet_ids_vgs.keys())[2]]
	vgs = 		   finfet_ids_vgs[list(finfet_ids_vgs.keys())[0]]

	# I_ds vs Vds at Vgs = 0.375V
	ids_vgs_04 = finfet_ids_vds[list(finfet_ids_vds.keys())[1]]
	vds = 		 finfet_ids_vds[list(finfet_ids_vds.keys())[0]]

	gm, _, _, _ = h.get_transconductance(current=ids_high_vds, voltage=vgs)
	gds, _, _, _ = h.get_transconductance(current=ids_vgs_04, voltage=vds)

	intrinsic_gain = gm[np.where(vgs == 0.375)] / gds[np.where(vds == 0.75)]

	print("{} Intrinsic Gain: {}\n".format(device, str(intrinsic_gain.item())))


def postlabq4():

	csv_files = ["nfdsoi_lp02_wp43_n40_transfer.csv", "nfinfet_3nm_nf02_n256_transfer.csv", "nfdsoi_lp02_wp43_n40_output.csv", "nfinfet_3nm_nf02_n256_output.csv"]

	# For FDSOI
	device = "FDSOI"

	fdsoi_ids_vgs = h.opencsv(csv_files[0])
	fdsoi_ids_vds = h.opencsv(csv_files[2])

	# I_ds vs Vgs at Vds = 0.8V
	ids_high_vds = fdsoi_ids_vgs[list(fdsoi_ids_vgs.keys())[2]]
	vgs = 		   fdsoi_ids_vgs[list(fdsoi_ids_vgs.keys())[0]]

	# FDSOI W = 80 * 0.43 um
	W = 80 * 0.43 * (10**(-6))

	# Get gm when vds is high so that we can get a part of gm in saturation
	gm, _, _, _ = h.get_transconductance(current=ids_high_vds, voltage=vgs)

	gm_div_w = gm/W 
	ids_high_vds_div_w = ids_high_vds/W

	# Plot Ids/W on X, gm/W on Y
	h.plot_generic(x=ids_high_vds_div_w, y=gm_div_w, xlabel="Ids/W [A/m]", ylabel="gm/W [S/m]", title="gm/W vs Ids/W", device=device)


	# For FinFET
	device = "FinFET"

	finfet_ids_vgs = h.opencsv(csv_files[1])
	finfet_ids_vds = h.opencsv(csv_files[3])

	# I_ds vs Vgs at Vds = 0.75V
	ids_high_vds = finfet_ids_vgs[list(finfet_ids_vgs.keys())[2]]
	vgs = 		   finfet_ids_vgs[list(finfet_ids_vgs.keys())[0]]

	# FDSOI W = 256 * 2 * 95 nm
	W = 256 * 2 * 95 * (10**(-9))

	gm, _, _, _ = h.get_transconductance(current=ids_high_vds, voltage=vgs)

	gm_div_w = gm/W 
	ids_high_vds_div_w = ids_high_vds/W

	# Plot Ids/W on X, gm/W on Y
	h.plot_generic(x=ids_high_vds_div_w, y=gm_div_w, xlabel="Ids/W [A/m]", ylabel="gm/W [S/m]", title="gm/W vs Ids/W", device=device)

if __name__ == "__main__":
	#part1()
	#part2()
	#part3()
	#postlabq3()
	postlabq4()