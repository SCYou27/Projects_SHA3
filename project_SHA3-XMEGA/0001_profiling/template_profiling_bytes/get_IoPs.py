import numpy as np
import h5py
import sys
import time

ICS_DIR = 'ics_combined_090/'

class IOPS_Extractor:
  def __init__(self):
    self.CompleteTraceFiles = []
    for t in range(0, 20):
      fname = '../Processed_HDF5/part_'+str(t).zfill(2)+'.hdf5'
      print('Loading', fname)
      self.CompleteTraceFiles.append(h5py.File(fname, 'r'))
    return
  
  def close(self):
    for t in range(0, 20):
      print('Closing file part '+str(t).zfill(2))
      self.CompleteTraceFiles[t].close()
    return
  
  def get_IoPs(self, Tag, byte):
    print('=====================================================')
    print(Tag+' b'+str(byte).zfill(3), time.asctime())
    name_ics = ICS_DIR+'ics_'+Tag+'_b'+str(byte).zfill(3)+'.npy'
    ICs = np.load(name_ics)
    print('Number of interesting clock cycles:', len(ICs))
    IoPs = []
    for part in range(0, 20):
      print('part '+str(part).zfill(2), time.asctime())
      IoPs_Part = []
      for it in range(0, len(ICs)):
        L = ICs[it]*25
        U = L+25
        IoPs_Part.append(self.CompleteTraceFiles[part]['Traces'][:,L:U])
      IoPs.append(np.hstack(IoPs_Part))
    return np.vstack(IoPs)
  
if __name__=='__main__':
  Extractor = IOPS_Extractor()
  ICS = Extractor.get_IoPs('A00', 173)
  Extractor.close()
  print(np.shape(ICS))
  print(time.asctime())
