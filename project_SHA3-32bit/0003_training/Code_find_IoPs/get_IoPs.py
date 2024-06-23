import numpy as np
import h5py
import sys
import time

ICS_DIR = 'ics_original_010/'

class IOPS_Extractor:
  def __init__(self):
    self.CompleteTraceFiles = []
    for t in range(0, 16):
      fname = '../Processed_HDF5/part_'+str(t).zfill(2)+'.hdf5'
      print('Loading', fname)
      self.CompleteTraceFiles.append(h5py.File(fname, 'r'))
    return
  
  def close(self):
    for t in range(0, 16):
      print('Closing file part '+str(t).zfill(2))
      self.CompleteTraceFiles[t].close()
  
  def get_IoPs(self, Tag, Num):
    print('=====================================================')
    print(Tag+' i'+str(Num).zfill(2))
    name_ics = ICS_DIR+'ics_'+Tag+'_i'+str(Num).zfill(2)+'.npy'
    ICs = np.load(name_ics)
    IoPs = []
    for part in range(0, 16):
      print('part '+str(part).zfill(2), time.asctime())
      IoPs_Part = []
      for it in range(0, len(ICs)):
        L = ICs[it]*10
        U = L+10
        IoPs_Part.append(self.CompleteTraceFiles[part]['Traces'][:,L:U])
      IoPs.append(np.hstack(IoPs_Part))
    name_output = 'IoPs/Ints_'+Tag+'_i'+str(Num).zfill(2)+'.hdf5'
    FILE = h5py.File(name_output, 'w')
    FILE.create_dataset('IoPs', compression="gzip", compression_opts=9, data=np.vstack(IoPs))
    FILE.close()
  
  def get_state(self, tag, lower, upper):
    for ints in range(lower, upper):
      self.get_IoPs(tag, ints)
    return
  
  def get_round(self, RD):
    self.get_state('A'+str(RD).zfill(2), 0, 50)
    self.get_state('B'+str(RD).zfill(2), 0, 50)
    self.get_state('C'+str(RD).zfill(2), 0, 10)
    self.get_state('D'+str(RD).zfill(2), 0, 10)
    return
    
if __name__=='__main__':
  rd = int(sys.argv[1])
  Extractor = IOPS_Extractor()
  Extractor.get_round(rd)
  Extractor.close()
