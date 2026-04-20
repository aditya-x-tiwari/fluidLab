import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def axisymmetric_jet_analysis(csv_file):

    # Load CSV
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()  # clean headers

    # Extract columns
    r = df['r_mm'].values

    V_D = df['V_D'].values
    V_5D = df['V_5D'].values
    V_10D = df['V_10D'].values

    # -------- Create symmetric radial data --------
    r_full = np.concatenate((-r[::-1], r))

    def mirror(V):
        return np.concatenate((V[::-1], V))

    V_D_full = mirror(V_D)
    V_5D_full = mirror(V_5D)
    V_10D_full = mirror(V_10D)

    # -------- Mean velocity curve --------
    V_mean = (V_D_full + V_5D_full + V_10D_full) / 3

    # -------- Gaussian fit (realistic profile) --------
    # V = V0 * exp(- (r^2 / a^2))
    coeffs = np.polyfit(r_full**2, np.log(np.abs(V_mean)+1e-6), 1)
    a = -1 / coeffs[0]

    r_smooth = np.linspace(min(r_full), max(r_full), 200)
    V_fit = np.exp(coeffs[1]) * np.exp(coeffs[0] * r_smooth**2)

    # -------- Plot --------
    plt.figure()

    plt.plot(r_full, V_D_full, 'o', label='z = D')
    plt.plot(r_full, V_5D_full, 's', label='z = 5D')
    plt.plot(r_full, V_10D_full, '^', label='z = 10D')

    # Mean curve
    plt.plot(r_full, V_mean, 'k--', linewidth=2, label='Mean Profile')

    # Smooth Gaussian fit
    plt.plot(r_smooth, V_fit, 'r-', linewidth=2, label='Gaussian Fit')

    plt.xlabel("Radial Distance r (mm)")
    plt.ylabel("Axial Velocity (m/s)")
    plt.title("Axisymmetric Jet Velocity Profile")

    plt.legend()
    plt.grid(True)

    plt.savefig("axisymmetric_jet_velocity_profile.png")
    plt.show()

    # -------- Centerline Velocity --------
    centerline = df.iloc[0]

    print("\nCenterline Velocities:")
    print("At z = D   :", centerline['V_D'], "m/s")
    print("At z = 5D  :", centerline['V_5D'], "m/s")
    print("At z = 10D :", centerline['V_10D'], "m/s")


if __name__ == "__main__":
    axisymmetric_jet_analysis("input_data.csv")
