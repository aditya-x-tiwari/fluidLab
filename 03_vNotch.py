import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

A_tank = 0.75  # Cross-sectional area of the tank in m²
theta_deg = 90  # Angle of the notch in degrees

def process_v_notch(csv_file):
    df = pd.read_csv(csv_file)
    g = 9.81  # Acceleration due to gravity (m/s²)

    # Convert theta to radians
    theta_rad = np.deg2rad(theta_deg)

    # Volume collected
    df['Volume'] = A_tank * df['h_m']

    # Actual discharge
    df['Q_actual'] = df['Volume'] / df['time_sec']

    # Theoretical constant K1
    df['K1'] = (8/15) * np.tan(theta_rad/2) * np.sqrt(2 * g)

    # H^(5/2)
    df['H_5_2'] = df['H_m']**(5/2)

    # Theoretical discharge
    df['Q_theoretical'] = df['K1'] * df['H_5_2']

    # Coefficient of discharge
    df['Cd'] = df['Q_actual'] / df['Q_theoretical']

    # Mean Cd
    mean_cd = df['Cd'].mean()
    print(f"Mean Cd = {mean_cd:.5f}")

    # -------- PLOTS -------- #

    # 1️⃣ Q vs H (Log-Log Plot)
    plt.figure()
    plt.scatter(df['H_m'], df['Q_actual'], color='blue', label="Actual Q")
    plt.scatter(df['H_m'], df['Q_theoretical'], color='green', label="Theoretical Q")

    # Log-log regression (fit line for actual Q)
    log_H = np.log(df['H_m'])
    log_Q_actual = np.log(df['Q_actual'])
    coeffs_actual = np.polyfit(log_H, log_Q_actual, 1)  # Fit a line (log-log)
    fit_line_actual = np.poly1d(coeffs_actual)
    
    # Plot the best fit line for actual Q
    plt.plot(df['H_m'], np.exp(fit_line_actual(np.log(df['H_m']))), 'r--', label=f"Fit: Q ~ H^{coeffs_actual[0]:.2f}")

    # Log-log regression (fit line for theoretical Q)
    log_Q_theoretical = np.log(df['Q_theoretical'])
    coeffs_theoretical = np.polyfit(log_H, log_Q_theoretical, 1)  # Fit a line (log-log)
    fit_line_theoretical = np.poly1d(coeffs_theoretical)

    # Plot the best fit line for theoretical Q
    plt.plot(df['H_m'], np.exp(fit_line_theoretical(np.log(df['H_m']))), 'g--', label=f"Fit: Q ~ H^{coeffs_theoretical[0]:.2f}")

    plt.xlabel("Head H (m)")
    plt.ylabel("Discharge Q (m³/s)")
    plt.title("Q vs H (Log-Log)")
    plt.legend()
    plt.grid(True, which="both")
    plt.savefig("Q_vs_H_loglog.png")
    plt.close()

    # 2️⃣ Cd vs H (Ordinary Plot)
    plt.figure()
    plt.scatter(df['H_m'], df['Cd'], color='blue', label="Cd values")

    # Linear regression (fit line for Cd)
    coeffs_cd = np.polyfit(df['H_m'], df['Cd'], 1)  # Fit a line (linear)
    fit_line_cd = np.poly1d(coeffs_cd)

    # Plot the best fit line for Cd
    plt.plot(df['H_m'], fit_line_cd(df['H_m']), 'r--', label=f"Fit: Cd = {coeffs_cd[0]:.2f} * H + {coeffs_cd[1]:.2f}")

    plt.xlabel("Head H (m)")
    plt.ylabel("Coefficient of Discharge (Cd)")
    plt.title("Cd vs H")
    plt.legend()
    plt.grid(True)
    plt.savefig("Cd_vs_H.png")
    plt.close()

    # Save computed table
    df.to_csv("v_notch_calculated_output.csv", index=False)

    print("Files saved:")
    print(" - Q_vs_H_loglog.png")
    print(" - Cd_vs_H.png")
    print(" - v_notch_calculated_output.csv")

# -----------------------------
if __name__ == "__main__":
    process_v_notch("input_data.csv")  # Change this to your file name
