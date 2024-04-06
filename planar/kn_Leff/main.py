import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = ['planar_lp065_w1_n80_transfer.txt', 'planar_lp090_w1_n80_transfer.txt',
         'planar_lp13_w1_n80_transfer.txt', 'planar_lp18_w1_n80_transfer.txt',
         'planar_lp25_w1_n80_transfer.txt', 'planar_lp35_w1_n80_transfer.txt']

x = [65, 90, 130, 180, 250, 350]
x = [0.001 * i for i in x]
y = []

for item in files:
    # Load data from the text file into a DataFrame
    data = pd.read_csv(item, delim_whitespace=True, names=['Vg', 'Id', 'Ig'])

    # Calculate gm (transconductance) as the derivative of Id with respect to Vg
    data['gm'] = np.gradient(data['Id'], data['Vg'])

    # Find the peak gm and the corresponding Vg and Id
    peak_gm_index = data['gm'].idxmax()
    peak_gm = data.loc[peak_gm_index, 'gm']
    peak_Vg = data.loc[peak_gm_index, 'Vg']
    peak_Id = data.loc[peak_gm_index, 'Id']
    print("Peak gm:", peak_gm)
    print("Vg at peak gm:", peak_Vg)
    print("Current at peak gm:", peak_Id)

    # # Plot gm vs. Vg
    # plt.plot(data['Vg'], data['gm'])
    # plt.plot(data['Vg'], data['Id'])
    # plt.xlabel('Vg')
    # plt.ylabel('gm')
    # plt.title('Transconductance (gm) vs. Vg')
    # plt.grid(True)
    # plt.show()

    # Constants
    Rs = 220 / 80
    Rd = 220 / 80

    # Calculate the corrected VDS
    VDS_prime = 0.04 - peak_Id * (Rs + Rd)

    y.append(VDS_prime * 80 / peak_gm)

z = np.polyfit(x, y, 1)
print(z)

# Generate equation for the best fit line
best_fit_eqn = f'y = {z[0]:.4f}x + {z[1]:.4f}'

plt.scatter(x, y)
plt.plot(np.linspace(0, 0.4), z[0] * np.linspace(0, 0.4) + z[1], label=best_fit_eqn, color="red")

plt.xlabel('Ldrawn (um)')
plt.ylabel('VDS\'W/gmin(peak)')
plt.title('VDS\'W/gmin(peak) vs. Ldrawn')
plt.grid(True)
plt.legend()

plt.show()

kn = 1 / z[0]
delta_L = -1 * z[1] / z[0]

print(kn)
print(delta_L)
