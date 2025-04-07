import matplotlib.pyplot as plt
import numpy as np
import os

fname = "20250406_165747_distLog.csv"
fname = "20250406_170207_distLog.csv"
fname = "20250406_170508_distLog.csv"
inDir = r"C:\Users\beale\Documents\Tiltmeter"

inFile = os.path.join(inDir, fname)

# array_data = np.random.rand(100, 100)
adata = np.genfromtxt(inFile, delimiter=",", dtype=int).T


# Display the array as a bitmap
plt.imshow(adata[10:-3,:], cmap='gray', interpolation='nearest', aspect='auto')
plt.colorbar()  # Add a colorbar to show the value mapping
plt.title("Array as Bitmap")
plt.show()
