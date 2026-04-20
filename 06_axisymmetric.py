import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


def axisymmetric_jet_analysis(csv_file):

    # Load CSV
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()

    # Extract columns
    r = df['r_mm'].values
    V_D = df['V_D'].values
    V_5D = df['V_5D'].values
    V_10D = df['V_10D'].values

    # -------- Mirror for symmetry --------
    r_full = np.concatenate((-r[::-1], r))

    def mirror(V):
        return np.concatenate((V[::-1], V))

    V_D_full = mirror(V_D)
    V_5D_full = mirror(V_5D)
    V_10D_full = mirror(V_10D)

    # -------- Smooth curves safely --------
    r_smooth = np.linspace(min(r_full), max(r_full), 300)

    def smooth_curve(r, V):

        # Remove NaN/Inf
        mask = np.isfinite(r) & np.isfinite(V)
        r_clean = r[mask]
        V_clean = V[mask]

        # Remove duplicate r values
        r_unique, indices = np.unique(r_clean, return_index=True)
        V_unique = V_clean[indices]

        # Sort
        idx = np.argsort(r_unique)
        r_sorted = r_unique[idx]
        V_sorted = V_unique[idx]

        # If too few points, skip
        if len(r_sorted) < 4:
            return None

        spline = make_interp_spline(r_sorted, V_sorted, k=3)
        return spline(r_smooth)

    V_D_fit = smooth_curve(r_full, V_D_full)
    V_5D_fit = smooth_curve(r_full, V_5D_full)
    V_10D_fit = smooth_curve(r_full, V_10D_full)

    # -------- Plot --------
    plt.figure()

    # Raw data
    plt.scatter(r_full, V_D_full, color='blue', label='z = D')
    plt.scatter(r_full, V_5D_full, color='orange', label='z = 5D')
    plt.scatter(r_full, V_10D_full, color='green', label='z = 10D')

    # Smooth curves
    if V_D_fit is not None:
        plt.plot(r_smooth, V_D_fit, color='blue', linewidth=2)

    if V_5D_fit is not None:
        plt.plot(r_smooth, V_5D_fit, color='orange', linewidth=2)

    if V_10D_fit is not None:
        plt.plot(r_smooth, V_10D_fit, color='green', linewidth=2)

    plt.xlabel("Radial Distance r (mm)")
    plt.ylabel("Axial Velocity (m/s)")
    plt.title("Axisymmetric Jet Velocity Profile")

    plt.legend()
    plt.grid(True)

    plt.savefig("axisymmetric_jet_velocity_profile.png")
    plt.show()


if __name__ == "__main__":
    axisymmetric_jet_analysis("input_data.csv")
