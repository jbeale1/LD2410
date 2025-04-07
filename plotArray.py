import matplotlib.pyplot as plt
import numpy as np
import os
# ------------------------------

import os
import glob

#     Finds the most recently modified .csv file in a directory.
def get_most_recent_csv(directory):
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        return None
    most_recent_csv = max(csv_files, key=os.path.getmtime)
    return most_recent_csv
# ----------------------------

inDir = r"C:\Users\beale\Documents\Tiltmeter"
# inFile = os.path.join(inDir, fname)
inFile = get_most_recent_csv(inDir)
fname = os.path.basename(inFile)

adata = np.genfromtxt(inFile, delimiter=",", dtype=int).T


# Display the array as a bitmap
fig, ax = plt.subplots()
im = ax.imshow(adata[10:-4,:], cmap='gray', interpolation='nearest', aspect='auto')
ax.set_yticks(np.arange(0, 19, 1), minor=False)
fig.colorbar(im)  # Add a colorbar to show the value mapping
plt.title(fname)
plt.show()
