
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import csv

# -----------------------------
# DATA FROM CSV
# -----------------------------

theta_deg = []
GM = []

with open('input_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        theta_deg.append(float(row['theta_deg']))
        GM.append(float(row['GM']))

# Convert to numpy arrays
theta_deg = np.array(theta_deg)
GM = np.array(GM)

# Convert degrees to radians
theta = np.deg2rad(theta_deg)

------------
# TRIGONOMETRIC MODEL
# GM = a + b*cos(theta)
# -----------------------------
def trig_model(theta, a, b):
    return a + b * np.cos(theta)

# Curve fitting
params, _ = curve_fit(trig_model, theta, GM)
a, b = params

# Smooth curve
theta_fit = np.linspace(0, max(theta), 200)
GM_fit = trig_model(theta_fit, a, b)

# Extrapolation at theta = 0
GM_0 = trig_model(0, a, b)

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(12, 8))

plt.scatter(theta_deg, GM, color='black', label='Experimental Data')
plt.plot(np.rad2deg(theta_fit), GM_fit, 'r-', linewidth=2,
         label='Trigonometric Best Fit')

plt.plot(0, GM_0, 'ro', markersize=8, label='GM at θ = 0°')
plt.plot([0, 0], [min(GM), GM_0], 'r--', linewidth=1.5)

plt.grid(True)
plt.xlabel('Angle of Heel, θ (degrees)')
plt.ylabel('Metacentric Height, GM (m)')
plt.title('GM vs Angle of Heel (Trigonometric Fit)')
plt.legend()
plt.tight_layout()

print(f"GM at zero heel (trigonometric fit) = {GM_0:.4f} m")

plt.show()
