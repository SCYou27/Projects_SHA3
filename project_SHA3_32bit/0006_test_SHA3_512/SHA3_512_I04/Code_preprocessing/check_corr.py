import numpy as np
import sys
bound = float(sys.argv[1])
L = int(sys.argv[2])
U = int(sys.argv[3])
for t in range(L, U):
  print("===========================================")
  print("Set #"+str(t).zfill(4))
  T = np.load("Corrcoefs/SHA3_512_I04_"+str(t).zfill(4)+".npy")
  for s in range(0, len(T)):
    if T[s]<bound:
      print(t, s, T[s])

