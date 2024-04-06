import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = [
    ['planar_lp065_w1_n80_transfer_VD_0_04.txt',
    'planar_lp065_w1_n80_transfer_VD_1_2.txt'],
    ['planar_lp090_w1_n80_transfer_VD_0_04.txt',
    'planar_lp090_w1_n80_transfer_VD_1_2.txt'],
    ['planar_lp13_w1_n80_transfer_VD_0_04.txt',
    'planar_lp13_w1_n80_transfer_VD_1_2.txt'],
    ['planar_lp18_w1_n80_transfer_VD_0_04.txt',
    'planar_lp18_w1_n80_transfer_VD_1_2.txt'],
    ['planar_lp25_w1_n80_transfer_VD_0_04.txt',
    'planar_lp25_w1_n80_transfer_VD_1_2.txt'],
    ['planar_lp35_w1_n80_transfer_VD_0_04.txt',
    'planar_lp35_w1_n80_transfer_VD_1_2.txt']
    ]

for pair in files:
    _004 = pair[0]
    _12 = pair[1]

    df_004 = pd.read_table(_004, delim_whitespace=True, names=['Vg', 'Id', 'Ig'])
    df_12 = pd.read_table(_12, delim_whitespace=True, names=['Vg', 'Id', 'Ig'])

    plt.plot(df_004['Vg'], df_004['Id'], label='Id, VD = 0.04 V')
    plt.plot(df_12['Vg'], df_12['Id'], label='Id, VD = 1.2 V')

    plt.xlabel('Vg')
    plt.ylabel('Id')

    plt.title('Id vs Vg')

    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.savefig(f"Id_vs_Vg_{pair[0]}.png")
    plt.clf()

    # Finding Vg when Id is closest to 1e-7
    target_id = 1e-7

    closest_id_004 = df_004.iloc[(df_004['Id']-target_id).abs().argsort()[:1]]
    vg_closest_004 = closest_id_004['Vg'].values

    closest_id_12 = df_12.iloc[(df_12['Id']-target_id).abs().argsort()[:1]]
    vg_closest_12 = closest_id_12['Vg'].values

    print(f"For {_004}, Closest Vg when Id is {target_id}: {vg_closest_004}")
    print(f"For {_12}, Closest Vg when Id is {target_id}: {vg_closest_12}")
