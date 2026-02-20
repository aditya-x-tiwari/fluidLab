
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -----------------------------
# DATA
# -----------------------------
theta_deg = np.array([2, 3, 5, 7, 8])
theta = np.deg2rad(theta_deg)   # radians
GM = np.array([0.143, 0.191, 0.171, 0.163, 0.178])

# -----------------------------
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
