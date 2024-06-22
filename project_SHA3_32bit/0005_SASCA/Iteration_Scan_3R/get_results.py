import numpy as np
import sys

tag = '3R_B'
L = int(sys.argv[1])
U = int(sys.argv[2])

Block = []
for t in range(L, U):
  Sname = 'Success/success_'+str(t).zfill(4)+'.npy'
  Block.append(np.load(Sname))
Block = np.array(Block, dtype=np.int32)
Iterations = np.sum(Block, axis=0)
np.save(('iteration_scan_'+tag+'.npy'), Iterations)


