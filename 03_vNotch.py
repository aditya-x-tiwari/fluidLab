
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def process_v_notch(csv_file):
    df = pd.read_csv(csv_file)

    g = 9.81

    # Convert theta to radians
    df['theta_rad'] = np.deg2rad(df['theta_deg'])

    # Volume collected
    df['Volume'] = df['A_tank'] * df['h_m']

    # Actual discharge
    df['Q_actual'] = df['Volume'] / df['time_sec']

    # Theoretical constant K1
    df['K1'] = (8/15) * np.tan(df['theta_rad']/2) * np.sqrt(2*g)

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
    plt.loglog(df['H_m'], df['Q_actual'], 'o-', label="Actual Q")
    plt.loglog(df['H_m'], df['Q_theoretical'], '--', label="Theoretical Q")
    plt.xlabel("Head H (m)")
    plt.ylabel("Discharge Q (m³/s)")
    plt.title("Q vs H (Log-Log)")
    plt.legend()
    plt.grid(True, which="both")
    plt.savefig("Q_vs_H_loglog.png")
    plt.close()

    # 2️⃣ Cd vs H (Ordinary Plot)
    plt.figure()
    plt.plot(df['H_m'], df['Cd'], 'o-')
    plt.xlabel("Head H (m)")
    plt.ylabel("Coefficient of Discharge (Cd)")
    plt.title("Cd vs H")
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
    process_v_notch("vnotch_input.csv")