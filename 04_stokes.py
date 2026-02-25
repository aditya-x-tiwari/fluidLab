import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

L_m = 1
nu = 9.441e-4
rho = 959.6
gamma_s = 73575
gamma_L = 9413.676

def process_stokes(csv_file):
    df = pd.read_csv(csv_file)

    # Radius
    df['a'] = df['diameter_m'] / 2

    # Terminal velocity
    df['U'] = L_m / df['time_sec']

    # Reynolds number
    df['Re'] = (2 * df['U'] * df['a']) / nu

    # Theoretical Cd (Stokes)
    df['Cd_theoretical'] = 24 / df['Re']

    # Experimental Cd
    df['Cd_experimental'] = (8/3) * df['a'] * (gamma_s - gamma_L) / \
                            (rho * df['U']**2)

    # Dynamic viscosity from Stokes formula
    df['mu'] = (2 * df['a']**2 * (gamma_s - gamma_L)) / (9 * df['U'])

    mean_mu = df['mu'].mean()
    print(f"Mean viscosity (Pa·s) = {mean_mu:.5f}")

    # -------- PLOT -------- #

    plt.figure()
    plt.loglog(df['Re'], df['Cd_experimental'], 'o', label="Experimental")

    Re_range = np.linspace(min(df['Re']), max(df['Re']), 200)

    # Stokes law
    plt.loglog(Re_range, 24/Re_range, '--', label="Stokes (24/Re)")

    # Oseen correction
    plt.loglog(Re_range,
               24/Re_range * (1 + 3/16*Re_range),
               '--', label="Oseen")

    plt.xlabel("Reynolds Number (Re)")
    plt.ylabel("Drag Coefficient (Cd)")
    plt.title("Cd vs Re (Log-Log)")
    plt.legend()
    plt.grid(True, which="both")
    plt.savefig("Cd_vs_Re_loglog.png")
    plt.close()

    df.to_csv("stokes_calculated_output.csv", index=False)

    print("Files saved:")
    print(" - Cd_vs_Re_loglog.png")
    print(" - stokes_calculated_output.csv")


# -----------------------------
if __name__ == "__main__":
    process_stokes("input_data.csv")
