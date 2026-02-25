import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def process_orifice(csv_file):
    df = pd.read_csv(csv_file)

    g = 9.81

    # Convert units
    df['Qrota'] = df['Qrota_LPM'] / 1000 / 60   # LPM → m3/s
    df['H'] = df['H_mm'] / 1000                 # mm → m
    df['x'] = df['x_mm']                        # already in meters

    # Areas
    df['a1'] = np.pi * df['d1_m']**2 / 4
    df['a2'] = np.pi * df['d2_m']**2 / 4

    # Theoretical discharge
    df['Qth'] = (df['a1'] * df['a2'] *
                np.sqrt(2 * g * df['H'])) / \
                np.sqrt(df['a2']**2 - df['a1']**2)

    # Actual discharge
    df['Qact'] = (df['A_tank'] * df['x']) / df['time_sec']

    # Cd (orifice)
    df['Cd_orifice'] = df['Qact'] / df['Qth']

    # Cd (rotameter)
    df['Cd_rotameter'] = df['Qact'] / df['Qrota']

    # Velocity in pipe
    df['V'] = df['Qact'] / df['a2']

    # Reynolds number
    df['Re'] = (df['rho'] * df['V'] * df['d2_m']) / df['mu']

    print("Mean Cd (Orifice) =", df['Cd_orifice'].mean())
    print("Mean Cd (Rotameter) =", df['Cd_rotameter'].mean())

    # -------- PLOTS -------- #

    # 1️⃣ Cd_orifice vs Re
    plt.figure()
    plt.plot(df['Re'], df['Cd_orifice'], 'o-')
    plt.xlabel("Reynolds Number (Re)")
    plt.ylabel("Cd (Orifice)")
    plt.title("Cd (Orifice) vs Re")
    plt.grid(True)
    plt.savefig("Cd_orifice_vs_Re.png")
    plt.close()

    # 2️⃣ Cd_rotameter vs Re
    plt.figure()
    plt.plot(df['Re'], df['Cd_rotameter'], 'o-')
    plt.xlabel("Reynolds Number (Re)")
    plt.ylabel("Cd (Rotameter)")
    plt.title("Cd (Rotameter) vs Re")
    plt.grid(True)
    plt.savefig("Cd_rotameter_vs_Re.png")
    plt.close()

    # Save full table
    df.to_csv("orifice_calculated_output.csv", index=False)

    print("Files saved:")
    print(" - Cd_orifice_vs_Re.png")
    print(" - Cd_rotameter_vs_Re.png")
    print(" - orifice_calculated_output.csv")


if __name__ == "__main__":
    process_orifice("input_data.csv")
