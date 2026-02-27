import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

D_m = 0.007  # Diameter in meters
A_m2 = (np.pi / 4) * D_m**2  # Cross-sectional area in square meters
L_m = 1  # Length of the pipe in meters
rho = 998.0  # Density of water (kg/m³)
nu = 10e-7  # Kinematic viscosity (m²/s)

def process_pipe_flow(csv_file):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Discharge Q (m³/s)
    df['Q'] = df['volume_m3'] / df['time_sec']

    # Hydraulic gradient i
    df['i'] = df['hf_m'] / L_m

    # Velocity V (m/s)
    df['V'] = df['Q'] / A_m2

    # Reynolds Number
    df['Re'] = (df['V'] * D_m) / nu

    # Friction factor
    g = 9.81
    df['f'] = df['hf_m'] / ((L_m / D_m) * (df['V']**2 / (2 * g)))
    df['f_1'] = 64 / df['Re']  # Laminar equation (f = 64/Re)
    df['f_2'] = 0.01364 / (df['Re']**0.25)  # Empirical equation for turbulent flow
    
    # -------- PLOTS -------- #

    # 1️⃣ i vs Q (Polynomial Fit)
    plt.figure()
    plt.scatter(df['Q'], df['i'], color='blue', label='Data Points')

    # Polynomial fit (2nd degree)
    coeffs = np.polyfit(df['Q'], df['i'], 2)
    poly_eq = np.poly1d(coeffs)
    x_fit = np.linspace(min(df['Q']), max(df['Q']), 100)
    y_fit = poly_eq(x_fit)
    
    plt.plot(x_fit, y_fit, 'r-', label=f"Fit: {poly_eq}")
    plt.xlabel("Discharge Q (m³/s)")
    plt.ylabel("Hydraulic Gradient i")
    plt.title("i vs Q with Polynomial Fit")
    plt.legend()
    plt.grid(True)
    plt.savefig("i_vs_Q_polyfit.png")
    plt.close()

    # 2️⃣ i vs V (Log-Log) with Polynomial Fit
    plt.figure()
    plt.scatter(df['V'], df['i'], color='blue', label='Data Points')

    # Polynomial fit (2nd degree)
    coeffs_v = np.polyfit(np.log(df['V']), np.log(df['i']), 1)
    poly_eq_v = np.poly1d(coeffs_v)
    x_fit_v = np.linspace(min(df['V']), max(df['V']), 100)
    y_fit_v = np.exp(poly_eq_v(np.log(x_fit_v)))

    plt.plot(x_fit_v, y_fit_v, 'r-', label=f"Fit: {poly_eq_v}")
    plt.xlabel("Velocity V (m/s)")
    plt.ylabel("Hydraulic Gradient i")
    plt.title("i vs V with Polynomial Fit (Log-Log)")
    plt.legend()
    plt.grid(True, which="both")
    plt.savefig("i_vs_V_polyfit.png")
    plt.close()

    # 3️⃣ f vs Re (Log-Log)
    plt.figure()
    plt.loglog(df['Re'], df['f'], 'o-', label="Experimental")

    # Split the Reynolds numbers into laminar and turbulent regions
    Re_laminar = df[df['Re'] < 2000]
    Re_turbulent = df[df['Re'] > 2000]

    # Laminar line (f = 64/Re) for Re < 2000
    plt.loglog(Re_laminar['Re'], 64/Re_laminar['Re'], '--', label="Laminar (f = 64/Re)")

    # Blasius equation for turbulent (f = 0.3164/Re^0.25) for Re > 2000
    plt.loglog(Re_turbulent['Re'], 0.3164 / (Re_turbulent['Re']**0.25), '--', label="Blasius (f = 0.3164/Re^0.25)")

    plt.xlabel("Reynolds Number (Re)")
    plt.ylabel("Friction Factor (f)")
    plt.title("f vs Re (Log-Log)")
    plt.legend()
    plt.grid(True, which="both")
    plt.savefig("f_vs_Re_loglog.png")
    plt.close()

    print("Plots saved successfully:")
    print(" - i_vs_Q_polyfit.png")
    print(" - i_vs_V_polyfit.png")
    print(" - f_vs_Re_loglog.png")


# -----------------------------
# Run the function
# -----------------------------
if __name__ == "__main__":
    csv_path = "input_data.csv"  # Change this to your file name
    process_pipe_flow(csv_path)
