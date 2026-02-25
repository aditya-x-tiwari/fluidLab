
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

D_m = 0.007 
A_m2 = (np.pi / 4) * D_m**2
L_m = 1
rho = 998.0
nu = 10e-7


def process_pipe_flow(csv_file):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Discharge Q
    df['Q'] = df['volume_m3'] / df['time_sec']

    # Hydraulic gradient i
    df['i'] = df['hf_m'] / df['L_m']

    # Velocity V
    df['V'] = df['Q'] / A_m2

    # Reynolds Number
    df['Re'] = (df['V'] * D_m) / nu

    # Friction factor
    g = 9.81
    df['f'] = df['hf_m'] / ((L_m/D_m) * (df['V']**2 / (2*g)))
    df['f_1'] = 64 / df['Re']
    df['f_2'] = 0.01364 / (df['Re']**0.25)
    
    # -------- PLOTS -------- #

    # 1️⃣ i vs Q (Ordinary Plot)
    plt.figure()
    plt.plot(df['Q'], df['i'], 'o-')
    plt.xlabel("Discharge Q (m³/s)")
    plt.ylabel("Hydraulic Gradient i")
    plt.title("i vs Q")
    plt.grid(True)
    plt.savefig("i_vs_Q.png")
    plt.close()

    # 2️⃣ i vs V (Log-Log)
    plt.figure()
    plt.loglog(df['V'], df['i'], 'o-')
    plt.xlabel("Velocity V (m/s)")
    plt.ylabel("Hydraulic Gradient i")
    plt.title("i vs V (Log-Log)")
    plt.grid(True, which="both")
    plt.savefig("i_vs_V_loglog.png")
    plt.close()

    # 3️⃣ f vs Re (Log-Log)
    plt.figure()
    plt.loglog(df['Re'], df['f'], 'o-', label="Experimental")

    # Laminar line (f = 64/Re)
    Re_range = np.linspace(min(df['Re']), max(df['Re']), 200)
    plt.loglog(Re_range, 64/Re_range, '--', label="Laminar (64/Re)")

    # Blasius equation for turbulent (smooth pipe)
    plt.loglog(Re_range, 0.3164/(Re_range**0.25), '--', label="Blasius")

    plt.xlabel("Reynolds Number (Re)")
    plt.ylabel("Friction Factor (f)")
    plt.title("f vs Re (Log-Log)")
    plt.legend()
    plt.grid(True, which="both")
    plt.savefig("f_vs_Re_loglog.png")
    plt.close()

    print("Plots saved successfully:")
    print(" - i_vs_Q.png")
    print(" - i_vs_V_loglog.png")
    print(" - f_vs_Re_loglog.png")


# -----------------------------
# Run the function
# -----------------------------
if __name__ == "__main__":
    csv_path = "input_data.csv"  # Change this to your file name
    process_pipe_flow(csv_path)
