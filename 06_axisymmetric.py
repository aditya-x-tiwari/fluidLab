import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def axisymmetric_jet_analysis(csv_file):

    # Load CSV
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()

    # Extract columns
    r = df['r_mm'].values
    V_D = df['V_D'].values
    V_5D = df['V_5D'].values
    V_10D = df['V_10D'].values

    # -------- Sort data (VERY IMPORTANT) --------
    sort_idx = np.argsort(r)
    r = r[sort_idx]
    V_D = V_D[sort_idx]
    V_5D = V_5D[sort_idx]
    V_10D = V_10D[sort_idx]

    # -------- Mirror for symmetry --------
    r_full = np.concatenate((-r[::-1], r))

    def mirror(V):
        return np.concatenate((V[::-1], V))

    V_D_full = mirror(V_D)
    V_5D_full = mirror(V_5D)
    V_10D_full = mirror(V_10D)

    # -------- Smooth curve using polynomial fit --------
    r_smooth = np.linspace(min(r_full), max(r_full), 300)

    def smooth_fit(r, V, degree=4):  # 4 is enough, don't go crazy
        coeffs = np.polyfit(r, V, degree)
        return np.polyval(coeffs, r_smooth)

    V_D_fit = smooth_fit(r_full, V_D_full)
    V_5D_fit = smooth_fit(r_full, V_5D_full)
    V_10D_fit = smooth_fit(r_full, V_10D_full)

    # -------- Plot --------
    plt.figure()

    # Raw points
    plt.scatter(r_full, V_D_full, label='z = D')
    plt.scatter(r_full, V_5D_full, label='z = 5D')
    plt.scatter(r_full, V_10D_full, label='z = 10D')

    # Smooth best-fit curves
    plt.plot(r_smooth, V_D_fit)
    plt.plot(r_smooth, V_5D_fit)
    plt.plot(r_smooth, V_10D_fit)

    plt.xlabel("Radial Distance r (mm)")
    plt.ylabel("Axial Velocity (m/s)")
    plt.title("Axisymmetric Jet Velocity Profile")

    plt.legend()
    plt.grid(True)

    plt.savefig("axisymmetric_jet_velocity_profile.png")
    plt.show()


if __name__ == "__main__":
    axisymmetric_jet_analysis("input_data.csv")
