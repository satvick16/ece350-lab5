import numpy as np
import matplotlib.pyplot as plt

# Read data from the text file
data = np.genfromtxt('planar_lp065_w1_n80_transfer.txt', skip_header=1)

# Extracting Vg, Id, and Ig
Vg = data[:, 0]
Id = data[:, 1]
Ig = data[:, 2]

# Calculating gm (transconductance) - derivative of Id with respect to Vg
Vg_step = Vg[1] - Vg[0]  # Assuming Vg is equally spaced
gm = np.gradient(Id, Vg_step)

# Assuming W is 80 micrometers
W = 80e-6  # meters

# Calculating gm/W and Ids/W
gm_W = gm / W
Ids_W = Id / W

# Plotting gm/W against Ids/W
plt.plot(Ids_W, gm_W)
plt.xlabel('Ids/W (A/m)')
plt.ylabel('gm/W (S/m)')
plt.title('gm/W vs Ids/W for planar mosfet')
plt.grid(True)
plt.show()
