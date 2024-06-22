import numpy as np
import sys

tag = '2R_B'
L = int(sys.argv[1])
U = int(sys.argv[2])

block = []
results = []
for t in range(L, U):
  tname = 'Success/success_'+str(t).zfill(4)+'.npy'
  print(tname)
  block.append(np.load(tname))
block = np.vstack(block)
for r in range(0, 201):
  results.append(np.count_nonzero(block[:,r]))
np.save(('rate_scan_'+tag+'.npy'), results)


