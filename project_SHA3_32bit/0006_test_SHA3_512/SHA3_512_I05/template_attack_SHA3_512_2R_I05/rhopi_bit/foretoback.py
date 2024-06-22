import numpy as np
fore = np.load("./foresupliment.npy")
backsup = [-1]*1600

for f in range(0, 1600):
  backsup[fore[f]] = f

np.save("./backsupliment.npy", backsup)


