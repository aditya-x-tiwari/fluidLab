# fluidLab 🌀

Computational toolkit for Fluid Mechanics Laboratory experiments.

This repository contains Python scripts developed to automate calculations, plotting, and data analysis for core undergraduate fluid mechanics lab experiments.

Developed as part of Mechanical Engineering coursework at Jadavpur University.

---

## 📌 Experiments Covered

### Determination of MetaCentric Height
- Variation of metacentric height with sliding weights
- Metacentre dependence on angle of heel 
- Metacentric height calculation
- Metacentre vs Angle of Heel plot 

---

### Characteristics of Pipe Flow
- Reynolds number calculation
- Friction factor determination
- Laminar vs turbulent verification
- Log-log plots:
  - f vs Re
  - i vs V
  - i vs Q

---

### Calibration of V-Notch
- Theoretical discharge calculation
- Actual discharge computation
- Coefficient of discharge (Cd)
- Log-log plot of Q vs H
- Cd vs H curve

---

### Verification of Stokes’ Law
- Terminal velocity computation
- Reynolds number calculation
- Drag coefficient (experimental & theoretical)
- Cd vs Re (log-log)
- Oseen correction implementation
- Viscosity determination using Falling Sphere Method

---

### Calibration of Orifice / Venturimeter / Rotameter
- Theoretical discharge (Bernoulli-based)
- Actual discharge from volumetric tank
- Cd vs Re plots
- Rotameter calibration

---

## ⚙️ Features

✔ Automatic CSV-based data processing  
✔ Log-log and standard plotting  
✔ Theoretical correlation comparison  
✔ Experimental vs analytical validation  
✔ Full results export to CSV  

---

## 🛠 Tech Stack

- Python 3.x
- NumPy
- Pandas
- Matplotlib

---

## 📊 Output Generated

- Publication-ready plots (PNG)
- Processed result tables (CSV)
- Reynolds number regime validation
- Theoretical vs experimental comparison

---

## 📎 How to Use

1. Prepare experimental data in CSV format.
2. Run the corresponding script:
   ```bash
   python {experiment_name}.py
   
