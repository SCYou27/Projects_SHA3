import numpy as np
import h5py
import sys
import time

INVOC = 4
TraceLen = 900000
LOWER = 20
UPPER = 60

def InvocationGenerate(invoc):
  print('===================================================================')
  print('Invocation '+str(invoc).zfill(2), time.asctime())
  Fname = '../Processed_HDF5/Invocation_'+str(invoc).zfill(2)+'.hdf5'
  print(Fname)
  FILE = h5py.File(Fname, 'w')
  Traces = []
  for set_idx in range(LOWER, UPPER):
    print('    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    Sname = '../Processed_HDF5/Processed_I'+str(INVOC).zfill(2)+'_'+str(set_idx).zfill(4)+'.hdf5'
    print('    '+Sname, time.asctime())
    SET_FILE = h5py.File(Sname, 'r')
    Traces.append(SET_FILE['Traces_I'+str(invoc).zfill(2)][()])
    SET_FILE.close()
  FILE.create_dataset('Traces', (1000, TraceLen), dtype='f8', compression="gzip", compression_opts=9, data=np.vstack(Traces))
  FILE.flush()
  FILE.close()
  return

def Check(invoc):
  print('===================================================================')
  print('Invocation '+str(invoc).zfill(2), time.asctime())
  Fname = '../Processed_HDF5/Invocation_'+str(invoc).zfill(2)+'.hdf5'
  print(Fname)
  FILE = h5py.File(Fname, 'r')
  Traces = []
  for set_idx in range(LOWER, UPPER):
    print('    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    Sname = '../Processed_HDF5/Processed_I'+str(INVOC).zfill(2)+'_'+str(set_idx).zfill(4)+'.hdf5'
    print('    '+Sname, time.asctime())
    SET_FILE = h5py.File(Sname, 'r')
    Traces.append(SET_FILE['Traces_I'+str(invoc).zfill(2)][()])
    SET_FILE.close()
  print(np.array_equiv(np.vstack(Traces), FILE['Traces']))
  FILE.close()
  return

if __name__=='__main__':
  tag = sys.argv[1]
  L = int(sys.argv[2])
  U = int(sys.argv[3])
  for p in range(L, U):
    if tag=='combine':
      InvocationGenerate(p)
    elif tag=='check':
      Check(p)

