import pandas as pd
import matplotlib.pyplot as plt


def axisymmetric_jet_analysis(csv_file):

    # Load CSV
    df = pd.read_csv(csv_file)

    # Extract columns
    r = df['r_mm']

    V_D = df['V_D']
    V_5D = df['V_5D']
    V_10D = df['V_10D']

    # -------- Plot Velocity Profiles --------
    plt.figure()

    plt.plot(r, V_D, marker='o', label='z = D')
    plt.plot(r, V_5D, marker='s', label='z = 5D')
    plt.plot(r, V_10D, marker='^', label='z = 10D')

    plt.xlabel("Radial Distance r (mm)")
    plt.ylabel("Axial Velocity (m/s)")
    plt.title("Velocity Distribution in Axisymmetric Jet")

    plt.legend()
    plt.grid(True)

    plt.savefig("axisymmetric_jet_velocity_profile.png")
    plt.show()

    # -------- Find Centerline Velocity --------
    centerline = df.iloc[0]

    print("\nCenterline Velocities:")
    print("At z = D   :", centerline['V_D'], "m/s")
    print("At z = 5D  :", centerline['V_5D'], "m/s")
    print("At z = 10D :", centerline['V_10D'], "m/s")


if __name__ == "__main__":
    axisymmetric_jet_analysis("input_data.csv")
