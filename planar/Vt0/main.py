import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = ['planar_lp13_w1_n80_transfer.txt', 'planar_lp18_w1_n80_transfer.txt', 
         'planar_lp25_w1_n80_transfer.txt', 'planar_lp35_w1_n80_transfer.txt', 
         'planar_lp065_w1_n80_transfer.txt', 'planar_lp090_w1_n80_transfer.txt']

for item in files:
    # Read the data into a pandas DataFrame
    df = pd.read_table(item, delim_whitespace=True, names=['Vg', 'Id', 'Ig'])

    # Calculate the derivative of Id with respect to Vg and store it in a new column 'gm'
    df['gm'] = np.gradient(df['Id'], df['Vg'])

    # Plot Id and gm against Vg
    plt.plot(df['Vg'], df['Id'], label='Id')
    plt.plot(df['Vg'], df['gm'], label='gm')
    plt.xlabel('Vg')
    plt.ylabel('Id/gm')
    plt.title('Id and gm vs Vg')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"Idgm_vs_Vg_{item}.png")
    plt.clf()  # Clear the plot

    # Find the value of Vg where gm is at its peak (voltage_at_max_gm)
    voltage_at_max_gm_index = df['gm'].idxmax()
    voltage_at_max_gm = df['Vg'][voltage_at_max_gm_index]

    # Draw the tangent to the curve of Id at voltage_at_max_gm
    m = df['gm'][voltage_at_max_gm_index]  # Slope of tangent (gm at voltage_at_max_gm)
    x_values = np.linspace(min(df['Vg']), max(df['Vg']), 100)
    tangent_line = m * (x_values - voltage_at_max_gm) + df['Id'][voltage_at_max_gm_index]

    plt.plot(df['Vg'], df['Id'], label='Id')
    plt.plot(x_values, tangent_line, '--', label='Tangent at maximum gm')
    plt.scatter(voltage_at_max_gm, df['Id'][voltage_at_max_gm_index], color='red', label='maximum gm')
    plt.xlabel('Vg')
    plt.ylabel('Id')
    plt.title('Tangent to Id curve at maximum gm')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"tangent_{item}.png")
    plt.clf()  # Clear the plot

    # Find the x intercept of the tangent line
    x_intercept = voltage_at_max_gm - (df['Id'][voltage_at_max_gm_index] / m)
    print("x-intercept of the tangent line:", x_intercept)

    # Subtract 3kT/q
    Vt0 = x_intercept - 0.075
    print("Vt0:", Vt0)
