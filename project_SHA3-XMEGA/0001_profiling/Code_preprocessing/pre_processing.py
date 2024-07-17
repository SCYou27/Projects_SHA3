import numpy as np
import os
from array import array
import sys
import KECCAK as kec
import serv_manager as svm
import time
import h5py
OFFSET = 50000-20
PPC = 125
CLOCKS = 36000
PPC_NEW = 25
MUL = PPC//PPC_NEW

def io_data_process(set_n):
  old_dir = 'sha3_train_set_'+str(set_n).zfill(3)+'/'
  inname = old_dir+'inputs.txt'
  outname = old_dir+'outputs.txt'
  raw_inputs = []
  raw_outputs = []
  IN_obj = open(inname, 'r')
  OUT_obj = open(outname, 'r')
  for i in range(0, 40):
    raw_data_i = IN_obj.readline().rstrip()
    raw_inputs.append(raw_data_i.lower())
    raw_data_o = OUT_obj.readline().rstrip()
    raw_outputs.append(raw_data_o.lower())
  IN_obj.close()
  OUT_obj.close()
  pr_inputs = ''
  pr_outputs = ''
  for i in range(0, 40):
    print('===========================================================================')
    print('Raw Index: ', i)
    datahex = raw_inputs[i]
    result = kec.SHA3_512(datahex)
    if result==raw_outputs[i]:
      print('  Passed!')
    else:
      print('  Failed!:')
      print(result)
      print(raw_outputs[i])
  np.save(('data_raw_in/set_TR_'+str(set_n).zfill(4)+'_inputs.npy'), raw_inputs)
  np.save(('data_raw_out/set_TR_'+str(set_n).zfill(4)+'_outputs.npy'), raw_outputs)
  return
    

def preprocessing(set_n):
  # Decompressing
  InputDir = 'sha3_train_set_'+str(set_n).zfill(3)+'/'
  InputZip = '../Raw/sha3_train_set_'+str(set_n).zfill(3)+'.zip'
  Proc_Name =  '../Processed_HDF5/Processed_TR_'+str(set_n).zfill(4)+'.hdf5'
  Peak_Name =  '../Peaks_HDF5/Processed_DN_'+str(set_n).zfill(4)+'.hdf5'
  svm.System(('unzip '+InputZip))
  # I/O checking
  io_data_process(set_n)
  # Processing traces.
  Proc_Traces = []
  Detect_Samples = []
  for t in range(0, 40):
    for inv in range(0, 4):
      print('=============================================================')
      InputName = InputDir+'temp'+str(t).zfill(4)+'_'+str(inv)+'_ch0.bin'
      print(InputName)
      Samples_TR = []
      Samples_DN = []
      input_file = svm.Open(InputName, 'rb')
      float_array = array('d')
      float_array.frombytes(input_file.read())
      input_file.close()
      Raw_Trace = float_array[OFFSET:(OFFSET+PPC*CLOCKS)]
      for clc in range(0, CLOCKS):
        Fragment = Raw_Trace[(PPC*clc):(PPC*clc+PPC)]
        Samples_DN.append(max(Fragment))
        for p in range(0, PPC_NEW):
          lower = p*MUL
          upper = lower+MUL
          Samples_TR.append(sum(Fragment[lower:upper]))
      Proc_Traces.append(Samples_TR)
      Detect_Samples.append(Samples_DN)
  Proc_Traces = np.vstack(Proc_Traces)
  Detect_Samples = np.vstack(Detect_Samples)
  print('Data saving.')
  FILE_TR = h5py.File(Proc_Name, 'w')
  FILE_TR.create_dataset('Traces', np.shape(Proc_Traces), 'f8', compression='gzip', compression_opts=9, data=Proc_Traces)
  FILE_TR.close()
  FILE_DN = h5py.File(Peak_Name, 'w')
  FILE_DN.create_dataset('Traces', np.shape(Detect_Samples), 'f8', compression='gzip', compression_opts=9, data=Detect_Samples)
  FILE_DN.close()
  svm.System(('rm -r '+InputDir))
  return True

if __name__=='__main__':
  L = int(sys.argv[1])
  U = int(sys.argv[2])
  for Set_n in range(L, U):
    tS = time.time()
    Suc = preprocessing(Set_n)
    tE = time.time()
    print(tE-tS)
