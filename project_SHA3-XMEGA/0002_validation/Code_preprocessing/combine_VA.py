import numpy as np
import h5py
import sys
import time

TAG = 'VA'
SET_SIZE = 100
SET_NUM = 10
TraceLen = 36000*25

def PartGenerate(part):
  print('===================================================================')
  print('Part '+str(part).zfill(2), time.asctime())
  Fname = '../Processed_HDF5/part_'+str(part).zfill(2)+'.hdf5'
  print(Fname)
  lower = part*SET_NUM
  upper = lower+SET_NUM
  FILE = h5py.File(Fname, 'w')
  Traces = FILE.create_dataset('Traces', (SET_SIZE*SET_NUM, TraceLen), dtype='f8', compression="gzip", compression_opts=9)
  for set_idx in range(lower, upper):
    print('    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    Sname = '../Processed_HDF5/Processed_'+TAG+'_'+str(set_idx).zfill(4)+'.hdf5'
    print('    '+Sname, time.asctime())
    set_lower = (set_idx-lower)*SET_SIZE
    set_upper = set_lower+SET_SIZE
    SET_FILE = h5py.File(Sname, 'r')
    Traces[set_lower:set_upper,:] = SET_FILE['Traces'][()]
    SET_FILE.close()
  FILE.flush()
  FILE.close()
  return

def Check(part):
  print('===================================================================')
  print('Part '+str(part).zfill(2), time.asctime())
  Fname = '../Processed_HDF5/part_'+str(part).zfill(2)+'.hdf5'
  print(Fname)
  lower = part*SET_NUM
  upper = lower+SET_NUM
  FILE = h5py.File(Fname, 'r')
  for set_idx in range(lower, upper):
    print('    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    Sname = '../Processed_HDF5/Processed_'+TAG+'_'+str(set_idx).zfill(4)+'.hdf5'
    print('    '+Sname, time.asctime())
    set_lower = (set_idx-lower)*SET_SIZE
    set_upper = set_lower+SET_SIZE
    SET_FILE = h5py.File(Sname, 'r')
    print('    ', np.array_equiv(FILE['Traces'][set_lower:set_upper,:], SET_FILE['Traces']))
    SET_FILE.close()
  FILE.close()
  return

if __name__=='__main__':
  tag = sys.argv[1]
  L = int(sys.argv[2])
  U = int(sys.argv[3])
  for p in range(L, U):
    if tag=='combine':
      PartGenerate(p)
    elif tag=='check':
      Check(p)

